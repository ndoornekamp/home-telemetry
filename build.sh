#!/bin/sh

# Generate a requirements.txt so we don't need to install poetry in our Dockerfile
poetry export -f requirements.txt -o requirements.txt
docker build . -t home_telemetry
