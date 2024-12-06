import tkinter as tk

from MyCustomWidgets import SubPage, TitleWidget, CustomFrame, CustomButton, CustomLabel
from MySettings import SettingsObj as stg

class SettingsPage(SubPage):
    def __init__(self, master):
        super().__init__(master=master)
        self.title("Settings")

        self.grid_columnconfigure((0), weight=1)
        self.grid_columnconfigure((1), weight=10)
        self.grid_rowconfigure((0), weight=2)
        self.grid_rowconfigure((1), weight=10)
        self.grid_rowconfigure((2), weight=1)

        TitleWidget(
            master=self,
            text="Settings"
        ).titleLabel.configure(
            font=(stg.TITLE_FONT[0], stg.TITLE_FONT[1]-10, stg.TITLE_FONT[2])
        )

        self.tabsFrame = CustomFrame(
            master=self,
            column=0, row=1
        )

        self.controlsFrame = CustomFrame(
            master=self,
            column=1, row=0, rowspan=3
        )

        CustomLabel(
            master=self.controlsFrame,
            text='settings page needs to...\n- allow configuration of all options in "settingsconfig.json"\n\t- include settings to configure\n- selection of themes\n- customisable keybinds',
            largetexttype=2,
        )

        CustomButton( # restart button
            master=self,
            text="save and restart",
            command=self.my_command,
            column=0, row=2
        )

    def my_command(self):
        stg.INDEX += 1
        if stg.INDEX > len(stg.THEMES)-1:
            stg.INDEX = 0
        stg.update_settings_config(
            {
                "INDEX": stg.INDEX
            })

        stg.update_settings_config(
            {
                "TYPOGRAPHY": {
                    "FONT": "Arial"
                }
            })

        self.master.recreate_main()