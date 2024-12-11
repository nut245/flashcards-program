"""
Found and used only within SettingsPage()
"""

import tkinter as tk
from my_settings_lib import settingsObj as stg

from .universal_widgets.custom_frame import CustomFrame
from .universal_widgets.custom_button import CustomButton
from .universal_widgets.custom_label import CustomLabel
from .universal_widgets.title_widget import TitleWidget

class KeyBindsWidget(CustomFrame):
    def __init__(self, master, action, keybind, column=0, row=0, columnspan=1, rowspan=1, grid_enabled=True):
        """
        tk.Frame() that resembles MyCustomWidgets.universal_widgets.OptionWidget

        used to display and edit keybinds for entire program

        ### Parameters
        - master: SettingsPage()
            - solely for placing into SettingsPage()
        - action: str
            - the action/command that would like to be performed after pressing keybind
        - keybind: str
            - the (combination of) buttons to press to begin an action
        - column, row: int, int
            - the placement of the widget
        - columnspan, rowspan: int, int
            - the number of columns and rows this widget takes up
        - grid_enabled: bool
            - determines whether to put widget onto screen with grid or pack manager
        """
        super().__init__(
            master=master,
            column=column,
            row=row,
            columnspan=columnspan,
            rowspan=rowspan,
            grid_enabled=grid_enabled
        )
        self.action = action
        self.keybind = keybind

        self.grid_columnconfigure((0,1), weight=2)
        self.grid_columnconfigure((2), weight=1)
        self.grid_rowconfigure((0), weight=1)

        self.actionLabel = CustomLabel(
            master=self,
            text=self.action,
            row=0, column=0
        )
        self.actionLabel.configure(
            width=20, 
            borderwidth=4,
            relief='sunken'
        )

        self.keybindLabel = CustomLabel(
            master=self,
            text=self.keybind,
            row=0, column=1
        )
        self.keybindLabel.configure(
            width=10
        )

        self.editButton = CustomButton(
            master=self,
            text="Edit",
            command= self.popup,
            row=0, column=2
        )

    def popup(self):
        Popup(self)

# code for Popup() already written, ever so generously, on https://pastebin.com/XKNGvVhk
# found from https://www.reddit.com/r/learnpython/comments/5q8v8g/trying_to_create_rebindable_keybindings_in/
class Popup(tk.Toplevel):
    def __init__(self, master: KeyBindsWidget):
        """
        Only purpose in life is to take input from user regarding the type and combination of key pressed

        Note that...
        - creation of Popup() does not allow the destruction or interaction of any other windows open
        - it does not have any properties accessable by developer
        """
        super().__init__(master=master, background=stg.BACKGROUND_COLOUR)
        self.master: KeyBindsWidget = master
        self.geometry(f'275x200+{(self.winfo_screenwidth() // 2 - self.winfo_width()) // 8}+{(self.winfo_screenheight() // 2 - self.winfo_height()) // 8}')
        self.resizable(False, False)
        self.focus_force()

        self.key=None
        self.bind("<Key>", self._key_press)

        TitleWidget(
            master=self,
            text="Press a key combination",
            grid_enabled=False
        ).titleLabel.configure(
            font=(stg.TITLE_FONT[0], stg.TITLE_FONT[1]-25, stg.TITLE_FONT[2])
        )

        self.key_lbl = CustomLabel(
            master=self,
            text=None,
            grid_enabled=False
        )

        CustomButton(
            master=self,
            text='OK',
            command=self._quit,
            grid_enabled=False
        )

        CustomButton(
            master=self, 
            text="Cancel", 
            command=self._return,
            grid_enabled=False
        )

        # The following commands keep the popup on top.
        self.transient(master)      # set to be on top of the main window
        self.grab_set()             # hijack all commands from the master (clicks on the main window are ignored)
        master.wait_window(self)    # pause anything on the main window until this one closes

    def _quit(self):
        if self.key:
            self.master.keybind = self.key
            self.master.keybindLabel.configure(text=self.master.keybind)
        self.destroy()

    def _key_press(self, event: tk.Event=None):
        if not event.keysym.startswith(("Control", "Shift", "Alt")):
            self.key = self._event_to_keytext(event)
            self.key_lbl.configure(text=self.key)

    def _event_to_keytext(self, event: tk.Event):
        keys = []
        if event.state & 1:
            keys.append("Shift")
        if event.state & 4:
            keys.append("Control")
        if event.state & 136:
            keys.append("Alt")
        keys.append(event.keysym)
        return "-".join(keys)
    
    def _return(self):
        self.master.focus_force()
        self.destroy()