from datetime import datetime
from time import sleep

from adapters import BaseAdapter, HeishamonAdapter, P1Adapter, SolaxAdapter
from config import P1_IP_ADDRESS, SOLAX_SERIAL_NUMBER, SOLAX_TOKEN_ID
from database import save_measurements
from models import Measurement


def fetch_data_all_sources(adapters: list[BaseAdapter]) -> list[Measurement]:
    measurements = []
    for adapter in adapters:
        try:
            measurements.extend(adapter.measure())
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
            measurements = fetch_data_all_sources(adapters=adapters)
            save_measurements(measurements)
            print(
                f"Fetched and saved {len(measurements)} measurements at {datetime.now().isoformat()}"
            )
        except Exception as e:
            print(f"Failed to fetch or save data at {datetime.now().isoformat()}: {e}")

        sleep(1)
