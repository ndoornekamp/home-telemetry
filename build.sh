#!/bin/sh

# Generate a requirements.txt so we don't need to install poetry in our Dockerfile
uv export --no-dev --format requirements-txt --output-file requirements.txt

# Build images for AMD and ARM (e.g. Raspberry Pi) platforms & push to Dockerhub
docker buildx build --push --platform linux/amd64,linux/arm64 --tag ndoornekamp/home_telemetry:buildx-latest .
