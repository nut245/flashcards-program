import tkinter as tk

from my_custom_widgets import SubPage, TitleWidget, CustomButton, VerticalScrolledFrame
from my_settings_lib import settingsObj as stg

from .keybinds_page import KeyBindsPage
from .themes_page import ThemesPage

class SettingsPage(SubPage):
    """
    window that hosts all the user-end configurations of settings_config.json file

    #### Currently manages...
    - KeyBindsPage()
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
            command=lambda : self.show_frame("KeyBindsPage"),
            grid_enabled=False
        )
        CustomButton(
            master=self.tabsFrame,
            text='Themes',
            command=lambda : self.show_frame("ThemesPage"),
            grid_enabled=False
        )

        CustomButton( # restart button
            master=self,
            text="save and restart",
            command=self._save_and_restart,
            column=0, row=2
        )

        self.frames: dict[str, tk.Frame | KeyBindsPage | ThemesPage] = {}
        for F in (KeyBindsPage, ThemesPage):
            page_name = F.__name__
            frame = F(master=self)
            self.frames[page_name] = frame
            frame.grid(column=1, row=0, rowspan=3, sticky='news')

        self.show_frame("KeyBindsPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        for frame in self.frames.values():
            frame.grid_forget()

        frame = self.frames[page_name]
        frame.grid(column=1, row=0, rowspan=3, sticky='news')
        frame.focus_force()

    def _save_and_restart(self):
        stg.update_settings_config(
            {
                "INDEX": self.frames["ThemesPage"].retrieve_chosen_theme_index()
            })

        stg.update_settings_config(
            self.frames["KeyBindsPage"].retrieve_updated_keybinds()
        )

        self.master.recreate_main()