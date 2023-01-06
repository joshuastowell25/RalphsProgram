import matplotlib
import numpy as np
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
from matplotlib import pyplot  # relies on tkinter
# Dates is an array/list of string representation of dates that correspond with the data
# Data is an array/list of the data to be plotted

def chartData(stockdata, gtdata, dates = None):
    max = len(stockdata) - 1
    #formats the x axis labels based on x positions, thus enabling coherent labels even when really zoomed in
    def format_date(x, pos=None):
        xlocation = np.clip(int(x + 0.5), 0, max) #clip the index somewhere between 0 and the max viable index
        return dates[xlocation]

    x = range(0, len(stockdata))
    fig, ax1 = pyplot.subplots(1, 1) #how many rows and columns of charts you want to display
    ax1.plot(x, stockdata, color="black")
    ax1.plot(x, gtdata, color="green")
    ax1.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))

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