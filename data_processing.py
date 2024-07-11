import matplotlib.pyplot as plt
import matplotlib as mpl 
import pandas as pd
import os
from datetime import datetime
import pickle
import shutil
import settings

r_col = settings.resistance_column
i_sw_col = settings.I_sweep_column
v_sw_col = settings.V_sweep_column
i_r_col = settings.I_read_column
v_r_col = settings.V_read_column
t_col = 'Time'


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

            try:
                info = get_all_info(dest)
                with open(dest + '\\Pickles\\info_file.pickle', 'wb') as f:
                    pickle.dump(info, f, protocol=pickle.HIGHEST_PROTOCOL)
            except FileNotFoundError:
                print('passing')
                pass

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
        print(filename)
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



        xl = pd.ExcelFile(dir + '\\' + filename)
        sheet_names = xl.sheet_names
        first_sheet = sheet_names[0]
        last_sheet = sheet_names[-1]

        df = pd.read_excel(dir + '\\' + filename, sheet_name=first_sheet)

        # Change column B and C's values to integers
        # if run_type == 'form' or run_type == 'set' or run_type == 'reset':
        #     df_data = df.astype({i_sw_col: float, v_sw_col: float, r_col: float, t_col: float})
        # else:
        #     df_data = df.astype({i_r_col: float, v_r_col: float, r_col: float, t_col: float})

        df_data = df.apply(pd.to_numeric, errors='ignore')


        df_params = pd.read_excel(dir + '\\' + filename, sheet_name=last_sheet)
        df_params.rename({"Unnamed: 0": "Parameter", "Unnamed: 1": "Value 1", "Unnamed: 2": "Value 2"}, axis="columns", inplace=True)
        param_list = settings.parameter_list
        df_params_filtered = df_params[df_params["Parameter"].isin(param_list)]
        df_params_filtered.set_index('Parameter', inplace=True)

        time_data = df_params_filtered.loc['Last Executed']['Value 1']
        time_data = datetime.strptime(time_data, "%m/%d/%Y %H:%M:%S")


        if run_type == 'form' or run_type == 'set' or run_type == 'reset':
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


def refresh_dfolders():
    all_folders = os.listdir(home_path + '\\Data')

    for sample in all_folders:
        print(sample)
        devices = os.listdir(home_path + '\\Data\\' + sample)
        for d in devices:
            print(d)
            dir = home_path + '\\Data\\' + sample + '\\' + d
            update_folders([dir])
            
            
            
            
        

#refresh_dfolders()
