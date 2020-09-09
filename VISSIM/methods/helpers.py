import pathlib

import pandas as pd
from datetime import datetime


# Function to load data from the VISSIM data files into a Pandas DataFrame
def load_VISSIM_file(path=None, columns=None, use_cols=None, skiprows=0, nrows=None, index_col=False, sep="\s+",
                     skipfooter=0):
    raw_data = pd.read_csv(filepath_or_buffer=path, sep=sep, names=columns, header=None, engine="python",
                           skiprows=skiprows,
                           skipfooter=skipfooter, usecols=use_cols, index_col=index_col, nrows=nrows)
    return raw_data


# Function used to get the name of the data set from the files and use this to name the output file.
def get_project_name(path):
    df = load_VISSIM_file(path=path, columns=None, use_cols=None, skiprows=4, nrows=1, index_col=False, sep="\s|:")
    df = df.values.tolist()[0]
    file_name = [element for element in df if element != "Comment" and type(element) == str]
    file_name = " ".join(file_name)
    return file_name


def df_writer(project_name, analysis):
    now = datetime.now().strftime("%d-%m_%H.%M")
    save_filename = f"{analysis}_{project_name}_{now}.xlsx"
    writer = data_outputs_path.joinpath(analysis.lower(), save_filename)
    return writer


def check_project_name(project, path):
    if project is None:
        project = 1
        return get_project_name(path)


data_inputs_path = pathlib.Path(__file__).resolve().parents[2].joinpath("data\\inputs")
data_outputs_path = pathlib.Path(__file__).resolve().parents[2].joinpath("data\\outputs")
project = None
