import pathlib
import pandas as pd

from .helpers import data_inputs_path, project
from .helpers import load_VISSIM_file, df_writer, check_project_name, df_to_numeric


def get_saturation_flows(data_directory, max_headway):
    """ Calculates the average saturation flow per stop-line. """

    # Declare DataFrames so that results can be appended at the end.
    results, summary_results, ignored_results = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    # Perform algorithm on each file in "Special_eval_files" folder.
    for path in pathlib.Path(data_directory).iterdir():
        if str(path)[-4:-2] == ".a":
            try:
                all_cols = [str(col) for col in range(100)]
                use_cols = all_cols[3:]  # We are only concerned with the fourth column, onwards.

                # Read the file, using our desired columns, delimiter set as space or colon separated.
                raw_data = load_VISSIM_file(path, sep='\s+|:', columns=all_cols, use_cols=use_cols, skiprows=7,
                                            skipfooter=4)

                # Slice the numerical data from the raw data and make a copy, to avoid chained-assignment warning.
                df = raw_data[1:].copy()

                # Locate the row containing the stopline name, extract the name and remove the trailing parenthesis.
                categorical_info = raw_data.iloc[0].copy()
                stopline_name = int(categorical_info[7][:-1])
                df.dropna(axis="columns", how="all", inplace=True)  # Remove excess empty columns
                df.columns = ["Column " + col for col in df]
                df.fillna(-1, inplace=True)  # Replace null values with -1 as to be ignored later

                # Remove the brackets and parenthesis so that data can be returned as int
                for col_name in df.columns:
                    df[col_name] = df[col_name].astype(str).str.replace("(", "-")

                # Change values containing trailing parenthesis to -1, so they get discarded in the final calculation.
                for col in df:
                    rows = 1  # Since we sliced the df, row 0 is not present and we start on row 1.
                    for value in df[col]:
                        if ")" in str(value):
                            df.at[rows, str(col)] = -1
                        rows += 1

                df_to_numeric(df.columns, df)  # Make the data numerical.

                # The Macro doesnt count anything above or including the maximum acceptable headway. So set anything
                # above this to -1, so it gets ignored. The same goes for pre-existing zeros.
                df[(df >= max_headway) | (df == 0)] = -1
                df = df.to_numpy()  # Convert to numpy array for easier and faster manipulation.

                # Loop through each row. If the value (discharge rate) is over the headway limit, go to the next
                # line. Otherwise increase the count and add this discharge rate to the cumulative_discharge_rate.
                # Skip the row containing un-useful data and after this row, start the loop one column to the right,
                # to account for the indent in the data.
                cumulative_discharge_rate, discharge_rate_count = 0, 0
                for row in df:
                    for col in row:
                        if 0 <= col <= max_headway:
                            cumulative_discharge_rate = cumulative_discharge_rate + col
                            discharge_rate_count += 1
                        else:
                            break

                # Perform the Saturation Flow calculation.
                sat_flow = round(3600 / (cumulative_discharge_rate / discharge_rate_count))

                results = results.append({"File": path, "Count": discharge_rate_count,
                                          "Saturation flow": sat_flow}, ignore_index=True)

                # Append the results per stop-line (file suffix) to a dataFrame.
                summary_results = summary_results.append(
                    {'ID': str(path)[-3:], "Stop-line": stopline_name, "Number of measurements": discharge_rate_count,
                     "Saturation flow": sat_flow}, ignore_index=True)
                project_name = check_project_name(project, path)

            except ZeroDivisionError:
                ignored_results = ignored_results.append(
                    {'File': path, "Number of measurements": discharge_rate_count}, ignore_index=True)

    # Group the same stop-lines together using the file suffix and get the average of the Saturation flows and the total
    # number of measurements for that saturation flow.
    results_grouped = summary_results.groupby(["ID", "Stop-line"]).agg(
        {"Saturation flow": "mean", "Number of measurements": "sum"}).round()

    writer = pd.ExcelWriter(df_writer(project_name, "Saturation_flows"))
    results_grouped.to_excel(writer, "Summary results")
    results.to_excel(writer, "All results", index=False)
    ignored_results.to_excel(writer, "Ignored files", index=False)
    writer.save()
