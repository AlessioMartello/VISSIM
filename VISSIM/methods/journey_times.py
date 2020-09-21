import pandas as pd
import pathlib

from .helpers import load_VISSIM_file, df_writer, check_project_name, df_to_numeric
from .helpers import data_inputs_path, project


def get_journey_times(data_directory):
    """Extracts the average journey times of each route."""

    results = pd.DataFrame()  # Initiate results DataFrame to append results
    use_cols = [col for col in range(1, 400, 2)]  # Create list of columns, to use when reading the DataFrame.
    SUFFIX, file_count = ".rsz", 0  # Initialise file count to be used for column names

    for path in pathlib.Path(data_directory).iterdir():
        if str(path).endswith(SUFFIX):
            excess_data = load_VISSIM_file(path=path, skiprows=8, skipfooter=5)
            skip_length = len(excess_data[excess_data[0].str.contains("No.")])  # Get the number of rows to skip
            relevant_data = load_VISSIM_file(path=path, sep=";", skiprows=(8 + skip_length), use_cols=use_cols)
            journey_times = relevant_data.drop([0, 1, 2, 3])  # Extract only the Journey Time row
            results = results.append(journey_times)  # add the extracted data to a DataFrame
            file_count += 1
            project_name = check_project_name(project, path)
    jt_route = relevant_data.drop([0, 1, 3, 4])  # Extract the Journey Time labels

    df_to_numeric(use_cols, results, jt_route)  # Convert the data to be numerical

    avg = results.mean(axis=0)  # Average journey times
    results = results.append(avg, ignore_index=True)  # Add average to the end of the results DataFrame
    results = pd.concat([jt_route, results]).reset_index(drop=True)  # Add the respective Journey time labels
    results_transposed = results.transpose(copy=True)  # Transpose DataFrame for readability in Excel

    # Create list of columns, rename dataFrame
    files = ["Routes"]
    [files.append("Seed " + str(num + 1)) for num in range(file_count)]
    files.append("Average")
    results_transposed.columns = files

    # Write results to an Excel file, timestamp ensures no overwriting
    writer = pd.ExcelWriter(df_writer(project_name, "Journey_times", data_directory))
    results_transposed.to_excel(writer, "Journey time results", index=False)
    writer.save()
