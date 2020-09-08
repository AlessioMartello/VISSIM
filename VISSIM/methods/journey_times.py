from VISSIM.methods.helpers import load_VISSIM_file
import pandas as pd
import pathlib
from VISSIM.methods.helpers import data_inputs_path, df_writer, get_project_name


# Some values are hardcoded into the script (skipfooter and initial skiprows). These are not variable.
# Any changing values have been considered and their calculation automated.
# Such as the length of rows to skip
def get_journey_times():
    results = pd.DataFrame()  # Initiate results DataFrame to append to on line 23
    use_cols = [col for col in range(1, 400,
                                     2)]  # Make a list of columns, to use when reading the DataFrame, every other column is useful.
    suffix = ".rsz"  # Define filename suffix for Journey time analysis
    file_count = 0  # Initialise file count for column names
    project_name = None
    for path in pathlib.Path(data_inputs_path).iterdir():
        if str(path).endswith(suffix):
            excess_data = load_VISSIM_file(path=path, skiprows=8,
                                           skipfooter=5)  # Create a DataFrame including the excess data only
            skip_length = len(
                excess_data[
                    excess_data[0].str.contains("No.")])  # Get the (length) number of rows containing excess data
            relevant_data = load_VISSIM_file(path=path, sep=";", skiprows=(8 + skip_length), use_cols=use_cols
                                             )  # load only the final data by skipping the length of the
            # excess data. Not hardcoded because this is changeable
            journey_times = relevant_data.drop([0, 1, 2, 3])  # Extract only the Journey Time row
            results = results.append(journey_times)  # add the extracted data to a DataFrame
            file_count += 1
            if project_name is None:
                project_name = get_project_name(path)
    JT_route = relevant_data.drop([0, 1, 3, 4])  # Extract the Journey Time labels

    for col in use_cols:
        try:
            results[col] = pd.to_numeric(results[col])
            JT_route[col] = pd.to_numeric(JT_route[col])
        except KeyError:
            continue

    avg = results.mean(axis=0)  # Average journey times
    results = results.append(avg, ignore_index=True)  # Add average to the end of the results DataFrame
    results = pd.concat([JT_route, results]).reset_index(drop=True)  # Add the respective Journey time labels
    results_transposed = results.transpose(copy=True)  # Transpose DataFrame for readability

    # Create list of columns, rename dataFrame
    files = ["Routes"]
    [files.append("Seed " + str(i + 1)) for i in range(file_count)]
    files.append("Average")
    results_transposed.columns = files

    # Write results to an Excel file, timestamp ensures no overwriting
    writer = pd.ExcelWriter(df_writer(project_name, "Journey_times"))
    results_transposed.to_excel(writer, "Journey time results", index=False)
    writer.save()