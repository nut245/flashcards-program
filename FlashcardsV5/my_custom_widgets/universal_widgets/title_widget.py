import tkinter as tk
from my_settings_lib import settingsObj as stg

class TitleWidget(tk.Frame):
    def __init__(self, master, text, column=0, row=0, columnspan=1, rowspan=1, grid_enabled=True):
        """
        Dynamically styled tk.Frame widget for titles/headings

        ### Parameters
        - master: Main()
            - to access static methods/attributes
            - to place widget into
        - text: str
            - the title text to display
        - column, row: int, int
            - the position of this widget, using solely grid method
        - columnspan, rowspan: int, int
            - how many rows and columns the widget expands

        ### Attributes
        - titleLabel: tk.Label()
            - inner label widget which displays text

        ### Returns
        - tk.Frame() object
            - styled with data in settings_config.json
        
        """
        super().__init__(
            master=master,
            background=stg.BACKGROUND_COLOUR
        )
        if grid_enabled:
            self.grid(
                column=column, 
                row=row, 
                columnspan=columnspan, 
                rowspan=rowspan,
                sticky='news'
            )
        else:
            self.pack(expand=True, fill='both', padx=stg.PADX, pady=stg.PADY)

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