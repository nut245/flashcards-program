import tkinter as tk
from MySettings import SettingsObj as stg

class CustomLabel(tk.Label):
    def __init__(self, master, text, column=0, row=0, columnspan=1, rowspan=1, largetexttype=False, bold=False, grid_enabled=True):
        """
        Dynamically styled tk.Label widget to display text

        ### Parameters
        - master: Main()
            - to access static methods/attributes
            - to place widget into
        - text: str
            - text to display
        - largetexttype: False | int
            - False used for widget text
            - currently 1 or 2
            - for text...
                1. blocked into smaller frames
                2. for standalone text
        - column, row: int, int
            - the position of this widget, using solely grid
        - columnspan, rowspan: int, int
            - how many rows and columns the widget expands

        ### Returns
        - tk.Frame object
            - styled with data in settingsconfig.json
        """
        super().__init__(
            master=master,
            text=text,
            background=stg.ACCENT_COLOUR,
            font=stg.COMMON_FONT
        )
        if grid_enabled:
            self.grid(
                column=column, 
                row=row,
                columnspan=columnspan,
                rowspan=rowspan,
                sticky='news', 
                padx=stg.PADX, 
                pady=stg.PADY
            )
        else:
            self.pack(expand=True, fill='both', padx=stg.PADX, pady=stg.PADY)

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