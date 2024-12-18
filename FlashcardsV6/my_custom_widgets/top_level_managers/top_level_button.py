import tkinter as tk
from my_settings_lib import settingsObj as stg
from ..universal_widgets.custom_button import CustomButton

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import Main

class TopLevelButton(CustomButton):
    """
    Styled tk.Button widget that manages the existence of tk.Toplevel windows stemming from Main()

    Accesses Main()'s frames attribute, which stores all SubPage() child objects

    ### Parameters
    - main: Main()
        - to access static methods/attributes
    - parent: tk.Frame() | CustomFrame()
        - to place widget into
    - file: SubPage()
        - to associate TopLevelButton() to a SubPage() child object
    - text: str
        - the title text to display
    - column, row: int, int
        - the position of this widget, using solely grid method
    - columnspan, rowspan: int, int
        - how many rows and columns the widget expands

    ### Returns
    - tk.Button() object
        - styled with data in settings_config.json
    """
    def __init__(self, controller, parent, text, column, row, columnspan=1, rowspan=1, file=None, flashcardsDependant=True):
        self.main: Main = controller
        self.file = file
        self.flashcardsDependant = flashcardsDependant
        self.fileString = file.__name__.upper()

        super().__init__(
            master=parent, 
            text=text, 
            command=self.open_subpage,
            column=column, 
            row=row, 
            columnspan=columnspan, 
            rowspan=rowspan,
        )

    def open_subpage(self):
        """
        Manager function to check...
        - if desired window is open -> gives focus to such window
        - if all windows are closed -> opens the desired window
        - if desired window is not open and other may be -> closes all windows and opens desired window
        """
        stg.refresh_values()

        frame_open = False
        for subPage in self.main.frames.values():
            if not subPage == None:
                frame_open = True
                break

        if not frame_open:
            if self.flashcardsDependant:
                if self.main.importedFlashcards == None:    # remove these two lines of code
                    self.main.import_flashcards()           # if developer would not like to invite importing new flashcards
                
                if self.main.importedFlashcards == None:
                    return
                
            self.main.frames[self.fileString] = self.file(master=self.main) # instantiating subpage child object

        try:
            self.main.frames[self.fileString].focus_force()
        except: 
        # for if there was an attempt to open another window
        # as the previous check did not pass, meaning there was no need to open a new file (the current file)
        # hence how can you focus_force() the current file, that does not exist?
            for subPage in self.main.frames.values():
                try:
                    subPage.return_to_main()
                except: # to clear all instances of a window, regardless of existence
                    pass
            
            self.open_subpage()