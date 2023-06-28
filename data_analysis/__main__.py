import datetime

import matplotlib.pyplot as plt
from tqdm import tqdm

from home_telemetry.database import get_measurements
from home_telemetry.models import MeasurementType, Source

if __name__ == "__main__":
    p1_power_measurements = get_measurements(
        measurement_type=MeasurementType.POWER, source=Source.HOMEWIZARD_P1, datetime_lte=datetime.datetime(2023, 6, 1)
    )
    solax_power_measurements = get_measurements(
        measurement_type=MeasurementType.POWER, source=Source.SOLAX, datetime_lte=datetime.datetime(2023, 6, 1)
    )

    timestamps_p1 = [measurement.timestamp for measurement in p1_power_measurements]
    values_p1 = [measurement.value for measurement in p1_power_measurements]

    values_p1_avg, timestamps_p1_avg, values_p1_undersampled, timestamps_p1_undersampled = [], [], [], []
    avg_values = []
    avg_timestamp = timestamps_p1[0]
    avg_period = datetime.timedelta(minutes=1)

    for measurement in tqdm(p1_power_measurements):
        if measurement.timestamp < avg_timestamp + avg_period:
            avg_values.append(measurement)
        else:
            values_p1_avg.append(sum([measurement.value for measurement in avg_values]) / len(avg_values))
            values_p1_undersampled.append(measurement.value)
            timestamps_p1_undersampled.append(measurement.timestamp)
            timestamps_p1_avg.append(avg_timestamp)
            avg_timestamp = measurement.timestamp
            avg_values = [measurement]

    timestamps_solax = [measurement.timestamp for measurement in solax_power_measurements]
    values_solax = [measurement.value for measurement in solax_power_measurements]

    # Create plot
    fig, ax = plt.subplots()
    ax.plot(timestamps_p1, values_p1)
    ax.plot(timestamps_p1_avg, values_p1_avg)
    ax.plot(timestamps_p1_undersampled, values_p1_undersampled)
    # ax.plot(timestamps_solax, values_solax)

    # Format plot
    ax.set_xlabel("Date")
    ax.set_ylabel("Value")
    ax.set_title("Time Series Plot")
    plt.xticks(rotation=45)
    plt.grid(True)

    # Display plot
    plt.show()
