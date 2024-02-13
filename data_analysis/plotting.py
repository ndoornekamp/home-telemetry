import matplotlib.pyplot as plt
from matplotlib.axes import Axes


def display_plot(ax: Axes) -> None:
    ax.set_xlabel("Date")
    ax.set_ylabel("Value")
    ax.set_title("Time Series Plot")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()

    plt.show()  # Display plot
