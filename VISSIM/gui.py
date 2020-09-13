import tkinter as tk
from tkinter import filedialog

from methods.saturation_flow import get_saturation_flow
from methods.journey_times import get_journey_times
from methods.demand_dependencies import get_demand_dependencies

root = tk.Tk()  # Window contains all the widgets
root.geometry("250x250")


def open_directory_dialogue():
    """Assigns the location of the selected directory to a variable"""
    global data_directory
    data_directory = filedialog.askdirectory()


def hit_and_run():
    """ Runs the selected function in the checkButton widget"""
    # Refactor me!!
    #
    if demand_dependency_state.get():
        get_demand_dependencies(data_directory)
    # #
    # elif saturation_flow_state.get():
    #     get_saturation_flow(data)
    #
    # elif journey_time_state.get():
    #     get_journey_times(data)
    #

intro_label = tk.Label(root, text="Select the analyses you would like to perform").pack()  # method adds the label
# "greeting" to the window  # Label widget

demand_dependency_state, journey_time_state, saturation_flow_state = tk.BooleanVar(), tk.BooleanVar(), tk.BooleanVar()

demand_dependency_button = tk.Checkbutton(root, text="Demand dependency", variable=demand_dependency_state).pack()
journey_time_button = tk.Checkbutton(root, text="Journey time", variable=journey_time_state).pack()
saturation_flow_button = tk.Checkbutton(root, text="Saturation flow", variable=saturation_flow_state).pack()

select_data_button = tk.Button(root, text="Select data and run", state="active", command=open_directory_dialogue, padx=50,
                               pady=15).pack()

run = tk.Button(root, text="Run", state="active", command=hit_and_run, padx=50,
                pady=15).pack()

root.mainloop()  # Event loop
