import matplotlib.pyplot as plt

from database import get_measurements
from models import MeasurementType, Source

if __name__ == "__main__":
    p1_power_measurements = get_measurements(measurement_type=MeasurementType.POWER, source=Source.HOMEWIZARD_P1)
    solax_power_measurements = get_measurements(measurement_type=MeasurementType.POWER, source=Source.SOLAX)

    timestamps_p1 = [measurement.timestamp for measurement in p1_power_measurements]
    values_p1 = [measurement.value for measurement in p1_power_measurements]

    timestamps_solax = [measurement.timestamp for measurement in solax_power_measurements]
    values_solax = [measurement.value for measurement in solax_power_measurements]

    # Create plot
    fig, ax = plt.subplots()
    ax.plot(timestamps_p1, values_p1)
    ax.plot(timestamps_solax, values_solax)

    # Format plot
    ax.set_xlabel('Date')
    ax.set_ylabel('Value')
    ax.set_title('Time Series Plot')
    plt.xticks(rotation=45)
    plt.grid(True)

    # Display plot
    plt.show()
