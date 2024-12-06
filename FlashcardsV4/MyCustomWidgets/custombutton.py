import tkinter as tk
from MySettings import SettingsObj as stg

class CustomButton(tk.Button):
    def __init__(self, master, text, command, column=0, row=0, columnspan=1, rowspan=1):
        super().__init__(
            master=master, 
            text=text,
            command=command,
            background=stg.BUTTON_COLOUR,
            font=stg.COMMON_FONT
        )
        self.grid(
            column=column,
            row=row,
            columnspan=columnspan,
            rowspan=rowspan,
            pady=stg.PADY, 
            padx=stg.PADX, 
            sticky='news'
        )
        if stg.MODE == 'dark':
            self.configure(foreground=stg.DARK_TEXT_COLOUR)