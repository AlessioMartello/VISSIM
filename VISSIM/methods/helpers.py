import pandas as pd
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows

# Function to load data from the VISSIM data files into a Pandas DataFrame
def load_VISSIM_file(path=None, columns=None, use_cols=None, skiprows=0, nrows=None, index_col=False, sep="\s+", skipfooter=0):
    raw_data = pd.read_csv(filepath_or_buffer=path, sep=sep, names=columns, header=None, engine="python", skiprows=skiprows,
                           skipfooter=skipfooter, usecols=use_cols, index_col=index_col, nrows=nrows)
    return raw_data

# Function used to get the name of the data set from the files and use this to name the output file.
def get_project_name(path):
    df = load_VISSIM_file(path=path,columns=None, use_cols=None, skiprows=4, nrows=1, index_col=False, sep="\s|:")
    df = df.values.tolist()[0]
    project_name = [element for element in df if element != "Comment" and type(element) == str]
    project_name = " ".join(project_name)
    return project_name