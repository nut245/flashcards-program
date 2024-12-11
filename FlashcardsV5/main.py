import tkinter as tk
from my_flashcards_lib import *
from my_custom_widgets import TopLevelButton, TitleWidget, CustomFrame
from my_custom_widgets import CustomButton # to be replaced with TopLevelButtons
from my_pages import *

from my_settings_lib import settingsObj as stg

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from my_custom_widgets import SubPage

class Main(tk.Tk):
    """
    The main application, which manages all subsequent objects within program.

    All instances of classes stem from main, primarily sharing access to its 
    flashcards attribute.

    All methods defined within main are treated statically.
    """
    def __init__(self, importedFlashcards: ImportFlashcards | None = None):
        """
        ### Parameters
        - importedFlashcards: ImportFlashcards | None
            - importedFlashcards argument is passed in instantiation of Main, within recreate_main() method
            to avoid repeated importing by user
            
        ### Returns
        - tk.Tk() object
        """
        super().__init__()
        self.title('Main Application')
        # to center main application on its instantiation
        self.geometry(f'600x400+{(self.winfo_screenwidth() // 2 - self.winfo_width()) // 2}+{(self.winfo_screenheight() // 2 - self.winfo_height()) // 2}')
        self.configure(background=stg.BACKGROUND_COLOUR)

        self.importedFlashcards: ImportFlashcards | None = importedFlashcards
        self.flashcards = None
        
        self.grid_columnconfigure((0), weight=1)
        self.grid_columnconfigure((1), weight=10)

        self.grid_rowconfigure((0), weight=1)
        self.grid_rowconfigure((1), weight=2)

        TitleWidget(
            master=self,
            text="QUIZ-IMI",
            columnspan=2)

        self.menuFrame = CustomFrame(
            master=self,
            column=1, row=1)
        
        self.menuFrame.grid_columnconfigure((0,1), weight=1)
        self.menuFrame.grid_rowconfigure((0,1,2), weight=1)

        self.pageButtons: dict[str, TopLevelButton] = {}

        self.pageButtons["Play Flashcards"] = TopLevelButton(
            controller=self, 
            parent=self.menuFrame,
            text=f"Play Flashcards [{stg.KEYBINDS['play flashcards']}]", 
            file=PlayFlashcardsPage, 
            column=0, columnspan=2, row=0)

        self.pageButtons["Test Your Knowledge"] = TopLevelButton(
            controller=self, 
            parent=self.menuFrame,
            text=f"Test Your Knowledge [{stg.KEYBINDS['test your knowledge']}]", 
            file=PageTwo, 
            column=0, columnspan=2, row=1)

        self.create_frames_dictionary()

        self.importButton = CustomButton(
            master=self.menuFrame,
            text=f"Import New Flashcards [{stg.KEYBINDS['import flashcards']}]",
            command=self.import_flashcards,
            column=0, row=2)

        # TODO : make exportable flashcards, into whatever format
        self.exportButton = CustomButton(
            master=self.menuFrame,
            text='Export Flashcards To...',
            command=lambda : ExportPage(master=self),
            column=1, row=2)

        self.settingsFrame = CustomFrame(
            master=self,
            column=0, row=1)

        self.settingsFrame.grid_columnconfigure((0), weight=1)
        self.settingsFrame.grid_rowconfigure((0,1), weight=1)

        self.pageButtons["Settings"] = TopLevelButton(
            controller=self, 
            parent=self.settingsFrame,
            text=f"Settings", 
            file=SettingsPage, 
            flashcardsDependant=False,
            column=0, row=0)

        # TODO : make view decks button work
        self.viewDecksButton = CustomButton(
            master=self.settingsFrame,
            text="View Decks",
            command=lambda : print("TODO : make view decks button work"),
            column=0, row=1)

        self.focus_force()

        self.bind(stg.format_keybind_string("play flashcards"), lambda _ : self.pageButtons["Play Flashcards"].open_subpage())
        self.bind(stg.format_keybind_string("test your knowledge"), lambda _ : self.pageButtons["Test Your Knowledge"].open_subpage())
        self.bind(stg.format_keybind_string("import flashcards"), lambda _ : self.import_flashcards())

    def create_frames_dictionary(self):
        """
        sets up frames dictionary to be accessed by TopLevelButtons
        - each key is an upper()'d string of each file (being a child class of SubPage) 
        - each value is a child class of the abstract SubPage class
        """
        self.frames: dict[str, SubPage] = {}
        listOfFiles = []
        for button in self.pageButtons:
            listOfFiles.append(self.pageButtons[button].file)

        for file in listOfFiles:
            self.frames[file.__name__.upper()] = None

    def recreate_flashcards(self, flashcardsParent = None):
        """
        #### TODO: functionality should be moved into new class for more control over importation
        called only when importing a new set of flashcards

        totally recreates flashcards object, with whatever file was imported by user last
        - has the added bonus of re-orienting flashcards onto new window, on their re-creation
        """
        try:
            if flashcardsParent is None:
                self.flashcards = Flashcards(dictionary=self.importedFlashcards.dictionary)
            else:
                self.flashcards = Flashcards(master=flashcardsParent, dictionary=self.importedFlashcards.dictionary)
                self.flashcards.pack(expand=True, fill='both')
        except IndexError:
            self.importedFlashcards = None

    def import_flashcards(self):
        """
        #### TODO: functionality should be moved into new class for more control over importation
        performs checks as to whether flashcards exist, 
        as well as whether importation was successful in retrieving a file directory.
        """
        if self.importedFlashcards != None:
            self.importedFlashcards.create_dictionary()
        else:
            self.importedFlashcards = ImportFlashcards()
            self.recreate_flashcards()
        
        if self.importedFlashcards == None:
            print(f"({__name__}) file. (MyOwnError): why didn't you choose a file.\n")

    def recreate_main(self):
        """
        the class is given access to its only object (inherently being a singleton).
        This is done to destroy its only instance and create another.
        
        only called within [my_settings\settings.py] to reset all default values
        after changes are made within [my_settings\settings_config.json]
        """
        global main
        try:
            main.destroy()
        except:
            pass
        stg.refresh_values()
        main = Main(importedFlashcards=self.importedFlashcards)
        main.mainloop()

if __name__ == '__main__':
    main = Main()

    main.mainloop()