import pytest
import structlog
from sqlalchemy import create_engine

from home_telemetry.database import get_measurements, save_measurements
from home_telemetry.models import Base, Measurement, MeasurementType, PhaseCode, Source

test_db_engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
Base.metadata.create_all(test_db_engine)


@pytest.fixture()
def measurements() -> list[Measurement]:
    return [
        Measurement(
            source=Source.HEISHAMON,
            measurement_type=MeasurementType.TEMPERATURE,
            value=18.0,
            description="test description",
            phasecode=PhaseCode.NONE,
        ),
    ]


def test_add_and_get_measurement_to_database(measurements: list[Measurement]) -> None:
    with structlog.testing.capture_logs() as caplog:
        save_measurements(measurements, engine=test_db_engine)

    measurements = get_measurements(
        measurement_type=MeasurementType.TEMPERATURE,
        source=Source.HEISHAMON,
        engine=test_db_engine,
    )

    assert len(measurements) == 1
    assert "Saved 1 measurement" in caplog[0]["event"]
