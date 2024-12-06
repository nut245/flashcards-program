import tkinter as tk
from MySettings import SettingsObj as stg
from .custombutton import CustomButton

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import Main

class TopLevelButton(CustomButton):
    def __init__(self, controller, parent, text, column, row, columnspan=1, rowspan=1, file=None):
        self.controller: Main = controller
        self.file = file
        self.fileString = file.__name__.upper()

        super().__init__(
            master=parent, 
            text=text, 
            command=self.configure_command,
            column=column, 
            row=row, 
            columnspan=columnspan, 
            rowspan=rowspan,
        )

    def configure_command(self):
        stg.refresh_values()
        frame_open = False

        for subPage in self.controller.frames.values():
            if subPage:
                frame_open = True
                break

        if not frame_open:
            try:
                self.controller.frames[self.fileString] = self.file(master=self.controller)
            except tk.TclError as e: # = "bad window path name"
                # return_to_main() was called the instant the window existed,
                # within SubPage class - due to flashcards not yet existing.
                # Hence the instantiation of SubPage child windows are abrupted,
                # causing this error.
                print(f"({__name__}) file. (MyOwnError): flashcards do not exist")#... or possibly: {e}\n")
                return

        try:
            self.controller.frames[self.fileString].focus_force()
        except: # for if there was an attempt to open another window
            for subPage in self.controller.frames.values():
                try:
                    subPage.return_to_main()
                except: # to clear all instances of a window, regardless of existence
                    pass
            self.configure_command()