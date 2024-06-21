import settings
import utils
import data_processing
import plot_script
import plotting_utils
import os
import matplotlib.pyplot as plt
import utils
# from utils import get_figures_info, save_figures_info


# get this file directory to use for reference further
home_path = os.path.dirname(__file__)


# create Data and Dump folders or ignore
utils.initialize_folders(home_path)
# check dump for files and sort them out
data_processing.sort_dump()


# user-defined input for plotting
chip = 'UCL112'
device = 'G5s_5_9'



# path to the user-defined device folder
folder_path = home_path + "\\Data\\" + chip + '\\' + device

# make the default graph save directory the current device graphs folder
utils.set_savedir(folder_path)



# load info from excel files (gives a lot of warnings but they can be ignored)
# comment out if loading pickle file
# all_info = data_processing.get_all_info(folder_path, save=True)       # remove save=True if you don't want to save data into .pickle file

# open data file (.pickle) and load it into all_info to use in plotting
all_info = utils.open_info(folder_path)

# print a list of performed tests in chronological order
utils.print_chrono(all_info)

# get parameters and dataa for a specific run
params = utils.get_run_parameters(all_info, 'set', 1)
data = utils.get_run_data(all_info, 'set', 1)
print('\n Data in set 1')
print(data)

# # run plotting script
auto_figure = plot_script.plot_info(all_info, auto=True)       # add show=False if don't want to show the graphs
figures = plot_script.plot_info(all_info)

# save plotting data for figures plotted using plot_info()
utils.save_figures_info(folder_path, figures)



# print runs that were used in figures
load_info = utils.get_figures_info(folder_path, name='reset sequence 1', print_info=True)
print(load_info)
