import matplotlib.pyplot as plt


from datetime import datetime
from data_analysis.plotting import display_plot
from home_telemetry.database import get_measurements
from home_telemetry.models import MeasurementType, PhaseCode, Source


def voltage():
    p1_voltage_measurements_l1 = get_measurements(
        measurement_type=MeasurementType.VOLTAGE,
        source=Source.HOMEWIZARD_P1,
        datetime_gte=datetime(2023, 12, 23),
        phase_code=PhaseCode.L1
    )

    p1_voltage_measurements_l2 = get_measurements(
        measurement_type=MeasurementType.VOLTAGE,
        source=Source.HOMEWIZARD_P1,
        datetime_gte=datetime(2023, 12, 23),
        phase_code=PhaseCode.L2
    )

    p1_voltage_measurements_l3 = get_measurements(
        measurement_type=MeasurementType.VOLTAGE,
        source=Source.HOMEWIZARD_P1,
        datetime_gte=datetime(2023, 12, 23),
        phase_code=PhaseCode.L3
    )

    timestamps = [measurement.timestamp for measurement in p1_voltage_measurements_l1]
    values_l1 = [measurement.value for measurement in p1_voltage_measurements_l1]
    values_l2 = [measurement.value for measurement in p1_voltage_measurements_l2]
    values_l3 = [measurement.value for measurement in p1_voltage_measurements_l3]

    # Create plot
    fig, ax = plt.subplots()
    ax.plot(timestamps, values_l1, label="Voltage L1")
    # ax.plot(timestamps, values_l2, label="Voltage L2")
    # ax.plot(timestamps, values_l3, label="Voltage L3")

    display_plot(ax)
