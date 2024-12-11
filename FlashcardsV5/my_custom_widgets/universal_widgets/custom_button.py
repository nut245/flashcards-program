import tkinter as tk
from my_settings_lib import settingsObj as stg

class CustomButton(tk.Button):
    def __init__(self, master, text, command, column=0, row=0, columnspan=1, rowspan=1, grid_enabled=True):
        """
        Dynamically styled tk.Button widget to hold other widgets

        ### Parameters
        - master: Main()
            - to access static methods/attributes
            - to place widget into
        - text: int, int
            - the title text to display
        - command: Callable
            - function to be run on user input
        - column, row: int, int
            - the position of this widget, using solely grid
        - columnspan, rowspan: int, int
            - how many rows and columns the widget expands

        ### Returns
        - tk.Button object
            - styled with data in settings_config.json
        """
        super().__init__(
            master=master, 
            text=text,
            command=command,
            background=stg.BUTTON_COLOUR,
            font=stg.COMMON_FONT
        )
        if grid_enabled:
            self.grid(
                column=column,
                row=row,
                columnspan=columnspan,
                rowspan=rowspan,
                pady=stg.PADY, 
                padx=stg.PADX, 
                sticky='news'
            )
        else:
            self.pack(
                expand=True,
                fill='both',
                pady=stg.PADY, 
                padx=stg.PADX
            )
        if stg.MODE == 'dark':
            self.configure(foreground=stg.DARK_TEXT_COLOUR)