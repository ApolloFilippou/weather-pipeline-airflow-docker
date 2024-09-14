# weather-pipeline-airflow-docker

## Overview

This project demonstrates a data engineering pipeline that utilizes Docker, Airflow, MinIO, PostgreSQL, and Streamlit. The pipeline performs the following tasks:

1. Collects daily weather data for Madrid from a specified source and stores it in a MinIO bucket.
2. Pulls the data from the bucket and trains a linear regression model to predict the average temperature of a specific date.
3. Allows users to predict tomorrow's average temperature in Madrid via a Streamlit web application.

## Getting Started

To run the project, follow these steps:

1. Ensure Docker and Docker Compose are installed on your machine.
2. Clone this repository to your local machine.

   ```bash
   git clone https://github.com/ApolloFilippou/weather-pipeline-airflow-docker.git
   cd weather-pipeline-airflow-docker
   ```

3. Start all services using Docker Compose.

    ```bash
    docker compose up
    ```

    This command will set up and run the following services:
    - MinIO server and client
    - Apache Airflow instance (including web UI, scheduler, and triggerer)
    - Streamlit server

## Accessing the Services
- Airflow
    - http://localhost:8080/
    - Username: airflow
    - Password: airflow

- MinIO
    - http://localhost:9001/
    - Username: minioadmin
    - Password: minioadmin

- Streamlit
    - http://localhost:8501/


## Workflow Details

1. MinIO Setup
    - A MinIO client is installed and a user is created through a Docker container.
    - A MinIO server is containerized and a bucket is created inside it.

2. Airflow DAG
    - A single DAG is created with two steps:
        1. Data Collection: Collect daily weather data for Madrid from <https://mavenanalytics.io/> and store it in the MinIO bucket.
        2. Model Training: Pull the data from the bucket and train a linear regression model to predict the average temperature for a given date.

3. Streamlit Application
    - Access the Streamlit server to predict tomorrow's average temperature in Madrid by clicking a button on the web interface.


## Configuration

You can configure the following components by editing the respective files in the repository:

- Airflow: Modify DAGs in the dags/ directory.
- MinIO: Configuration can be adjusted in docker-compose.yml.
- Streamlit: Modify the Streamlit app in the streamlit/ directory.


## Troubleshooting

- Ensure that Docker and Docker Compose are correctly installed and running.
- Check the logs of individual Docker containers for errors using:

    ```bash
    docker-compose logs <service-name>
    ```
- Ensure that the ports (8080 for Airflow, 9001 for MinIO, 8501 for Streamlit) are not in use by other services.


## Acknowledgements

- Apache Airflow: https://airflow.apache.org/
- MinIO: https://min.io/
- Streamlit: https://streamlit.io/
- PostgreSQL: https://www.postgresql.org/
- Maven Analytics: https://mavenanalytics.io/