from minio import Minio
import streamlit as st
import os
from datetime import datetime, timedelta
import pickle
import numpy as np


# Configure the MinIO client with your MinIO server details
minio_client = Minio(
    os.environ.get('MINIO_ENDPOINT'),  # Replace with your MinIO server address and port
    access_key=os.environ.get('MINIO_ACCESS_KEY'),
    secret_key=os.environ.get('MINIO_SECRET_ACCESS_KEY'),
    secure=False,  # Set to True if using HTTPS
)

models = minio_client.list_objects(minio_client.list_buckets()[0].name, 'models/')
model_name = [f.object_name for f in models][-1]

minio_client.fget_object(minio_client.list_buckets()[0].name, model_name, "model.pkl")
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

st.title("Predict Tomorrow's Temperature in Madrid")
if st.button('Predict Temperature'):
    tomorrow = datetime.today() + timedelta(days=1)
    prediction = np.round(model.predict([[tomorrow.month, tomorrow.day]])[0], 1)
    st.write(f"Tomorrow's Temperature: {prediction}")

