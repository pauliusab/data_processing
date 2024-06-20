import matplotlib.pyplot as plt
import matplotlib as mpl 
import pandas as pd
import os
from datetime import datetime
import pickle
import shutil
import settings


home_path = os.path.dirname(__file__)

def update_folders(destinations):

    for dest in destinations:
        if 'be_test' not in dest:
            print(dest)
            try:
                os.makedirs(dest + '\\Figures')
            except FileExistsError:
                pass
            
            try:
                os.makedirs(dest + '\\Pickles')
            except FileExistsError:
                pass


            info = get_all_info(dest)
            with open(dest + '\\Pickles\\info_file.pickle', 'wb') as f:
                pickle.dump(info, f, protocol=pickle.HIGHEST_PROTOCOL)


def sort_dump():
    dump_dir = home_path + '\Dump'
    all_dump_files = os.listdir(dump_dir)

    all_destinations = set({})

    for filename in all_dump_files:
        # get the run name
        char_list = [*filename]
        word_list = []
        word = []
        for char in char_list:
            if char == " ":
                word_list.append(word)
                word = []
            else:
                word.extend(char)

        # make lists of chars to list of strings
        for i in range(len(word_list)):
            word_list[i] = ''.join(word_list[i])

        project = word_list[0]
        site = word_list[1]
        subsite = word_list[2]
        device = word_list[3]
        test = word_list[4]

        this_folder = home_path + '\Data' + '\\' + subsite + '\\' + device
        destination = this_folder + '\\Excel_files'
        try:
            os.makedirs(destination)
        except FileExistsError:
            pass
        source = dump_dir + '\\' + filename
        try:
            shutil.move(source, destination)  # include , copy_function=copy2 to copy (copy2=including metadata) instead of moving
            all_destinations.add(this_folder)
        except shutil.Error:
            os.remove(source)
            print('file ' + filename + ' already exists and was therefore removed from dump')

    update_folders(all_destinations)


def get_all_info(folder_path, save=False):

    dir = folder_path + '\\Excel_files'
    all_files = os.listdir(dir)
    all_info = []

    for filename in all_files:

        # get run name
        run_type = ""
        if "form" in filename:
            run_type = "form"
        if "read" in filename:
            if "pristine" in filename:
                run_type = "pristine read"
            else:
                run_type = "read"
        if "set" in filename:
            run_type = "set"
        if "reset" in filename:
            run_type = "reset"

        # get the run name
        char_list = [*filename]
        word_list = []
        word = []
        for char in char_list:
            if char == " ":
                word_list.append(word)
                word = []
            else:
                word.extend(char)


        run_nr = ""
        for i in word_list[-1]:
            run_nr = run_nr + i

        # drop the 'Run' part and extract number
        run_nr = int(run_nr[3:])


        df_data = pd.read_excel(dir + '\\' + filename, sheet_name="Sheet1", dtype=float)

        df_params = pd.read_excel(dir + '\\' + filename, sheet_name="Sheet3")
        df_params.rename({"Unnamed: 0": "Parameter", "Unnamed: 1": "Value 1", "Unnamed: 2": "Value 2"}, axis="columns", inplace=True)
        param_list = settings.parameter_list
        df_params_filtered = df_params[df_params["Parameter"].isin(param_list)]
        df_params_filtered.set_index('Parameter', inplace=True)


        time_data = df_params_filtered.loc['Last Executed']['Value 1']
        time_data = datetime.strptime(time_data, "%m/%d/%Y %H:%M:%S")


        if "read" not in filename:
            # drop first and last items (if sweep starts and ends with 0v)
            if df_data.iloc[0][settings.V_sweep_column] == 0:
                df_data.drop(index=[0], inplace=True)
            if df_data.iloc[-1][settings.V_sweep_column] == 0:
                df_data.drop(len(df_data), inplace=True)

        this_info = {'type':run_type, 'nr':run_nr, 'time':time_data, 'parameters':df_params_filtered, 'data':df_data}
        all_info.append(this_info)

    if save==True:
        try:
            with open(folder_path + '\\Pickles\\info_file.pickle', 'wb') as f:
                    pickle.dump(all_info, f, protocol=pickle.HIGHEST_PROTOCOL)
        except FileNotFoundError:
            os.makedirs(folder_path + '\\Pickles')
            with open(folder_path + '\\Pickles\\info_file.pickle', 'wb') as f:
                    pickle.dump(all_info, f, protocol=pickle.HIGHEST_PROTOCOL)

    return all_info
