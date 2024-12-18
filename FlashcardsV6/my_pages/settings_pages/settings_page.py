import tkinter as tk

from my_custom_widgets import SubPage, TitleWidget, CustomButton, VerticalScrolledFrame, EmbeddedPages
from my_settings_lib import settingsObj as stg

from .keybinds_page import KeyBindsPage
from .themes_page import ThemesPage

class SettingsPage(SubPage):
    """
    window that hosts all the user-end configurations of settings_config.json file

    #### Currently manages...
    - KeyBindsPage()
    - ThemesPage()
    """
    def __init__(self, master):
        super().__init__(master=master)
        self.title("Settings")

        self.grid_columnconfigure((0), weight=1)
        self.grid_columnconfigure((1), weight=10)
        self.grid_rowconfigure((0), weight=2)
        self.grid_rowconfigure((1), weight=10)
        self.grid_rowconfigure((2), weight=1)

        self.allowed_keybinds = []

        TitleWidget(
            master=self,
            text="Settings"
        ).titleLabel.configure(
            font=(stg.TITLE_FONT[0], stg.TITLE_FONT[1]-10, stg.TITLE_FONT[2])
        )

        self.tabsFrame = VerticalScrolledFrame(
            parent=self,
            column=0, row=1
        ).interior

        CustomButton(
            master=self.tabsFrame,
            text='KeyBinds',
            command=lambda : self.embeddedPages.show_frame("KeyBindsPage"),
            grid_enabled=False
        )
        CustomButton(
            master=self.tabsFrame,
            text='Themes',
            command=lambda : self.embeddedPages.show_frame("ThemesPage"),
            grid_enabled=False
        )

        CustomButton( # restart button
            master=self,
            text="save and restart",
            command=self._save_and_restart,
            column=0, row=2
        )

        self.embeddedPages = EmbeddedPages(
            controller=self,
            pages=[KeyBindsPage, ThemesPage],
            column=1, row=0, rowspan=3
        )

        self.embeddedPages.show_frame("KeyBindsPage")

    def _save_and_restart(self):
        stg.update_settings_config(
            {
                "INDEX": self.embeddedPages.frames["ThemesPage"].retrieve_chosen_theme_index()
            })

        stg.update_settings_config(
            self.embeddedPages.frames["KeyBindsPage"].retrieve_updated_keybinds()
        )

        self.master.recreate_main()