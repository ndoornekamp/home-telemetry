# Home telemetry

Personal app for collecting and persisting data from:

- Smart electricity meter (via the Homewizard P1 adapter)
- PV inverter (via the Solax LAN adapter)
- Heatpump (via Heishamon)

## Setup and usage

This project uses `poetry` for package management. To create a new env with the required packages, run:

`poetry install`

Or, if you don't need the dev dependencies:

`poetry install --without dev`

Then, either open a poetry shell using `poetry shell` and then run the module using `python -m home_telemetry`, or combine the two using `poetry run python -m home_telemetry`