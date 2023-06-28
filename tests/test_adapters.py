from collections import defaultdict

import pytest

from home_telemetry.adapters import BaseAdapter
from home_telemetry.models import Measurement, MeasurementType, PhaseCode


@pytest.mark.parametrize(
    "measurements,cache_expected",
    [
        (
            [
                Measurement(
                    value=1,
                    measurement_type=MeasurementType.VOLTAGE,
                    phasecode=PhaseCode.ALL,
                    description="Test description",
                )
            ],
            {MeasurementType.VOLTAGE: {PhaseCode.ALL: {"Test description": [1]}}},
        ),
        (
            [
                Measurement(
                    value=1,
                    measurement_type=MeasurementType.VOLTAGE,
                    phasecode=PhaseCode.ALL,
                    description="Test description",
                ),
                Measurement(
                    value=2,
                    measurement_type=MeasurementType.VOLTAGE,
                    phasecode=PhaseCode.ALL,
                    description="Test description",
                ),
            ],
            {MeasurementType.VOLTAGE: {PhaseCode.ALL: {"Test description": [1, 2]}}},
        ),
        (
            [
                Measurement(
                    value=1,
                    measurement_type=MeasurementType.VOLTAGE,
                    phasecode=PhaseCode.ALL,
                    description="Test description",
                ),
                Measurement(
                    value=2,
                    measurement_type=MeasurementType.VOLTAGE,
                    phasecode=PhaseCode.ALL,
                    description="Some other test description",
                ),
            ],
            {MeasurementType.VOLTAGE: {PhaseCode.ALL: {"Test description": [1], "Some other test description": [2]}}},
        ),
        (
            [
                Measurement(
                    value=1,
                    measurement_type=MeasurementType.POWER,
                    phasecode=PhaseCode.ALL,
                    description="Test description",
                ),
                Measurement(
                    value=2,
                    measurement_type=MeasurementType.VOLTAGE,
                    phasecode=PhaseCode.ALL,
                    description="Test description",
                ),
            ],
            {
                MeasurementType.POWER: {PhaseCode.ALL: {"Test description": [1]}},
                MeasurementType.VOLTAGE: {PhaseCode.ALL: {"Test description": [2]}},
            },
        ),
    ],
)
def test_adapter_cache(measurements: list[Measurement], cache_expected):
    adapter = BaseAdapter()

    adapter.aggregate(measurements)

    assert adapter.aggregation_cache == cache_expected


def test_adapter_aggregation():
    adapter = BaseAdapter()
    adapter.source = None
    adapter.aggregation_cache = {
        MeasurementType.POWER: {PhaseCode.ALL: {"Test description": [1]}},
        MeasurementType.VOLTAGE: {PhaseCode.ALL: {"Test description": [2, 4]}},
    }
    adapter.aggregation_period_seconds = 0  # To force aggregation on every call

    aggregated_measurements = adapter.aggregate([])
    assert aggregated_measurements == [
        Measurement(
            measurement_type=MeasurementType.POWER,
            phasecode=PhaseCode.ALL,
            description="Test description",
            value=1,
        ),
        Measurement(
            measurement_type=MeasurementType.VOLTAGE,
            phasecode=PhaseCode.ALL,
            description="Test description",
            value=3,
        ),
    ]
    assert adapter.aggregation_cache == defaultdict(defaultdict(defaultdict(list).copy).copy), "Cache should be cleared"
