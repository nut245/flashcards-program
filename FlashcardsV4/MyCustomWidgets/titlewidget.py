import tkinter as tk
from MySettings import SettingsObj as stg

class TitleWidget(tk.Frame):
    def __init__(self, master, text, column=0, row=0, columnspan=1, rowspan=1):
        super().__init__(
            master=master,
            background=stg.BACKGROUND_COLOUR
        )
        self.grid(
            column=column, 
            row=row, 
            columnspan=columnspan, 
            rowspan=rowspan,
            sticky='news'
        )

        self.titleLabel = tk.Label(
            master=self,
            text=text,
            background=stg.ACCENT_COLOUR,
            font=stg.TITLE_FONT,
            relief='ridge',
            borderwidth=6
        )
        self.titleLabel.pack(
            expand=True, 
            fill='both', 
            padx=stg.PADX, 
            pady=stg.PADY
        )
        if stg.MODE == 'dark':
            self.titleLabel.configure(foreground=stg.DARK_TEXT_COLOUR)