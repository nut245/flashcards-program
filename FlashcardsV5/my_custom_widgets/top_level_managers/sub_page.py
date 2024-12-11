import tkinter as tk
from my_settings_lib import settingsObj as stg
from ..universal_widgets.custom_frame import CustomFrame

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import Main

class SubPage(tk.Toplevel):
    """
    tk.Toplevel() window given more functionality for management

    Meant as an abstract class to give inherent access to Main()'s flashcards attribute

    Deals with edge-cases alongside TopLevelButton() with the usage of self.return_to_main()
    """
    def __init__(self, master = None):
        """
        ### Parameters
        - master: Main()
            - to access static methods
            - for clearence of all windows, on Main()'s destruction

        ### Properties
        - self.return_to_main()
            - destroys instance of SubPage child class
            - accessed only within SubPage, which has its complications
            and TopLevelButton()
        - self.create_flashcards_frame(self, master, column=0, row=0)
            - master: tk.Frame | tk.Widget
                - to place flashcards into, within a new window
            - column, row: int, int
                - the position of the flashcards within new frame/widget
        - self.flashcardsFrame: tk.Frame
            - able to re-orient flashcards, and access other aesthetic attributes

        ### Returns
        - tk.Toplevel()
        """
        self.master: Main = master

        super().__init__(master=self.master, background=stg.BACKGROUND_COLOUR)
        self.title('Toplevel Application')
        # to offset subpage's position from main, to the top left corner on its instantiation
        self.geometry(f'600x400+{(self.winfo_screenwidth() // 2 - self.winfo_width()) // 4}+{(self.winfo_screenheight() // 2 - self.winfo_height()) // 4}')

        self.focus_force()

        self.bind('<Escape>', lambda _ : self.return_to_main())

        self.protocol("WM_DELETE_WINDOW", self.return_to_main)

    def return_to_main(self):
        """
        - destroys the instance of child object (within memory and Main().frames dictionary)
        - gives focus to Main() window
        """
        self.master.focus_force()
        self.destroy()
        try:
            self.master.frames[str(self)[2:].upper().rstrip("0123456789")] = None
        except AttributeError: 
            # either the error above occurs due to negligence from developer, 
            # or a subpage was not connected to Main(), instead child of Main()
            pass # print(f"({__name__}) file. (MyOwnError): master attribute was not passed\n")

    def create_flashcards_frame(self, master, column=0, row=0):
        """
        re-orients flashcards into desired page
        """
        self.flashcardFrame = CustomFrame(
            master=master,
            column=column, row=row, columnspan=2
        )

        self.master.recreate_flashcards(flashcardsParent=self.flashcardFrame)

        if self.master.importedFlashcards != None:
            self.importedFlashcards = self.master.importedFlashcards
            self.flashcards = self.master.flashcards