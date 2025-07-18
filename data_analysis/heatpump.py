from datetime import datetime

import matplotlib.pyplot as plt

from data_analysis.plotting import display_plot
from home_telemetry.database import get_measurements
from home_telemetry.models import MeasurementType, Source


def heatpump_analysis() -> None:
    heatpump_flow_measurements = get_measurements(
        measurement_type=MeasurementType.FLOW,
        source=Source.HEISHAMON,
        datetime_gte=datetime(2024, 9, 23),
    )
    heatpump_main_inlet_measurements = get_measurements(
        measurement_type=MeasurementType.TEMPERATURE,
        source=Source.HEISHAMON,
        description="Main inlet",
        datetime_gte=datetime(2024, 9, 23),
    )
    heatpump_main_outlet_measurements = get_measurements(
        measurement_type=MeasurementType.TEMPERATURE,
        source=Source.HEISHAMON,
        description="Main outlet",
        datetime_gte=datetime(2024, 9, 23),
    )
    heatpump_main_target = get_measurements(
        measurement_type=MeasurementType.TEMPERATURE,
        source=Source.HEISHAMON,
        description="Main target",
        datetime_gte=datetime(2024, 9, 23),
    )
    dhw_target = get_measurements(
        measurement_type=MeasurementType.TEMPERATURE,
        source=Source.HEISHAMON,
        description="DHW target",
        datetime_gte=datetime(2024, 9, 23),
    )
    dhw_actual = get_measurements(
        measurement_type=MeasurementType.TEMPERATURE,
        source=Source.HEISHAMON,
        description="DHW actual",
        datetime_gte=datetime(2024, 9, 23),
    )

    timestamps_heatpump = [measurement.timestamp for measurement in heatpump_flow_measurements]
    values_heatpump_flow = [measurement.value for measurement in heatpump_flow_measurements]
    values_heatpump_inlet = [measurement.value for measurement in heatpump_main_inlet_measurements]
    values_heatpump_outlet = [measurement.value for measurement in heatpump_main_outlet_measurements]
    values_heatpump_target = [measurement.value for measurement in heatpump_main_target]
    values_dhw_target = [measurement.value for measurement in dhw_target]
    values_dhw_actual = [measurement.value for measurement in dhw_actual]

    fig, ax = plt.subplots()

    ax.plot(timestamps_heatpump, values_heatpump_flow, label="Heatpump flow", color="orange")
    ax.plot(timestamps_heatpump, values_heatpump_inlet, label="Heatpump inlet temperature", color="red")
    ax.plot(timestamps_heatpump, values_heatpump_outlet, label="Heatpump outlet temperature", color="purple")
    ax.plot(timestamps_heatpump, values_heatpump_target, label="Heatpump target temperature", color="green")
    ax.plot(timestamps_heatpump, values_dhw_target, label="DHW target temperature", color="blue")
    ax.plot(timestamps_heatpump, values_dhw_actual, label="DHW actual temperature", color="black")

    display_plot(ax)
