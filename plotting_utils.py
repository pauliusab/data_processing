import matplotlib.pyplot as plt
import matplotlib
import settings
import pickle


r_col = settings.resistance_column
i_sw_col = settings.I_sweep_column
v_sw_col = settings.V_sweep_column
i_r_col = settings.I_read_column
v_r_col = settings.V_read_column

def auto_plot_IV(all_info):
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
    
    fig = MyFigure(1, title='I-V')
    ax = fig.axs

    if (len(resets) == 0) and (len(sets) == 0) and (len(electroform) == 0):
        pristine_read = list(filter(lambda x: x['type'] == 'pristine read', all_info))
        fig.plot_I(ax, pristine_read, test_type='read' ,color='black')
        ax.set_title('pristine read')
    else:
        fig.plot_sweeps(ax, resets, color='blue')
        fig.plot_sweeps(ax, sets, color='red')
        fig.plot_sweeps(ax, electroform, color='black')
        ax.set_title('I-V')

    return fig




def auto_plot_cycles(all_info):
    time_sort = sorted(all_info, key=lambda x: x['time'])
    cycles = []
    cycle = []
    cycle_overlap = []
    n_change = 0
    for run in time_sort:
        type = run['type']
        if len(cycle) > 1:
            if type not in ['read', 'pristine read']:
                try:
                    previous_type = previous_run['type']
                    if previous_type == 'form':
                        previous_type = 'set'
                    if type != previous_type:
                        n_change += 1
                    if n_change == 2:
                        cycle_overlap.append(run)
                    if n_change == 3:
                        cycles.append(cycle)
                        cycle = cycle_overlap
                        cycle_overlap = []
                        n_change = 1
                except UnboundLocalError:
                    pass

        cycle.append(run)
        if type not in ['read', 'pristine read']:
            previous_run = run

    cycles.append(cycle)


    figures = []
    cycles_reads = []
    for c in range(len(cycles)):

        cycle_info = cycles[c]
        resets = []
        sets_before = []
        sets_after = []
        forms = []
        first_read = None
        last_read = None
        change = False

        for i in cycle_info:

            if i['type'] == 'reset':
                change = True
                resets.append(i)  
            elif i['type'] == 'set':
                if change == False:
                    sets_before.append(i)
                else:
                    sets_after.append(i)
            elif i['type'] == 'form':
                forms.append(i)
            elif i['type'] == 'read':
                if first_read == None:
                    first_read = i
                else:
                    last_read = i

        if first_read != None:
            cycles_reads.append(first_read)
        if last_read != None:
            cycles_reads.append(last_read)


        fig = MyFigure(1, title='Cycle nr ' + str(c+1))
        ax = fig.axs

        fig.plot_sweeps(ax, resets)
        if len(forms) > 0:
            fig.plot_sweeps(ax, forms, color='gray', label='electroform')
        else:
            fig.plot_sweeps(ax, sets_before, color='gray', label='previous set')
        fig.plot_sweeps(ax, sets_after, color='black', label='subsequent set')
        #ax.set_title('Cycle nr ' + str(c+1))
        ax.legend()
        figures.append(fig)
    
    # # plots reads
    # if len(cycles_reads) > 0:
    #     fig = MyFigure(1, title='Read and retention')
    #     ax = fig.axs
    #     fig.plot_I(ax, cycles_reads, test_type='read', show_legend=True)
    #     ax.set_title('@ 20mV DC bias')
    #     figures.append(fig)

    return figures








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
        test_type = kwargs.get('test_type', 'sweep')   
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
        test_type = kwargs.get('test_type', 'sweep')
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
                if test_type == 'sweep':
                    ax.plot(df[i_sw_col], color=color, label=label)
                elif test_type == 'read':
                    ax.plot(df[i_r_col], color=color, label=label)
                ax.set_xlabel("step nr")
            else:
                if test_type == 'sweep':
                    ax.plot(df['Time'], df[i_sw_col], color=color, label=label)
                elif test_type == 'read':
                    ax.plot(df['Time'], df[i_r_col], color=color, label=label)
                ax.set_xlabel("Time (s)")

        if show_legend == True:
            ax.legend(legend)
        
        for i in self.data:
            if  i['ax'] == ax:
                i['data'].extend(data)


    def plot_sweeps(self, ax, data, **kwargs):
        test_type = kwargs.get('test_type', 'sweep')
        color = kwargs.get('color', None)
        show_legend = kwargs.get('show_legend', False)
        yscale = kwargs.get('yscale', None)
        if yscale != None:
            ax.set_yscale(yscale)
        label = kwargs.get('label', None)
        linestyle = kwargs.get('linestyle', '-')

        ax.set_xlabel("Voltage (V)")
        ax.set_ylabel("Current (A)")
        auto_legend = []

        label_applied = False
        for i in data:
            df = i['data']
            run = i['nr']
            auto_legend.append(run)
            if test_type == 'sweep':
                if (label_applied == False) or (show_legend == True):
                    ax.plot(df[v_sw_col], abs(df[i_sw_col]), linestyle, color=color, label=label)
                    label_applied = True
                else:
                    ax.plot(df[v_sw_col], abs(df[i_sw_col]), linestyle, color=color)
            elif test_type == 'read':
                if (label_applied == False) or (show_legend == True):
                    ax.plot(df[v_r_col], abs(df[i_r_col]), linestyle, color=color, label=label)
                    label_applied = True
                else:
                    ax.plot(df[v_r_col], abs(df[i_r_col]), linestyle, color=color)

        if show_legend == True:
            ax.legend(auto_legend)

        for i in self.data:
            if i['ax'] == ax:
                i['data'].extend(data)
