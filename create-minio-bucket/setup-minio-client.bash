#!/bin/bash

# # Install minio client
curl https://dl.min.io/client/mc/release/linux-arm64/mc --create-dirs -o ~/minio-binaries/mc

chmod +x $HOME/minio-binaries/mc
export PATH=$PATH:$HOME/minio-binaries/

# Create user
mc alias set minio "http://host.docker.internal:9000" minioadmin minioadmin