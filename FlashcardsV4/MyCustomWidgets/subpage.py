import tkinter as tk
from MySettings import SettingsObj as stg
from .customframe import CustomFrame

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import Main

class SubPage(tk.Toplevel):
    """"
    some more documentation
    """
    def __init__(self, master = None):
        self.master: Main = master

        super().__init__(master=self.master, background=stg.BACKGROUND_COLOUR)
        self.title('Toplevel Application')
        self.geometry(f'600x400+{(self.winfo_screenwidth() // 2 - self.winfo_width()) // 4}+{(self.winfo_screenheight() // 2 - self.winfo_height()) // 4}')

        self.focus_force()

        self.bind('<Escape>', lambda _ : self.return_to_main())

        self.protocol("WM_DELETE_WINDOW", self.return_to_main)

        if self.master.importedFlashcards == None:
            self.return_to_main()

    def return_to_main(self):
        self.master.focus_force()
        self.destroy()
        try:
            self.master.frames[str(self)[2:].upper().rstrip("0123456789")] = None
        except AttributeError:
            print(f"({__name__}) file. (MyOwnError): master attribute was not passed\n")

    def create_flashcards_frame(self, master, column=0, row=0):
        self.flashcardFrame = CustomFrame(
            master=master,
            column=column, row=row, columnspan=2
        )
            
        self.master.recreate_flashcards(self.flashcardFrame)

        if self.master.importedFlashcards != None:
            self.importedFlashcards = self.master.importedFlashcards
            self.flashcards = self.master.flashcards