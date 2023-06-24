from dataclasses import dataclass
import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, Float, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Source(enum.Enum):
    SOLAX = enum.auto()
    HOMEWIZARD_P1 = enum.auto()
    HEISHAMON = enum.auto()


class MeasurementType(enum.Enum):
    POWER = enum.auto()
    TEMPERATURE = enum.auto()
    FLOW = enum.auto()
    VOLTAGE = enum.auto()


class PhaseCode(enum.Enum):
    L1 = enum.auto()
    L2 = enum.auto()
    L3 = enum.auto()
    ALL = enum.auto()
    NONE = enum.auto()


@dataclass
class Measurement(Base):
    __tablename__ = "measurement"

    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[float] = mapped_column(Float)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    source: Mapped[Source] = mapped_column(Enum(Source))
    measurement_type: Mapped[MeasurementType] = mapped_column(Enum(MeasurementType))
    phasecode: Mapped[PhaseCode] = mapped_column(
        Enum(PhaseCode), default=PhaseCode.NONE
    )
    description: Mapped[str] = mapped_column(String, default=None, nullable=True)
