from datetime import datetime
from time import sleep

from home_telemetry.adapters import BaseAdapter, HeishamonAdapter, P1Adapter, SolaxAdapter
from home_telemetry.config import P1_IP_ADDRESS, SOLAX_SERIAL_NUMBER, SOLAX_TOKEN_ID
from home_telemetry.database import save_measurements
from home_telemetry.models import Measurement


def get_aggregated_measurements(adapters: list[BaseAdapter]) -> list[Measurement]:
    measurements = []
    for adapter in adapters:
        try:
            adapter_measurements = adapter.measure()
            measurements.extend(adapter.aggregate(adapter_measurements))
        except Exception as e:
            print(f"Failed to fetch data from {adapter}: {e}")

    return measurements


if __name__ == "__main__":
    adapters = [
        HeishamonAdapter(),
        P1Adapter(ip_address=P1_IP_ADDRESS),
        SolaxAdapter(serial_number=SOLAX_SERIAL_NUMBER, token_id=SOLAX_TOKEN_ID),
    ]

    while True:
        try:
            aggregated_measurements = get_aggregated_measurements(adapters=adapters)
            save_measurements(aggregated_measurements)

            print(
                f"Fetched and saved {len(aggregated_measurements)} measurements at {datetime.now().isoformat()}"
            )
        except Exception as e:
            print(f"Failed to fetch or save data at {datetime.now().isoformat()}: {e}")

        sleep(1)
