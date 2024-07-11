from plotting_utils import MyFigure, auto_plot_IV, auto_plot_cycles
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl


def autoplot(all_info, show=True, g_o=False, savefig=False):
    # function to automatically generate all runs I-V for the device
    fig = auto_plot_IV(all_info)
    figures = auto_plot_cycles(all_info)
    
    all_figs = [fig]
    all_figs.extend(figures)

    if g_o == True:
        for figure in all_figs:
            ax = figure.axs
            x = np.linspace(ax.get_xlim()[0], ax.get_xlim()[1], 1000)
            y = abs(x * 7.748 * (10**(-5)))
            ax.plot(x, y,'-.', color='magenta', label='G_o')
            ax.legend()
    if show == True:
        plt.show()

    if savefig == True:
        for figure in all_figs:
            figure.fig.savefig(mpl.rcParams["savefig.directory"] + '\\' + figure.fig.get_suptitle())

    return all_figs


def plot_info(all_info, show=True, g_o=False, savefig=False):

    # list of figures to be returned to the main script
    figures = []


    # sort all info into seperate info arrays by test type
    pristine_reads = []
    electroform = []
    resets = []
    sets = []
    reads = []
    for i in all_info:
        if i['type'] == 'pristine read':
            pristine_reads.append(i)
        elif i['type'] == 'form':
            electroform.append(i)
        elif i['type'] == 'reset':
            resets.append(i)  
        elif i['type'] == 'set':
            sets.append(i)  
        elif i['type'] == 'read':
            reads.append(i)
    
    
    # # alternative way to manually plot all runs I-V:
    fig = MyFigure(1, title='I-V')
    ax = fig.axs
    fig.plot_sweeps(ax, resets, color='blue', label='resets')
    fig.plot_sweeps(ax, sets, color='red', label='sets')
    fig.plot_sweeps(ax, electroform, color='black', label='electroform')
    ax.set_title('I-V')
    ax.legend()
    figures.append(figure)



    if g_o == True:
        for figure in figures:
            ax = figure.axs
            x = np.linspace(ax.get_xlim()[0], ax.get_xlim()[1], 1000)
            y = abs(x * 7.748 * (10**(-5)))
            ax.plot(x, y,'-.', color='magenta', label='G_o')
            ax.legend()

    if savefig == True:
        for figure in figures:
            figure.fig.savefig(mpl.rcParams["savefig.directory"] + '\\' + figure.fig.get_suptitle())

    # leave these in
    if show == True:
        plt.show()

    return figures