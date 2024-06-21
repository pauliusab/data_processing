from plotting_utils import MyFigure, auto_plot_IV
import matplotlib.pyplot as plt


def plot_info(all_info, auto=False, show=True):

    
    if auto == True:
        # function to automatically generate all runs I-V for the device
        fig = auto_plot_IV(all_info)
        if show == True:
            plt.show()
        return([fig])

    # list of figures to be returned to the main script
    figures = []


    # sort all info into seperate info arrays by test type
    resets = list(filter(lambda x: x['type'] == 'reset', all_info))
    electroform = list(filter(lambda x: x['type'] == 'form', all_info))
    sets = list(filter(lambda x: x['type'] == 'set', all_info))
    reads = list(filter(lambda x: x['type'] == 'read', all_info))
    
    # sort reads by their run number
    reads = sorted(reads, key=lambda x: int(x['nr']))


    # remove unwanted elements
    sets = list(filter(lambda x: x['nr'] not in [57], sets))
    resets = list(filter(lambda x: x['nr'] not in [55], resets))


    

    # alternative way to manually plot all runs I-V:
    fig = MyFigure(1, title='I-V')
    ax = fig.axs
    fig.plot_sweeps(ax, resets, color='blue')
    fig.plot_sweeps(ax, sets, color='red')
    fig.plot_sweeps(ax, electroform, color='black')
    figures.append(fig)



    # example of reset sequence plot
    reset_seq1 = list(filter(lambda x: x['nr'] <= 45, resets))
    set1 = list(filter(lambda x: x['nr'] == 1, sets))       # alternatively, if the sets list is sorted, write: set1 = [sets[0]]
    read1 = list(filter(lambda x: x['nr'] == 1, reads))
    read2 = list(filter(lambda x: x['nr'] == 4, reads))

    fig = MyFigure(2, title='reset sequence 1')
    ax = fig.axs
    ax[0].set_title('I-V')
    fig.plot_sweeps(ax[0], [electroform[-1]], color='grey', label='previous set')
    fig.plot_sweeps(ax[0], reset_seq1)
    fig.plot_sweeps(ax[0], set1, color='black', label='subsequent_set')
    # to show legend:
    ax[0].legend()
    
    ax[1].set_title('DC read')
    fig.plot_res(ax[1], read1, label='set resistance')
    fig.plot_res(ax[1], read2, label='reset resistance')
    ax[1].legend()
    figures.append(fig)




    # leave these in
    if show == True:
        plt.show()

    return figures