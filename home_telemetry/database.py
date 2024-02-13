from datetime import datetime

import structlog
from sqlalchemy import URL, Engine, create_engine
from sqlalchemy.orm import Session

from home_telemetry import config
from home_telemetry.config import DatabaseType
from home_telemetry.models import Base, Measurement, MeasurementType, PhaseCode, Source

_logger = structlog.get_logger(__name__)

if config.DATABASE_TYPE == DatabaseType.POSTGRES:
    database_url = URL.create(
        drivername="postgresql+psycopg2",
        username=config.POSTGRES_USER,
        password=config.POSTGRES_PASSWORD,
        host=config.POSTGRES_HOST,
        port=config.POSTGRES_PORT,
        database=config.POSTGRES_DB,
    )
    engine = create_engine(database_url)
else:
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
    phase_code: PhaseCode | None = None,
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

    if phase_code:
        query = query.filter(Measurement.phasecode == phase_code)

    return query.order_by(Measurement.timestamp).all()
