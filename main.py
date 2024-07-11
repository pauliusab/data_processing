import settings
import utils
import data_processing
import plot_script
import plotting_utils
import os
import matplotlib.pyplot as plt
import utils
import sys


# get this file directory to use for reference further
home_path = os.path.dirname(__file__)


# create Data and Dump folders or ignore
utils.initialize_folders(home_path)
# check dump for files and sort them out
data_processing.sort_dump()
#data_processing.refresh_dfolders()


# user-defined input for plotting
chip = 'UCL127'
device = 'B6_S_A4'





if device not in os.listdir(home_path + "\\Data\\" + chip):
    print('there is no such device')
    sys.exit()

# path to the user-defined device folder
folder_path = home_path + "\\Data\\" + chip + '\\' + device

# make the default graph save directory the current device graphs folder
utils.set_savedir(folder_path)



# # load info from excel files (gives a lot of warnings but they can be ignored)
# # comment out if loading pickle file
# all_info = data_processing.get_all_info(folder_path, save=True)       # remove save=True if you don't want to save data into .pickle file

# open data file (.pickle) and load it into all_info to use in plotting
all_info = utils.open_info(folder_path)

# # heres a way to remove unwanted runs
# forms = list(filter(lambda x: x['type'] == 'form', all_info))
# form2 = list(filter(lambda x: x['nr'] != 1, forms))
# all_info = list(filter(lambda x: x['type'] != 'form', all_info))
# all_info.extend(form2)


# print a list of performed tests in chronological order
utils.print_chrono(all_info)


# # get parameters and data for a specific run
# params = utils.get_run_parameters(all_info, 'set', 1)
# data = utils.get_run_data(all_info, 'set', 1)
# print('\n Data in set 1')
# print(data)
# print('\n Set 1 parameters:')
# print(params)


# automatically plot I-V and cycles
figures = plot_script.autoplot(all_info,
                                g_o=True,           # includes G_o level in figures
                                savefig=True,       # saves figures as .png in device/Figures folder
                                show=True)          # add show=False if don't want to show the graphs (e.g. when just want to save as .png)

# # run custom plot script
# figures = plot_script.plot_info(all_info,
#                                 g_o=True,
#                                 savefig=True,
#                                 show=False)


# # save plotting data for figures plotted (like which runs were used to generate the graph and their full data)
# utils.save_figures_info(folder_path, figures)


# # print runs that were used in figures
# load_info = utils.get_figures_info(folder_path, name='autoplot', print_info=True)
# print(load_info)
