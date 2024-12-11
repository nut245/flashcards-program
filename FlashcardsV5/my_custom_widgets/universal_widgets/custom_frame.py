import tkinter as tk
from my_settings_lib import settingsObj as stg

class CustomFrame(tk.Frame):
    def __init__(self, master, column=0, row=0, columnspan=1, rowspan=1, grid_enabled=True):
        """
        Dynamically styled tk.Frame widget to hold other widgets

        ### Parameters
        - master: Main()
            - to access static methods/attributes
            - to place widget into
        - column, row: int, int
            - the position of this widget, using solely grid
        - columnspan, rowspan: int, int
            - how many rows and columns the widget expands

        ### Returns
        - tk.Frame object
            - styled with data in settings_config.json
        """
        super().__init__(
            master=master,
            background=stg.FRAME_COLOUR
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