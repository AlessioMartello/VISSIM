from VISSIM.methods.helpers import load_VISSIM_file, get_project_name
import pandas as pd
import openpyxl
import pathlib
from openpyxl.utils.dataframe import dataframe_to_rows
from VISSIM.methods.helpers import data_inputs_path, data_outputs_path

def get_demand_dependencies():
    study_period_data = pd.DataFrame()  # initialise empty DataFrame to append cleaned data and ones for results
    all_results = pd.DataFrame()

    # Read Excel file, extract the SC number and SCJ number.

    dd_file_path = data_inputs_path.joinpath('Demand_dependancy.xlsx')
    book = openpyxl.load_workbook(dd_file_path)
    worksheet = book.active
    sites = []
    sc = []
    for row in worksheet.iter_rows(min_row=5):
        site = row[0].value
        signal_control = row[4].value
        if type(site) is int:
            sites.append(site)
            sc.append(signal_control)
        else:
            continue

    # Get times from Excel file to inform where to slice the DataFrame
    warmup_time = worksheet.cell(row=5, column=15).value
    cooldown_time = worksheet.cell(row=5, column=16).value

    file_number = 0  # initialise variable to count the number of .lsa files
    intro_lines = 8  # Hard code the number of introductory lines, to be ignored when reading DataFrame

    suffix = ".lsa"  # The suffix for demand dependency files from VISSIM, to be checked for when reading files
    signal_group_list_length = 0  # Initialise variable to ensure the length of introductory data is read once only

    # Filter the combined DataFrame for each of the extracted value combinations. Average the length of the occurrence and
    # append the results to a list.
    aspect = "green"
    results = list()
    project_name = None  # Initialise project_name as none, to only run get_project_name() once at the end of the below loop

    # Read each .lsa file in directory, filter based on the warmup and cooldown times.
    # Get each demand dependant stage count per filtered file.
    # Append to the all_results DataFrame.
    for path in pathlib.Path(data_inputs_path).iterdir():
        if str(path).endswith(suffix):
            raw_data = load_VISSIM_file(path=path, sep=";", columns=["Time", "SCJ", "SC", "Signal"], use_cols=[0, 2, 3, 4],
                                        skiprows=intro_lines)
            signal_group_list_length = len(raw_data[raw_data["Time"].str.contains("SC")])
            raw_data = load_VISSIM_file(path=path,sep=";", columns=["Time", "SCJ", "SC", "Signal"], use_cols=[0, 2, 3, 4],
                                        skiprows=intro_lines + signal_group_list_length)
            df = raw_data[(raw_data.Time > warmup_time) & (raw_data.Time < cooldown_time)]
            seed_results = []
            for SCJ_number, SC_number in zip(sites, sc):
                green_signal_instances = df[
                    (df.SCJ == SCJ_number) & (df.SC == SC_number) & (df["Signal"].str.contains(aspect))]
                seed_results.append(len(green_signal_instances))
            all_results["Seed " + str(file_number + 1)] = pd.Series(seed_results, dtype=float)
            file_number += 1
            if project_name is None:
                project_name = get_project_name(path)

    # Rename the indices of the results DataFrame using the Demand dependency codes
    names = [f'{SCJ}_{SC}_{aspect}' for SCJ, SC in zip(sites, sc)]
    all_results.index = names

    all_results["Average"] = all_results.mean(axis=1)  # Get the average per demand dependant criteria

    # Insert the results into the designated column in previously read Excel file.
    row_number = 5
    for value in all_results["Average"]:
        worksheet.cell(row=row_number, column=9).value = value
        row_number += 1

    # Append the results from all seeds into the seconds sheet
    worksheet = book["Seed validation"]
    for row in dataframe_to_rows(all_results, index=True, header=True):
        worksheet.append(row)

    # Save the file
    filename = "Demand_dependency " + str(project_name) + ".xlsx"
    demand_dependancy_output = data_outputs_path.joinpath(filename)
    book.save(demand_dependancy_output)
