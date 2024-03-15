# /App/GUI/main_menu.py
# Contains main menu code


# Importing modules and libraries:
import customtkinter as ctk


# ProgFunc class, contains functions that the program uses
class ProgFunc:
    def __init__(self):
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

    # TODO: Code goes here

    # Root mainloop
    root.mainloop()
