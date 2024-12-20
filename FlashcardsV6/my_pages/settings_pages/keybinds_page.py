import tkinter as tk

from my_custom_widgets import VerticalScrolledFrame, KeyBindsWidget

from my_settings_lib import settingsObj as stg

class KeyBindsPage(VerticalScrolledFrame):
    """
    Populated by keys (actions) and values (keybinds) found under keybinds, in settings_config.json

    Creation of new keybinds takes place only within settings_config.json
    - all KeyBindWidget()s are placed in the same order as those within settings_config.json

    ### Parameter
    - master: SettingsPage()
        - solely for placing this widget into
    
    ### Properties
    - retrieve_updated_keybinds(self) -> dict
        - collects all actions and keybinds and constructs a new dictionary
        - to be as used within Settings()'s update_settings_config() as 'updated_value' parameter
    """
    def __init__(self, master):
        super().__init__(parent=master)
        self.keybinds = {"KEYBINDS":{}}

        self.keybindOptions: list[KeyBindsWidget] = []
        for action, keybind in stg.KEYBINDS.items():
            self.keybindOptions.append(
                KeyBindsWidget(
                    master=self.interior,
                    action=action,
                    keybind=keybind,
                    grid_enabled=False
                )
            )
    
    def retrieve_updated_keybinds(self):
        """
        - collects all actions and keybinds and constructs a new dictionary
        - to be as used within Settings()'s update_settings_config() as 'updated_value' parameter
        """
        for keybindOption in self.keybindOptions:
            self.keybinds["KEYBINDS"][keybindOption.action] = keybindOption.keybind

        return self.keybinds