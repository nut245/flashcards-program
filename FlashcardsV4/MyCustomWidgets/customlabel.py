import tkinter as tk
from MySettings import SettingsObj as stg

class CustomLabel(tk.Label):
    def __init__(self, master, text, column=0, row=0, columnspan=1, rowspan=1, largetexttype=False, bold=False):
        super().__init__(
            master=master,
            text=text,
            background=stg.ACCENT_COLOUR,
            font=stg.COMMON_FONT
        )
        self.grid(
            column=column, 
            row=row,
            columnspan=columnspan,
            rowspan=rowspan,
            sticky='news', 
            padx=stg.PADX, 
            pady=stg.PADY
        )
        if stg.MODE == 'dark':
            self.configure(foreground=stg.DARK_TEXT_COLOUR)
        if largetexttype == 1:
            self.configure(
                justify='left', 
                width=5, 
                anchor='w'
            )
        elif largetexttype == 2:
            self.configure(
                justify='left', 
                anchor='w'
            )
        if bold:
            self.configure(font=(stg.COMMON_FONT[0], stg.COMMON_FONT[1], 'bold'))