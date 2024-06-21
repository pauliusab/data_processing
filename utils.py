import matplotlib.pyplot as plt
import matplotlib as mpl 
import pandas as pd
import os
from datetime import datetime
import pickle
import shutil
from copy import copy


def initialize_folders(home_path):
    try:
        os.makedirs(home_path + '\Data')
    except FileExistsError:
        pass
    
    try:
        os.makedirs(home_path + '\Dump')
    except FileExistsError:
        pass

# make the default graph save directory the current device graphs folder
def set_savedir(folder_path):
    try:
        os.makedirs(folder_path + '\\Figures')
    except FileExistsError:
        pass
    mpl.rcParams["savefig.directory"] = folder_path + '\\Figures'

# open data file (.pickle) and load it into all_info to use in plotting
def open_info(folder_path):
    with open(folder_path + '\\Pickles\\info_file.pickle', 'rb') as f:
        return pickle.load(f)


# get a list of performed tests in chronological order
def print_chrono(all_info):
    time_sort = sorted(all_info, key=lambda x: x['time'])
    chrono_list = [i['type'] + ' ' + str(i['nr']) for i in time_sort]
    print('\n')
    print('Chronological order:')
    print(chrono_list)


def save_figures_info(folder_path, figures):
    for figure in figures:
        figname = figure.fig.get_suptitle()
        with open(folder_path + '\\Pickles\\' + figname + '_datafile.pickle', 'wb') as f:
            pickle.dump(figure.data, f, protocol=pickle.HIGHEST_PROTOCOL)


def load_data(dir):
        with open(dir, 'rb') as f:
            data = pickle.load(f)
            return data 
        
# print runs that were used in figures
def get_figures_info(folder_path, name=None, print_info=True):
    all_filenames = os.listdir(folder_path + '\\Pickles')
    all_save_files = list(filter(lambda x: 'datafile.pickle' in x, all_filenames))

    if name != None:
        if '_datafile.pickle' not in name:
            all_save_files = list(filter(lambda x: x == (name + '_datafile.pickle'), all_save_files))
        else:
            print('\n')
            print('Enter the figure name without "_datafile.pickle"')

    all_info = []
    for filename in all_save_files:
        data = load_data(folder_path + '\\Pickles\\' + filename)
        print('\n')
        figure_name = filename.removesuffix('_datafile.pickle')
        if print_info == True: print('Figure:  ' + figure_name)
        axs_info = []
        for d in data:
            if print_info == True:
                print('data in graph ' + d['ax'].get_title() + ':')
                print([i['type'] + ' ' + str(i['nr']) for i in d['data']])
            axs_info.append({'ax': d['ax'].get_title(), 'data':[i['type'] + ' ' + str(i['nr']) for i in d['data']]})
        all_info.append({'figure': figure_name, 'graphs': axs_info})

    return all_info


def get_run_parameters(all_info, run_type, run_nr, print_info=True):
    run = list(filter(lambda x: x['type']==run_type and x['nr']==run_nr, all_info))
    if len(run) != 0:
        if print_info == True:
            print('\n')
            print('Parameters for ' + run_type + ' ' + str(run_nr) + ':')
            print(run[0]['parameters'])
        return run[0]['parameters']
    else:
        print('run could not be found')
        return None


def get_run_data(all_info, run_type, run_nr):
    run = list(filter(lambda x: x['type']==run_type and x['nr']==run_nr, all_info))
    if len(run) != 0:
        return run[0]['data']
    else:
        print('run could not be found')
        return None