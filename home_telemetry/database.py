from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models import Base, Measurement, MeasurementType, Source

engine = create_engine('sqlite:///test.db')
Base.metadata.create_all(engine)


def save_measurements(measurements: list[Measurement]) -> None:
    with Session(engine) as session:
        for measurement in measurements:
            session.add(measurement)
        session.commit()


def get_measurements(measurement_type: MeasurementType, source: Source) -> list[Measurement]:
    with Session(engine) as session:
        measurements = session.query(Measurement).filter(
            Measurement.measurement_type == measurement_type,
            Measurement.source == source
        ).all()

    return measurements
