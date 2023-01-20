import matplotlib
import numpy as np
import matplotlib.ticker as ticker
from matplotlib import pyplot  # relies on tkinter

from domain import System


# Dates is an array/list of string representation of dates that correspond with the data
# Data is an array/list of the data to be plotted

def chartSystem(system: System):
    datapoints = system.datapoints
    #formats the x axis labels based on x positions, thus enabling coherent labels even when really zoomed in
    def format_date(x, pos=None):
        xlocation = np.clip(int(x + 0.5), 0, len(datapoints)-1) #clip the index somewhere between 0 and the max viable index
        return datapoints[xlocation].datetime

    x = range(0, len(datapoints))
    y = [datapoint.price for datapoint in datapoints]
    np.polyfit(x, y, deg=1)

    #figure out a polynomial function that fits the earnings best. Then see how far the data deviate from it as a measure of accuracy
    m, b = np.polyfit(x, system.stats.runningGt, deg=1)

    priceData = [datapoint.price for datapoint in datapoints]
    fig, ax1 = pyplot.subplots(1, 1) #how many rows and columns of charts you want to display
    ax1.plot(x, [datapoint.price for datapoint in datapoints], color="black")
    ax1.plot(x, system.stats.runningGt, color="green")
    ax1.plot(x, [m*item for item in x], color="red")
    #ax1.plot(x, system.stats.running30IncVariance, color="red")
    ax1.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))

    ymax=max(int(max(system.stats.runningGt)), int(max(priceData)))
    ymin= min(int(min(system.stats.runningGt)), int(min(priceData)))
    pyplot.ylim(ymax=ymax, ymin=ymin)

    ax1.set_xlabel('Time')
    ax1.set_ylabel('Grand Total')
    ax1.set_title('Grand Total over time')
    fig.autofmt_xdate()

    #This code rotates some of the axis labels
    #for ax in fig.axes:
    #    pyplot.sca(ax)
    #    pyplot.xticks(rotation=90)

    #pyplot.get_current_fig_manager().full_screen_toggle()  # toggle fullscreen mode

    #the way you maximize the plot depends on the matplotlib backend that's installed
    backend = matplotlib.get_backend()
    print("Matplotlib backend: "+backend+"\n")

    if(backend == "TkAgg"):
        manager = pyplot.get_current_fig_manager()
        manager.resize(*manager.window.maxsize())
    elif(backend == "WX"):
        manager = pyplot.get_current_fig_manager()
        manager.frame.Maximize(True)
    elif(backend == "QT"):
        manager = pyplot.get_current_fig_manager()
        manager.window.showMaximized()
    else:
        print("Unrecognized matplotlib backend: "+backend)

    pyplot.draw()
    pyplot.show()