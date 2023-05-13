from datetime import datetime
from time import sleep

from adapters import HeishamonAdapter, P1Adapter, SolaxAdapter
from config import P1_IP_ADDRESS, SOLAX_SERIAL_NUMBER, SOLAX_TOKEN_ID
from database import save_measurements
from models import Measurement


def fetch_data_all_sources() -> list[Measurement]:
    heishamon_adapter = HeishamonAdapter()
    p1_adapter = P1Adapter(ip_address=P1_IP_ADDRESS)
    solax_adapter = SolaxAdapter(
        serial_number=SOLAX_SERIAL_NUMBER, token_id=SOLAX_TOKEN_ID
    )

    measurements = []
    for adapter in [heishamon_adapter, p1_adapter, solax_adapter]:
        try:
            measurements.extend(adapter.measure())
        except Exception as e:
            print(f"Failed to fetch data from {adapter}: {e}")

    return measurements


if __name__ == "__main__":
    while True:
        try:
            measurements = fetch_data_all_sources()
            save_measurements(measurements)
            print(
                f"Fetched and saved {len(measurements)} measurements at {datetime.now().isoformat()}"
            )
        except Exception as e:
            print(f"Failed to fetch or save data at {datetime.now().isoformat()}: {e}")

        sleep(1)
