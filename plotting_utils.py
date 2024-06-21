import matplotlib.pyplot as plt
import matplotlib
import settings
import pickle


r_col = settings.resistance_collumn
i_col = settings.I_sweep_column
v_col = settings.V_sweep_column


def auto_plot_IV(all_info):
    resets = list(filter(lambda x: x['type'] == 'reset', all_info))
    electroform = list(filter(lambda x: x['type'] == 'form', all_info))
    sets = list(filter(lambda x: x['type'] == 'set', all_info))
    
    fig = MyFigure(1, title='autoplot')
    ax = fig.axs

    if (len(resets) == 0) and (len(resets) == 0) and (len(resets) == 0):
        pristine_read = list(filter(lambda x: x['type'] == 'pristine read', all_info))
        fig.plot_res(ax, pristine_read, color='black')
        ax.set_title('pristine read')
    else:
        fig.plot_sweeps(ax, resets, color='blue')
        fig.plot_sweeps(ax, sets, color='red')
        fig.plot_sweeps(ax, electroform, color='black')
        ax.set_title('I-V')

    return fig





class MyFigure:

    def __init__(self, nr_plots, **kwargs):
        self.fig = None
        self.axs = []
        self.data = []
        self.yscale = 'linear'
        title = kwargs.get('title', None)
        size = settings.figure_size
        if nr_plots == 1:
            self.fig, self.axs = plt.subplots(figsize=(size, size))
            if title != None:
                self.fig.suptitle(title, fontsize=16)
                self.fig.canvas.manager.set_window_title(title)

        elif  nr_plots == 2:
            self.fig, self.axs = plt.subplots(1,2, figsize=(2*size, size))
            self.fig.subplots_adjust(left=0.075, right=0.95, top=0.85, wspace=0.3)
            if title != None:
                self.fig.suptitle(title, x=0.525, fontsize=16)
                self.fig.canvas.manager.set_window_title(title)
        else:
            print('nr plots should be 1 or 2')

        try:
            for ax in self.axs:
                self.data.append({'ax':ax, 'data':[]})
                ax.grid()
                ax.set_yscale('log')
                ax.minorticks_on()
        except TypeError:
            self.data.append({'ax':self.axs, 'data':[]})
            self.axs.grid()
            self.axs.set_yscale('log')
            self.axs.minorticks_on()


    def plot_res(self, ax, data, **kwargs):   
        color = kwargs.get('color', None)
        show_legend = kwargs.get('show_legend', False)
        step_graph = kwargs.get('step_graph', False)
        yscale = kwargs.get('yscale', None)
        if yscale != None:
            ax.set_yscale(yscale)
        label = kwargs.get('label', None)

        ax.set_ylabel("Resistance (Ohms)")
        legend = []

        for i in data:
            df = i['data']
            run = i['nr']
            legend.append(run)

            if step_graph:
                ax.plot(df[r_col], color=color, label=label)
                ax.set_xlabel("step nr")
            else:
                ax.plot(df['Time'], df[r_col], color=color, label=label)
                ax.set_xlabel("Time (s)")

        if show_legend == True:
            ax.legend(legend)

        for i in self.data:
            if  i['ax'] == ax:
                i['data'].extend(data)
   

    def plot_I(self, ax, data, **kwargs):   
        color = kwargs.get('color', None)
        show_legend = kwargs.get('show_legend', False)
        step_graph = kwargs.get('step_graph', False)
        yscale = kwargs.get('yscale', None)
        if yscale != None:
            ax.set_yscale(yscale)
        label = kwargs.get('label', None)

        ax.set_ylabel("Current (A)")

        legend = []

        for i in data:
            df = i['data']
            run = i['nr']
            legend.append(run)

            if step_graph:
                ax.plot(df[i_col], color=color, label=label)
                ax.set_xlabel("step nr")
            else:
                ax.plot(df['Time'], df[i_col], color=color, label=label)
                ax.set_xlabel("Time (s)")

        if show_legend == True:
            ax.legend(legend)
        
        for i in self.data:
            if  i['ax'] == ax:
                i['data'].extend(data)


    def plot_sweeps(self, ax, data, **kwargs):

        color = kwargs.get('color', None)
        show_legend = kwargs.get('show_legend', False)
        yscale = kwargs.get('yscale', None)
        if yscale != None:
            ax.set_yscale(yscale)
        label = kwargs.get('label', None)

        ax.set_xlabel("Voltage (V)")
        ax.set_ylabel("Current (A)")
        auto_legend = []


        for i in data:
            df = i['data']
            run = i['nr']
            auto_legend.append(run)
            ax.plot(df[v_col], abs(df[i_col]), color=color, label=label)

        if show_legend == True:
            ax.legend(auto_legend)

        for i in self.data:
            if i['ax'] == ax:
                i['data'].extend(data)
