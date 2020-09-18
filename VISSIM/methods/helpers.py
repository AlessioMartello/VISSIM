import pathlib

import pandas as pd
from datetime import datetime


def load_VISSIM_file(path=None, columns=None, use_cols=None, skiprows=0, nrows=None, index_col=False, sep="\s+",
                     skipfooter=0, header=None):
    """
    Function to load data from the VISSIM data files format.

    Parameters:
        path (Path): File location.
        columns (list): Column names.
        use_cols (list): Columns to be used.
        skiprows (int): Rows to skip from the top when reading DataFrame.
        nrows (int): Number of rows to include.
        index_col (Bool): Boolean, informs whether to treat first column as the index column.
        sep (regEx): custom delimiter to define the separator(s) between useful data.
        skipfooter (int): Rows to skip form the bottom when reading DataFrame.

    Returns:
        raw_data: A pandas DataFrame.
    """

    raw_data = pd.read_csv(filepath_or_buffer=path, sep=sep, names=columns, header=header, engine="python",
                           skiprows=skiprows,
                           skipfooter=skipfooter, usecols=use_cols, index_col=index_col, nrows=nrows)
    return raw_data


def get_project_name(path):
    """
    Function used to get the name of the data set from the loaded DatFrame; it is used to name the output file.

    Parameters:
        path (Path): File path object.

    Returns:
        file_name: a string containing the name of the project.
    """

    df = load_VISSIM_file(path=path, columns=None, use_cols=None, skiprows=4, nrows=1, index_col=False, sep="\s|:")
    df = df.values.tolist()[0]
    file_name = [element for element in df if element != "Comment" and type(element) == str]
    file_name = " ".join(file_name)
    return file_name


def df_writer(project_name, analysis, data_directory):
    """
    Function returns full file path and name of the save location.

    Parameters:
        project_name (str): The returned string from get_project_name()
        analysis (str): The analysis type being performed; it is used to inform the filename.
        data_directory:

    Returns:
        writer: a Pandas Excel writer object containing the file path of the project and where to save.
    """

    now = datetime.now().strftime("%d-%m_%H.%M")
    save_filename = f"{analysis}_{project_name}_{now}.xlsx"
    writer = pathlib.Path(data_directory).joinpath(save_filename)
    return writer


def check_project_name(project, path):
    """"" Checks whether a project name exist, and if not, returns it using get_project_name()"""
    if project is None:
        project = 1
        return get_project_name(path)


def df_to_numeric(columns, *dfs):
    """ Converts any number of DataFrames with data as Python Objects to numerical data. """
    for df in dfs:
        for col in columns:
            try:
                df[col] = pd.to_numeric(df[col], errors="coerce")
            except KeyError:
                continue


data_inputs_path = pathlib.Path(__file__).resolve().parents[2].joinpath("data\\inputs")
data_outputs_path = pathlib.Path(__file__).resolve().parents[2].joinpath("data\\outputs")
project = None