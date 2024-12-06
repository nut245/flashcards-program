import tkinter as tk
from MySettings import SettingsObj as stg

class CustomFrame(tk.Frame):
    def __init__(self, master, column, row, columnspan=1, rowspan=1):
        super().__init__(
            master=master,
            background=stg.FRAME_COLOUR
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