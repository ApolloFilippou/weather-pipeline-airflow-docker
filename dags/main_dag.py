import os
import io
import pickle
from zipfile import ZipFile
import requests
import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from minio import Minio
import streamlit as st

# Configure the MinIO client with your MinIO server details
minio_client = Minio(
    os.environ.get('MINIO_ENDPOINT'),  # Replace with your MinIO server address and port
    access_key=os.environ.get('MINIO_ACCESS_KEY'),
    secret_key=os.environ.get('MINIO_SECRET_ACCESS_KEY'),
    secure=False,  # Set to True if using HTTPS
)

default_args = {
     'owner': 'airflow',
     'retries': 5,
     'retry_delay': timedelta(minutes=5)
}

def save_data_to_bucket():
    # Pull and unzip data
    response = requests.get('https://maven-datasets.s3.amazonaws.com/Madrid+Daily+Weather/Madrid+Daily+Weather+1997-2015.csv.zip')
    zipfile = ZipFile(io.BytesIO(response.content))
    filename = zipfile.extract(zipfile.namelist()[0])
    file_path = f'data/{filename.split('/')[-1]}'
    
    # Save to bucket
    minio_client.fput_object(minio_client.list_buckets()[0].name, file_path, filename)
    return file_path


def train_model_and_save_to_bucket(**kwargs):
    # Get dataset
    ti = kwargs['ti']
    file_path = ti.xcom_pull(task_ids='save_data_to_bucket')
    minio_client.fget_object(minio_client.list_buckets()[0].name, file_path, "data.csv")

    # Clean data
    df = pd.read_csv('data.csv')
    df[['Month', 'Day']] = df['CET'].apply(lambda x: x.split('-')[1:]).tolist()
    df_train = df[['Month', 'Day', 'Mean TemperatureC']].dropna().map(lambda x: int(x))

    # Train model
    linreg = LinearRegression()
    linreg.fit(df_train[['Month', 'Day']], df_train['Mean TemperatureC'])

    # Save model
    model_name = f'model-{datetime.now().strftime("%Y%m%d-%H%M%S")}.pkl'

    with open(model_name, 'wb') as f:
        pickle.dump(linreg, f) 

    # Save to bucket
    model_path = f'models/{model_name}'
    minio_client.fput_object(minio_client.list_buckets()[0].name, model_path, os.path.abspath(model_name))
    return model_path


with DAG(
     dag_id='main_dag',
     description='Some stuff here',
     default_args=default_args,
     start_date=datetime.today(),
     schedule_interval='@daily'
) as dag:
     

    save_data_to_bucket = PythonOperator(
        task_id='save_data_to_bucket',
        python_callable=save_data_to_bucket
    )

    train_model_and_save_to_bucket = PythonOperator(
        task_id='train_model_and_save_to_bucket',
        python_callable=train_model_and_save_to_bucket
    )


    save_data_to_bucket >> train_model_and_save_to_bucket