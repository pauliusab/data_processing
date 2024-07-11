# name of project and site as defined in Clarius
# note: subsite, device, test and run is read and sorted automatically
project = 'Yiming_2'
site = 'Site@1'


# names of columns as defined in Clarius
resistance_column = 'RES'
I_sweep_column = 'AI'
V_sweep_column = 'AV'
I_read_column = 'AI'
V_read_column = 'AV'


# list of parameters to be saved from .xls files to .pickle
parameter_list = ["Last Executed", "Device Terminal",
                  "Mode", "Operation Mode", "Bias",
                  "Start/Bias", "Stop", "Step", "Compliance"]


# size of figures (2x for 2-graph)
figure_size = 7