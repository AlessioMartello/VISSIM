import pathlib
import os

# print(os.getcwd())
# print(os.chdir("/VISSIM/data/"))

save_path = f'{pathlib.Path(__file__).resolve().parents[1]}\data\inputs'  # finding relative path folder
file_name = f'{"Demand_dependency.xlsx"}'  # generate file name
raw_data_file = os.path.join(save_path, file_name)  # generate absolute path
print(raw_data_file)