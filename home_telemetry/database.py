import structlog

from datetime import datetime

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

from home_telemetry.models import Base, Measurement, MeasurementType, Source

_logger = structlog.get_logger(__name__)
engine = create_engine("sqlite:///test.db")
Base.metadata.create_all(engine)


def save_measurements(measurements: list[Measurement], engine: Engine = engine) -> None:
    if not measurements:
        return

    with Session(engine) as session:
        for measurement in measurements:
            session.add(measurement)
        session.commit()
    _logger.info(f"Saved {len(measurements)} measurements at {datetime.now().isoformat()}")


def get_measurements(
    measurement_type: MeasurementType,
    source: Source,
    datetime_lte: datetime | None = None,
    datetime_gte: datetime | None = None,
    description: str | None = None,
    engine: Engine = engine,
) -> list[Measurement]:
    with Session(engine) as session:
        query = session.query(Measurement).filter(
            Measurement.measurement_type == measurement_type,
            Measurement.source == source,
        )

    if datetime_lte:
        query = query.filter(Measurement.timestamp <= datetime_lte)

    if datetime_gte:
        query = query.filter(Measurement.timestamp >= datetime_gte)

    if description:
        query = query.filter(Measurement.description == description)

    return query.all()
