from unittest.mock import AsyncMock

import pytest

from home_telemetry.__main__ import get_aggregated_measurements
from home_telemetry.adapters import BaseAdapter
from home_telemetry.models import Measurement, MeasurementType, PhaseCode, Source


@pytest.fixture
def mock_adapter_1():
    measurements = [
        Measurement(
            source=Source.HEISHAMON,
            measurement_type=MeasurementType.TEMPERATURE,
            value=18.0,
            description="test description",
            phasecode=PhaseCode.NONE,
        )
    ]

    adapter = BaseAdapter()
    adapter.update = AsyncMock(return_value=measurements)
    return adapter


@pytest.fixture
def mock_adapter_2():
    aggregated_measurements = [
        Measurement(
            source=Source.HOMEWIZARD_P1,
            measurement_type=MeasurementType.VOLTAGE,
            value=230.0,
            description="test description",
            phasecode=PhaseCode.L1,
        ),
        Measurement(
            source=Source.HOMEWIZARD_P1,
            measurement_type=MeasurementType.VOLTAGE,
            value=230.0,
            description="test description",
            phasecode=PhaseCode.L2,
        ),
        Measurement(
            source=Source.HOMEWIZARD_P1,
            measurement_type=MeasurementType.VOLTAGE,
            value=230.0,
            description="test description",
            phasecode=PhaseCode.L3,
        )
    ]

    adapter = BaseAdapter()
    adapter.update = AsyncMock(return_value=aggregated_measurements)
    return adapter


def test_get_aggregated_measurements(mock_adapter_1, mock_adapter_2):
    aggregated_measurements = get_aggregated_measurements([mock_adapter_1, mock_adapter_2])

    assert len(aggregated_measurements) == 4
