import matplotlib.pyplot as plt


def display_plot(ax):
    ax.set_xlabel("Date")
    ax.set_ylabel("Value")
    ax.set_title("Time Series Plot")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()

    plt.show()  # Display plot
