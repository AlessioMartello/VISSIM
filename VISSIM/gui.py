import tkinter as tk
from tkinter import filedialog

root = tk.Tk()  # Window contains all the widgets


def open_file_dialogue():
    root.filename = filedialog.askdirectory()


intro_label = tk.Label(root, text="Select the analyses you would like to perform", bg="purple", fg="white", height=10,
                 width=50).grid(row=0)  # method adds the label "greeting" to the window  # Label widget
select_data_button = tk.Button(root, text="Select data", state="active", command=open_file_dialogue, padx=50, pady=15).grid(row=1)

root.mainloop()  # Event loop
