# Higharchey/app.py
# Contains App class

# Importing Modules
from App.AppLib.config import Config


# App class
class App:
    def __init__(self):
        self.returnStatement = "main"
        self.settings = {
            "current_theme": Config.get_setting("current_theme"),
            "previous_interval": Config.get_setting("previous_interval"),
            "previous_message": Config.get_setting("previous_message"),
            "toggle_hotkey": Config.get_setting("toggle_hotkey"),
        }
