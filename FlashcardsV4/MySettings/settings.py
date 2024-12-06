import json
import collections.abc

class Settings():
    def __init__(self):
        self.refresh_values()

    def refresh_values(self):
        self.settingsConfig = self.parse_settings_config()
        
        self.INDEX = self.settingsConfig["INDEX"]

        self.TYPOGRAPHY = self.settingsConfig["TYPOGRAPHY"]

        self.PADX = self.settingsConfig["PADX"]
        self.PADY = self.settingsConfig["PADY"]

        self.THEMES = self.settingsConfig["THEMES"]

        self.MODE = self.THEMES[self.INDEX]["mode"]
        self.DARK_TEXT_COLOUR = self.settingsConfig["DARK TEXT COLOUR"]

        self.BACKGROUND_COLOUR = self.THEMES[self.INDEX]["background"]
        self.FRAME_COLOUR = self.THEMES[self.INDEX]["frame"]
        self.ACCENT_COLOUR = self.THEMES[self.INDEX]["accent"]
        self.BUTTON_COLOUR = self.THEMES[self.INDEX]["button"]

        self.KEYWORD_COLOUR = self.THEMES[self.INDEX]["keyword"]
        self.DEFINITION_COLOUR = self.THEMES[self.INDEX]["definition"]
        self.FLASHCARDS_FONT = (self.TYPOGRAPHY["FONT"], self.TYPOGRAPHY["FLASHCARDS SIZE"])

        self.WRONG_COLOUR = self.THEMES[self.INDEX]["wrong"]
        self.CORRECT_COLOUR = self.THEMES[self.INDEX]["correct"]

        self.TITLE_FONT = (self.TYPOGRAPHY["FONT"], self.TYPOGRAPHY["TITLE SIZE"], 'bold')
        self.COMMON_FONT = (self.TYPOGRAPHY["FONT"], self.TYPOGRAPHY["COMMON SIZE"])

    def parse_settings_config(self):
        with open("MySettings\\settingsconfig.json", 'r') as jsonFile:
            data = jsonFile.read()
        config: dict = json.loads(data)
        return config
    
    def update_settings_config(self, updated_value):
        self._write_to_settings_config(
            data=self._update(
                dictionary=self.settingsConfig, 
                updated_value=updated_value
            )
        )

    def _write_to_settings_config(self, data: dict):
        with open("MySettings\\settingsconfig.json", 'w') as jsonFile:
            json.dump(data, jsonFile, indent=4)

    def _update(self, dictionary: dict, updated_value: dict):
        for key, value in updated_value.items():
            if isinstance(value, collections.abc.Mapping):
                dictionary[key] = self._update(dictionary.get(key, {}), value)
            elif key in dictionary:
                dictionary[key] = value
            else:
                print(f"{__name__} file. (MyOwnError): the key and/or path to, '{key}', does not exist in settingsconfig.json\n")
        return dictionary