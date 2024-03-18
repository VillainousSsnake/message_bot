# /App/GUI/main_menu.py
# Contains main menu code


# Importing modules and libraries:
from App.AppLib.config import Config
from functools import partial
import customtkinter as ctk


# ProgFunc class, contains functions that the program uses
class ProgFunc:

    @staticmethod
    def update_time_interval_entry(self, event):

        text = self.get()

        if event.keysym == "BackSpace":
            text = text[:len(text) - 1]
        elif hasattr(event, "char"):
            text = text + event.char

        if str(text).isdigit():
            self.configure(text_color="white")
            Config.overwrite_setting("previous_interval", text)
        else:
            self.configure(text_color="red")


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

    # Creating time interval frame
    time_interval_frame = ctk.CTkFrame(master=root, fg_color="#242424")
    time_interval_frame.pack()

    # Creating a time interval frame children
    time_interval_label = ctk.CTkLabel(
        master=time_interval_frame,
        text="Time interval (Milliseconds):",
        fg_color="#1F6AA5",
        width=200,
        corner_radius=15,
        anchor="w",
    )
    time_interval_label.pack()

    time_interval_entry = ctk.CTkEntry(
        master=time_interval_frame,
        width=200,
    )
    time_interval_entry.pack()

    # Inserting the correct number into time_interval_entry
    if app.settings["previous_interval"] is None:
        time_interval_entry.configure(placeholder_text="(Eg. '100' for 100 milliseconds)")
    else:
        time_interval_entry.insert(0, app.settings["previous_interval"])

    # TODO: More code goes here

    # Root mainloop
    root.mainloop()
