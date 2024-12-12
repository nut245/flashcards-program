import json
import collections.abc

class Settings():
    def __init__(self):
        """
        pseudo-singleton class that manages the values within settings_config.json file

        ### Methods
        - update_settings_config(self, updated_value: dict) -> None
            - documentation found within function
        - format_keybind_string(self, string: str) -> str
            - documentation found within function
        """
        self.refresh_values()

    def refresh_values(self):
        """
        instantiates new values of settingsObj properties, taken from the potentially updated settings_config.json file
        """
        # importing settings_config.json
        self.settingsConfig = self._parse_settings_config()

        self.PADX = self.settingsConfig["PADX"]
        self.PADY = self.settingsConfig["PADY"]

        # ---
        
        # index to search for which theme is used
        self.INDEX = self.settingsConfig["INDEX"]

        # for the individual colours of each theme, dependant on index
        self.THEMES = self.settingsConfig["THEMES"]

        self.MODE = self.THEMES[self.INDEX]["mode"]
        self.DARK_TEXT_COLOUR = self.settingsConfig["DARK TEXT COLOUR"]

        self.BACKGROUND_COLOUR = self.THEMES[self.INDEX]["background"]
        self.FRAME_COLOUR = self.THEMES[self.INDEX]["frame"]
        self.ACCENT_COLOUR = self.THEMES[self.INDEX]["accent"]
        self.BUTTON_COLOUR = self.THEMES[self.INDEX]["button"]

        self.KEYWORD_COLOUR = self.THEMES[self.INDEX]["keyword"]
        self.DEFINITION_COLOUR = self.THEMES[self.INDEX]["definition"]

        self.WRONG_COLOUR = self.THEMES[self.INDEX]["wrong"]
        self.CORRECT_COLOUR = self.THEMES[self.INDEX]["correct"]

        # ---

        self.TYPOGRAPHY = self.settingsConfig["TYPOGRAPHY"]
        self.FLASHCARDS_FONT = (self.TYPOGRAPHY["FONT"], self.TYPOGRAPHY["FLASHCARDS SIZE"])
        self.TITLE_FONT = (self.TYPOGRAPHY["FONT"], self.TYPOGRAPHY["TITLE SIZE"], 'bold')
        self.COMMON_FONT = (self.TYPOGRAPHY["FONT"], self.TYPOGRAPHY["COMMON SIZE"])

        # ---

        self.KEYBINDS: dict = self.settingsConfig["KEYBINDS"]

    def format_keybind_string(self, action: str):
        """
        return overly complex string that allows for ever-changing keybinds
        - for given action which would like to be executed, independant of key pressed
        - action should be binded to correct function/method by developers... otherwise whats the point
        """
        try:
            int(self.KEYBINDS[f'{action}']) # checks to see whether keybind is an integer
        except ValueError:
            return f"<{self.KEYBINDS[f'{action}']}>" # if not, proceed as usual
        else: 
            return f"{self.KEYBINDS[f'{action}']}" # if so, remove angle brackets from string

    def update_settings_config(self, updated_value: dict):
        """
        changes the values within settings_config.json file

        ### Parameters
        - updated_value: dict
            - a smaller dictionary than the settings_config.json file, 
            ideally sharing select keys with different values

        a static function, usable within all files/classes, but particularly SettingsPage()
        """
        self._write_to_settings_config(
            data=self._update(
                dictionary=self.settingsConfig, 
                updated_value=updated_value
            )
        )

    def _parse_settings_config(self):
        """
        to open and later insert values of settings.json file

        ### Returns
        - config: dict
            - json file as dictionary in python
        """
        with open("my_settings_lib\\settings_config.json", 'r') as jsonFile:
            data = jsonFile.read()
        config: dict = json.loads(data)
        return config

    def _write_to_settings_config(self, data: dict):
        """
        updates and rewrites information within settings_config.json file with conventional formatting
        """
        with open("my_settings_lib\\settings_config.json", 'w') as jsonFile:
            json.dump(data, jsonFile, indent=4)

    def _update(self, dictionary: dict, updated_value: dict):
        """
        navigates settings_config dictionary and compares values within another dictionary

        replaces/updates values under congruent dictionary keys

        ### Parameters
        - dictionary: dict
            - the settings_config.json file converted into python dictionary
        - updated_value: dict
            - another dictionary, ideally sharing select keys with different values

        ### Returns
        - modified dictionary parameter

        ### Raises
        - MyOwnError: Exception | str
            - outputs incongruous keys within updated_value dict
        """
        for key, value in updated_value.items():
            if isinstance(value, collections.abc.Mapping):
                dictionary[key] = self._update(dictionary.get(key, {}), value)
            elif key in dictionary:
                dictionary[key] = value
            else:
                print(f"{__name__} file. (MyOwnError): the key and/or path to, '{key}', does not exist in settings_config.json\n")
        return dictionary