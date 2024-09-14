import os
from minio import Minio
from minio.error import S3Error

# Configure the MinIO client with your MinIO server details
minio_client = Minio(
    os.environ.get('MINIO_ENDPOINT'),  # Replace with your MinIO server address and port
    access_key=os.environ.get('MINIO_ACCESS_KEY'),
    secret_key=os.environ.get('MINIO_SECRET_ACCESS_KEY'),
    secure=False,  # Set to True if using HTTPS
)

bucket_name = 'main-bucket-1'
try:
    found = minio_client.bucket_exists(bucket_name)

    if not found:
        minio_client.make_bucket(bucket_name)
        print("Created bucket", bucket_name)
    else:
        print("Bucket", bucket_name, "already exists")
except S3Error as exc:
        print("error occurred.", exc)  