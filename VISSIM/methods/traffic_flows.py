import pathlib
import pandas as pd

from .helpers import project
from .helpers import load_VISSIM_file, df_writer, check_project_name, df_to_numeric


def get_traffic_flows(data_directory):
    """ Extracts the traffic flows from all .mes files and creates an average"""
    writer = None
    count = 0
    df_concat = pd.DataFrame()
    for path in pathlib.Path(data_directory).iterdir():
        if str(path).endswith(".mes"):  # Perform operation only on .mes files
            count += 1
            try:
                if not writer:  # Get the project name and create a writer object only once
                    project_name = check_project_name(project, path)
                    writer = pd.ExcelWriter(df_writer(project_name, "Traffic_flows", data_directory))
                raw_data = load_VISSIM_file(path=path, sep='\s+|:', skiprows=8)
                skip_length = len(
                    raw_data[raw_data[0].str.contains("Measurement")])  # Automate the number of rows to skip
                relevant_data = load_VISSIM_file(path=path, sep=";", skiprows=(16 + skip_length), header=0)

                # Extract the relevant columns, label the Route column and make data numerical. Write to Excel file
                relevant_data.rename(columns={relevant_data.columns[0]: "Data collection point"}, inplace=True)
                relevant_data.drop(relevant_data.columns[[1, 2]], axis=1, inplace=True)
                df_to_numeric(relevant_data.columns, relevant_data)
                relevant_data.to_excel(writer, f"Seed {count}", index=False, header=True)

                # Join all data together vertically, group by the route name, get the average
                df_concat = pd.concat((df_concat, relevant_data))
                grouped = df_concat.groupby(by=["Data collection point"])
                df_means = grouped.mean().round()

            except IndexError:
                print(f"File {path} does not not have appropriate delimiters")

    df_means.to_excel(writer, f"Average", index=True,
                      header=True)  # Write the DataFrame containing averages to last sheet
    writer.save()
