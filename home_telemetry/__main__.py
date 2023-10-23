import asyncio
import structlog

from datetime import datetime
from time import sleep

from home_telemetry.adapters import BaseAdapter, HeishamonAdapter, P1Adapter, SolaxAdapter
from home_telemetry.config import P1_IP_ADDRESS, SOLAX_SERIAL_NUMBER, SOLAX_TOKEN_ID, HEISHAMON_IP_ADDRESS
from home_telemetry.database import save_measurements
from home_telemetry.models import Measurement

_logger = structlog.get_logger(__name__)


async def get_tasks(adapters: list[BaseAdapter]) -> list[asyncio.Task]:
    tasks = [asyncio.create_task(adapter.update()) for adapter in adapters]
    return [await task for task in tasks]


def get_aggregated_measurements(adapters: list[BaseAdapter]) -> list[Measurement]:
    results = asyncio.run(get_tasks(adapters))
    return [measurement for result in results for measurement in result]


if __name__ == "__main__":
    adapters = [
        HeishamonAdapter(ip_address=HEISHAMON_IP_ADDRESS),
        P1Adapter(ip_address=P1_IP_ADDRESS),
        SolaxAdapter(serial_number=SOLAX_SERIAL_NUMBER, token_id=SOLAX_TOKEN_ID),
    ]

    _logger.info(f"Running with the following adapters: {[str(adapter) for adapter in adapters]}")

    while True:
        try:
            aggregated_measurements = get_aggregated_measurements(adapters=adapters)
            save_measurements(aggregated_measurements)
        except Exception:
            _logger.exception(f"Failed to fetch or save data at {datetime.now().isoformat()}")

        sleep(1)
