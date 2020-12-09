import numpy as np
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
from matplotlib import pyplot  # relies on tkinter
# Dates is an array/list of string representation of dates that correspond with the data
# Data is an array/list of the data to be plotted

def chartData(data, dates = None):
    max = len(data) - 1
    #formats the x axis labels based on x positions, thus enabling coherent labels even when really zoomed in
    def format_date(x, pos=None):
        xlocation = np.clip(int(x + 0.5), 0, max) #clip the index somewhere between 0 and the max viable index
        return dates[xlocation]

    x = range(0, len(data))
    y = list(map(lambda x: x/100, data))
    fig, ax1 = pyplot.subplots(1, 1)
    ax1.plot(x, y)
    ax1.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))

    ax1.set_xlabel('Time')
    ax1.set_ylabel('Grand Total')
    ax1.set_title('Grand Total over time')
    fig.autofmt_xdate()

    for ax in fig.axes:
        pyplot.sca(ax)
        pyplot.xticks(rotation=90)

    pyplot.draw()
    pyplot.show()