# name of project and site as defined in Clarius
# note: subsite, device, test and run is read and sorted automatically
project = 'Paulius'
site = 'try1@1'


# names of columns as defined in Clarius
resistance_collumn = 'RES'
I_sweep_column = 'I'
V_sweep_column = 'V'


# list of parameters to be saved from .xls files to .pickle
parameter_list = ["Last Executed", "Device Terminal",
                  "Mode", "Operation Mode", "Bias",
                  "Start/Bias", "Stop", "Step", "Compliance"]


# size of figures (2x for 2-graph)
figure_size = 7