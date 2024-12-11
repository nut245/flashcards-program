import tkinter as tk
from my_settings_lib import settingsObj as stg
from .custom_frame import CustomFrame

class OptionWidget(CustomFrame):
    """
    Traditional user-input-prompt widget

    Displays text for desired user input
    and entry for easy access to user input

    ### Parameters
    - parent: tk.Frame() | tk.Widget()
        - to place widget into
    - text: str
        - to prompt users with
    - column, row: int, int
        - the position of this widget, using solely grid
    """
    def __init__(self, parent, text, column=0, row=0, grid_enabled=True):
        """
        ### Properties
        - self.label: tk.Label
            - displays text
        - self.entry: tk.Entry
            - self.entry.get() to access user input
        
        able to access all tkinter attributes/methods within both

        ### Returns
        - tk.Frame object
            - styled with data in settings_config.json
        """
        self.text = text
        self.parent = parent

        super().__init__(
            master=self.parent,
            column=column, row=row,
            grid_enabled=grid_enabled
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