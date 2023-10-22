# Home telemetry

Personal app for collecting and persisting data from:

- Smart electricity meter (via the Homewizard P1 adapter)
- PV inverter (via the Solax LAN adapter)
- Heatpump (via Heishamon)

## Setup

This project uses `poetry` for package management. To create a new env with the required packages, run:

```bash
poetry install
```

Or, if you don't need the dev dependencies:

```bash
poetry install --without dev
```

## Running the module locally

Then, either open a poetry shell using `poetry shell` and then run the module using

```bash
python -m home_telemetry
```

or combine the two using

```bash
poetry run python -m home_telemetry
```

## Docker

Build the Docker image by running the build script: `sh build.sh`. Then run a container with that image alongside a Postgres database using

```bash
docker compose up
```
