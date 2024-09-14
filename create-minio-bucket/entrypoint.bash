#!/bin/bash

# Run your bash script
chmod +x setup-minio-client.bash
./setup-minio-client.bash

# Run your Python script
python ./create-minio-bucket.py