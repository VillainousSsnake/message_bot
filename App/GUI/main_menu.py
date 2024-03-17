# /App/GUI/main_menu.py
# Contains main menu code


# Importing modules and libraries:
from functools import partial
import customtkinter as ctk


# ProgFunc class, contains functions that the program uses
class ProgFunc:
    def __init__(self):
        pass  # TODO: Stub

    @staticmethod
    def update_time_interval_entry(self, event):
        pass  # TODO: Stub


# main_menu function
def main_menu(app):

    # Creating root window
    root = ctk.CTk()
    root.title("message_bot - Main Menu - App Version: 1.0 - HigharcheySDL Version: 1.0")
    root.geometry("850x525+200+200")

    # Defining on_close function
    def on_close():
        root.destroy()
        app.returnStatement = "exit"

    # Assigning the buttons on the tkinter window top bar
    root.protocol("WM_DELETE_WINDOW", on_close)

    # Creating a time interval label and entry
    time_interval_label = ctk.CTkLabel(
        master=root,
        text="Time interval:",
        fg_color="#1F6AA5",
        width=150,
        corner_radius=15,
    )
    time_interval_label.pack()

    time_interval_entry = ctk.CTkEntry(
        master=root,
        width=150,
    )
    time_interval_entry.pack()

    # Inserting the correct number into time_interval_entry
    if app.settings["previous_interval"] is None:
        time_interval_entry.configure(placeholder_text="(Eg. '100' for 100 milliseconds)")
    else:
        time_interval_entry.insert("0.0", app.settings["previous_interval"])

    # Binding an update command to time_interval_entry
    time_interval_entry_command = partial(ProgFunc.update_time_interval_entry, time_interval_entry)
    time_interval_entry.bind("<Key>", time_interval_entry_command)

    # TODO: More code goes here

    # Root mainloop
    root.mainloop()
