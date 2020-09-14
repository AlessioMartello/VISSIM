import tkinter as tk
from tkinter import filedialog, messagebox

from methods.saturation_flow import get_saturation_flow
from methods.journey_times import get_journey_times
from methods.demand_dependencies import get_demand_dependencies

background_colour = "white"
foreground_colour = "#512d6d"
root = tk.Tk()
root.geometry("500x400")
root.configure(bg= background_colour)

def open_directory_dialogue():
    """Assigns the location of the selected directory to a global variable"""
    global data_directory
    data_directory = filedialog.askdirectory()


def hit_and_run():
    """ Runs the selected function(s) in the checkButton widget"""
    # Refactor me to be more elegant!
    try:
        if journey_time_state.get() and saturation_flow_state.get() and demand_dependency_state.get():
            get_journey_times(data_directory) and get_saturation_flow(data_directory) and get_demand_dependencies(data_directory)
        elif journey_time_state.get() and saturation_flow_state.get():
            get_journey_times(data_directory) and get_saturation_flow(data_directory)
        elif journey_time_state.get() and demand_dependency_state.get():
            get_journey_times(data_directory) and get_demand_dependencies(data_directory)
        elif saturation_flow_state.get() and demand_dependency_state.get():
            get_saturation_flow(data_directory) and get_demand_dependencies(data_directory)
        elif demand_dependency_state.get():
            get_demand_dependencies(data_directory)
        elif saturation_flow_state.get():
            get_saturation_flow(data_directory)
        elif journey_time_state.get():
            get_journey_times(data_directory)
    except NameError:
        messagebox.showinfo("Error", "First you must select a data folder.")
    except ValueError:
    	messagebox.showinfo("Error", "Ensure your chosen folder has the appropriate data")


intro_label = tk.Label(root, text="Select the analyses you would like to perform:", bg= background_colour, fg= foreground_colour, font= ("", 15, "bold")).pack()

demand_dependency_state, journey_time_state, saturation_flow_state = tk.BooleanVar(), tk.BooleanVar(), tk.BooleanVar()

demand_dependency_button = tk.Checkbutton(root, text="Demand dependency", variable=demand_dependency_state, bg=background_colour, fg=foreground_colour, highlightcolor=foreground_colour, font= ("", 15), pady=10).pack()
journey_time_button = tk.Checkbutton(root, text="Journey time", variable=journey_time_state, bg=background_colour, fg=foreground_colour, highlightcolor=foreground_colour, font= ("", 15), pady=10).pack()
saturation_flow_button = tk.Checkbutton(root, text="Saturation flow", variable=saturation_flow_state, bg=background_colour, fg=foreground_colour, highlightcolor=foreground_colour, font= ("", 15), pady=10).pack()

select_data_button = tk.Button(root, text="Select data folder", state="active", command=open_directory_dialogue, padx=50,
                               pady=20, fg=foreground_colour, font=("",0,"bold")).pack()

run = tk.Button(root, text="Run", state="active", command=hit_and_run, padx=50,
                pady=20, fg=foreground_colour, font=("",0,"bold")).pack()

root.mainloop()