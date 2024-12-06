import tkinter as tk
from MySettings import SettingsObj as stg
from .customframe import CustomFrame
from .customlabel import CustomLabel

class OptionWidget(CustomFrame):
    def __init__(self, parent, text, column, row):
        self.text = text
        self.parent = parent

        super().__init__(
            master=self.parent,
            column=column, row=row
        )

        self.label = tk.Label(
            master=self, 
            text=self.text, 
            width=20, 
            background=stg.ACCENT_COLOUR, 
            font=stg.COMMON_FONT,
            borderwidth=4,
            relief='sunken'
        )
        self.label.pack(fill='both', expand=True, side='left', padx=stg.PADX, pady=stg.PADY)

        self.entry = tk.Entry(
            master=self, 
            width=20, 
            background=stg.KEYWORD_COLOUR, 
            font=stg.COMMON_FONT
        )
        self.entry.pack(fill='both', expand=True, side='left', padx=stg.PADX, pady=stg.PADY)
        if stg.MODE == 'dark':
            self.label.configure(foreground=stg.DARK_TEXT_COLOUR)
            self.entry.configure(foreground=stg.DARK_TEXT_COLOUR)