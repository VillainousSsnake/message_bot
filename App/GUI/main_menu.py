# /App/GUI/main_menu.py
# Contains main menu code
import time

# Importing modules and libraries:
from App.AppLib.config import Config
from tkinter import messagebox
from functools import partial
from threading import Thread
import customtkinter as ctk
import tkinter as tk
import keyboard


# Creating global variable
BotIsRunning_global = False
SpecialCharactersList_global = [
   "~", "!", "@", "#", "$", "%", "^", "&", "(", ")", "_"
]


# ProgFunc class, contains functions that the program uses
class ProgFunc:

    @staticmethod
    def update_while_timer_running(root):
        root.update()

    @staticmethod
    def update_time_interval_entry(self: ctk.CTkEntry, event):

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

            if str(text) == "":
                Config.overwrite_setting("previous_interval", None)

    @staticmethod
    def update_message_entry(self: ctk.CTkEntry, event):

        text = self.get()

        if event.keysym == "BackSpace":
            text = text[:len(text) - 1]

            # Making empty strings convert to 'None'
            if text == "":
                text = None
        elif hasattr(event, "char"):
            text = text + event.char

        Config.overwrite_setting("previous_message", text)

    @staticmethod
    def toggle_bot_command(
            message_entry: ctk.CTkEntry,
            toggle_bot_button: ctk.CTkButton,
            root: ctk.CTk,
            app,
    ):

        # Importing global variables
        global BotIsRunning_global

        # Getting the text from toggle_bot_button
        status = toggle_bot_button.cget("text")

        match status:

            case "Start Bot":   # Starting the bot

                # Changing the text for toggle_bot_button
                toggle_bot_button.configure(text="Stop", text_color="red")

                # Getting and formatting the text to type
                text = message_entry.get()

                special_characters_dict = {
                    r"\n": "\n",
                    r"\\": "\\",
                }

                for key in special_characters_dict:
                    if key in text:
                        new_text = []
                        counter = 0
                        skip = False

                        for item in list(text):

                            if not skip:    # If it doesn't skip

                                if item == "\\":
                                    if list(text)[counter+1] == "\\":
                                        new_text.append("\\")
                                        skip = True
                                    elif list(text)[counter+1] == "n":
                                        new_text.append("enter")
                                        skip = True
                                else:
                                    new_text.append(item)

                            else:   # Setting skip to True
                                skip = True

                            counter += 1

                        text = new_text

                # Typing text
                BotIsRunning_global = True

                while BotIsRunning_global:

                    for item in text:

                        root.update()

                        if item.isupper() or item in SpecialCharactersList_global:
                            keyboard.press("shift")
                            keyboard.press_and_release(item)
                            keyboard.release("shift")
                        else:
                            keyboard.press_and_release(item)

                        if keyboard.is_pressed(app.settings["toggle_hotkey"]):
                            BotIsRunning_global = False

                            # Changing the text for toggle_bot_button
                            toggle_bot_button.configure(text="Start Bot", text_color="white")

                    timer_command = partial(ProgFunc.update_while_timer_running, root)
                    thread = Thread(target=timer_command)
                    thread.start()

                    # Preforming sanity checks
                    if Config.get_setting("previous_interval") is None and Config.get_setting("previous_message") is None:
                        messagebox.showerror(
                            "Error",
                            "Please fill out the interval entry and the message entry",
                        )
                        return 0

                    elif Config.get_setting("previous_interval") is None:
                        messagebox.showerror(
                            "Error",
                            "Please fill out the interval entry"
                        )
                        return 0

                    elif Config.get_setting("previous_message") is None:
                        messagebox.showerror(
                            "Error",
                            "Please fill out the message entry"
                        )
                        return 0

                    time.sleep(int(Config.get_setting("previous_interval"))/1000)

                    del thread

            case "Stop":
                BotIsRunning_global = False

                # Changing the text for toggle_bot_button
                toggle_bot_button.configure(text="Start Bot", text_color="white")

    @staticmethod
    def update_hotkey_entry(self: ctk.CTkEntry, event: tk.Event):

        text = self.get()

        if event.keysym == "BackSpace":
            text = text[:len(text) - 1]
        elif hasattr(event, "char"):
            text = text + event.char

        Config.overwrite_setting("toggle_hotkey", text)


# main_menu function
def main_menu(app):

    # Creating root window
    root = ctk.CTk()
    root.title("message_bot - v1.0.0")
    root.geometry("300x300")

    # Defining on_close function
    def on_close():
        root.destroy()
        app.returnStatement = "exit"

    # Assigning the buttons on the tkinter window top bar
    root.protocol("WM_DELETE_WINDOW", on_close)

    # Creating time interval frame
    time_interval_frame = ctk.CTkFrame(master=root, fg_color="#242424")
    time_interval_frame.pack(pady=10)

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

    # Binding an update command to time_interval_entry
    time_interval_entry_command = partial(ProgFunc.update_time_interval_entry, time_interval_entry)
    time_interval_entry.bind("<Key>", time_interval_entry_command)

    # Creating a message frame
    message_frame = ctk.CTkFrame(
        master=root,
        fg_color="#242424"
    )
    message_frame.pack(pady=10)

    # Creating message frame children
    message_label = ctk.CTkLabel(
        master=message_frame,
        text="Message:",
        fg_color="#1F6AA5",
        width=200,
        corner_radius=15,
        anchor="w",
    )
    message_label.pack()

    message_entry = ctk.CTkEntry(
        master=message_frame,
        width=200,
    )
    message_entry.pack()

    # Inserting the correct number into time_interval_entry
    if app.settings["previous_message"] is None:
        message_entry.configure(placeholder_text="(Eg. \"Hello!\")")
    else:
        message_entry.insert(0, app.settings["previous_message"])

    # Assigning the update command to message entry
    message_entry_command = partial(ProgFunc.update_message_entry, message_entry)
    message_entry.bind("<Key>", message_entry_command)

    # Creating hotkey frame
    hotkey_frame = ctk.CTkFrame(
        master=root,
        fg_color="#242424"
    )
    hotkey_frame.pack(pady=10)

    # Creating the hotkey frame's children
    hotkey_label = ctk.CTkLabel(
        master=hotkey_frame,
        text="Toggle Start/Stop Hotkey:",
        fg_color="#1F6AA5",
        width=200,
        corner_radius=15,
        anchor="w",
    )
    hotkey_label.pack()

    hotkey_entry = ctk.CTkEntry(
        master=hotkey_frame,
        width=200,
    )
    hotkey_entry.pack()

    # Inserting text into hotkey_entry
    hotkey_entry.insert(0, Config.get_setting("toggle_hotkey"))

    # Assigning update function to hotkey entry
    hotkey_entry_command = partial(ProgFunc.update_hotkey_entry, hotkey_entry)
    hotkey_entry.bind("<Key>", hotkey_entry_command)

    # Creating the toggle bot frame
    toggle_bot_frame = ctk.CTkFrame(master=root, fg_color="#242424")
    toggle_bot_frame.pack()

    # Creating the toggle bot frame's children
    toggle_bot_button = ctk.CTkButton(
        master=toggle_bot_frame,
        text="Start Bot",
    )
    toggle_bot_button.pack(pady=10)

    # Assigning the toggle_bot_button command
    toggle_bot_button_command = partial(
        ProgFunc.toggle_bot_command,
        message_entry,
        toggle_bot_button,
        root,
        app,
    )
    toggle_bot_button.configure(command=toggle_bot_button_command)

    # Root mainloop
    root.mainloop()
