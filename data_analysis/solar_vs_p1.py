from datetime import datetime

import matplotlib.pyplot as plt

from data_analysis.plotting import display_plot
from home_telemetry.database import get_measurements
from home_telemetry.models import MeasurementType, Source


def solar_vs_p1() -> None:
    p1_power_measurements = get_measurements(
        measurement_type=MeasurementType.POWER,
        source=Source.HOMEWIZARD_P1,
        datetime_gte=datetime(2024, 9, 23),
    )
    solax_power_measurements = get_measurements(
        measurement_type=MeasurementType.POWER,
        source=Source.SOLAX,
        datetime_gte=datetime(2024, 9, 23),
    )

    timestamps_p1 = [measurement.timestamp for measurement in p1_power_measurements]
    values_p1 = [measurement.value for measurement in p1_power_measurements]

    timestamps_solax = [measurement.timestamp for measurement in solax_power_measurements]
    values_solax = [measurement.value for measurement in solax_power_measurements]

    # Create plot
    fig, ax = plt.subplots()
    ax.plot(timestamps_solax, values_solax, label="Solar power")
    ax.plot(timestamps_p1, values_p1, label="P1 net power")

    display_plot(ax)
