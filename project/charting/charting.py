
def chartSystems(data):
    import numpy as np 
    from matplotlib import pyplot as plt #relies on tkinter

    x = np.arange(0,len(data)) 
    y = list(map(lambda x: x/100, data))
    plt.title("System grand total over time") 
    plt.xlabel("Time") 
    plt.ylabel("Grand total") 
    plt.plot(x,y)
    #ensure matplot lib uses full screen
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()

    plt.show() 