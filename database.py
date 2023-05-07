from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models import Base, Measurement


engine = create_engine('sqlite:///test.db')
Base.metadata.create_all(engine)


def save_measurements(measurements: list[Measurement]) -> None:
    with Session(engine) as session:
        for measurement in measurements:
            session.add(measurement)
        session.commit()
