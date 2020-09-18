import tkinter as tk
from tkinter import filedialog, messagebox

from methods.saturation_flow import get_saturation_flows
from methods.journey_times import get_journey_times
from methods.demand_dependencies import get_demand_dependencies
from methods.traffic_flows import get_traffic_flows

background_colour = "#d6d6d6"
foreground_colour = "#512d6d"
root = tk.Tk()
root.geometry("600x450")
root.configure(bg=background_colour)


def open_directory_dialogue():
    """Assigns the location of the selected directory to a global variable"""
    global data_directory
    data_directory = filedialog.askdirectory()


def hit_and_run():
    """ Runs the selected function(s) in the checkButton widget"""
    # Refactor me to be more elegant!
    if saturation_flow_state.get():
        try:
            max_headway = int(e.get())
        except ValueError:
            messagebox.showinfo("Error", "Select an appropriate data folder.")
            pass
    try:
        if journey_time_state.get() and saturation_flow_state.get() and demand_dependency_state.get() and traffic_flow_state.get():
            get_journey_times(data_directory)
            get_saturation_flows(data_directory, max_headway)
            get_demand_dependencies(data_directory)
            get_traffic_flows(data_directory)
        elif journey_time_state.get() and saturation_flow_state.get() and traffic_flow_state.get():
            get_journey_times(data_directory)
            get_saturation_flows(data_directory, max_headway)
            get_traffic_flows(data_directory)
        elif journey_time_state.get() and demand_dependency_state.get() and traffic_flow_state.get():
            get_journey_times(data_directory)
            get_demand_dependencies(data_directory)
            get_traffic_flows(data_directory)
        elif saturation_flow_state.get() and demand_dependency_state.get() and traffic_flow_state.get():
            get_saturation_flows(data_directory, max_headway)
            get_demand_dependencies(data_directory)
            get_traffic_flows(data_directory)
        elif journey_time_state.get() and saturation_flow_state.get() and demand_dependency_state.get():
            get_journey_times(data_directory)
            get_saturation_flows(data_directory, max_headway)
            get_demand_dependencies(data_directory)
        elif demand_dependency_state.get() and traffic_flow_state.get():
            get_demand_dependencies(data_directory)
            get_traffic_flows(data_directory)
        elif saturation_flow_state.get() and traffic_flow_state.get():
            get_saturation_flows(data_directory, max_headway)
            get_traffic_flows(data_directory)
        elif journey_time_state.get() and traffic_flow_state.get():
            get_journey_times(data_directory)
            get_traffic_flows(data_directory)
        elif demand_dependency_state.get():
            get_demand_dependencies(data_directory)
        elif saturation_flow_state.get():
            get_saturation_flows(data_directory, max_headway)
        elif journey_time_state.get():
            get_journey_times(data_directory)
        elif traffic_flow_state.get():
            get_traffic_flows(data_directory)
    except NameError:
        messagebox.showinfo("Error", "First you must select a data folder, containing the appropriate data.")
    except KeyError:
        messagebox.showinfo("Error", "Maximum headway cannot be zero.")


intro_label = tk.Label(root, text="Select the analyses you would like to perform:", bg=background_colour,
                       fg=foreground_colour, font=("", 15, "bold")).pack()

demand_dependency_state, journey_time_state, saturation_flow_state, traffic_flow_state = tk.BooleanVar(), tk.BooleanVar(), tk.BooleanVar(), tk.BooleanVar()
demand_dependency_button = tk.Checkbutton(root, text="Demand dependency", variable=demand_dependency_state,
                                         bg=background_colour, fg=foreground_colour, highlightcolor=foreground_colour,
                                          font=("", 15), pady=10).pack()
journey_time_button = tk.Checkbutton(root, text="Journey time", variable=journey_time_state, bg=background_colour,
                                     fg=foreground_colour, highlightcolor=foreground_colour, font=("", 15),
                                     pady=10).pack()
traffic_flow_button = tk.Checkbutton(root, text="Traffic flow", variable=traffic_flow_state,
                                     bg=background_colour, fg=foreground_colour, highlightcolor=foreground_colour,
                                     font=("", 15), pady=10).pack()
saturation_flow_button = tk.Checkbutton(root, text="Saturation flow", variable=saturation_flow_state,
                                        bg=background_colour, fg=foreground_colour, highlightcolor=foreground_colour,
                                        font=("", 15), pady=10).pack()

headway_label = tk.Label(root, text="Enter the maximum accepted headway below if saturation flow is being performed.",
                         bg=background_colour, fg=foreground_colour, font=("", 10)).pack()

e = tk.Entry(root, width=5, borderwidth=5, bg="white", fg=foreground_colour)
e.pack()

select_data_button = tk.Button(root, text="Select data folder", state="normal", command=open_directory_dialogue,
                               padx=50,
                               pady=20, fg=foreground_colour, font=("", 0, "bold")).pack()

run = tk.Button(root, text="Run", state="normal", command=hit_and_run, padx=50,
                pady=20, fg=foreground_colour, font=("", 0, "bold")).pack()

root.mainloop()
