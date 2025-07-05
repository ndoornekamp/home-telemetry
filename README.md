# Home telemetry

Personal app for collecting and persisting data from:

- Smart electricity meter (via the Homewizard P1 adapter)
- PV inverter (via the Solax LAN adapter)
- Heatpump (via Heishamon)

## Setup

This project uses `uv` for package management. To create a new env with the required packages, run:

```bash
uv sync
```

Or, if you don't need the dev dependencies:

```bash
uv sync --without dev
```

### Non-Python dependencies for plotting

```bash
sudo apt install pyqt5-dev-tools

```

## Running the module locally

Then run the module using

```bash
uv run python -m home_telemetry
```

## Docker

Build the Docker image by running the build script: `sh build.sh`. Then run a container with that image alongside a Postgres database using

```bash
docker compose up
```
