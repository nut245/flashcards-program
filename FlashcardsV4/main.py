import tkinter as tk
from MyFlashcardsLib import *
from MyCustomWidgets import TopLevelButton, TitleWidget, CustomFrame
from MyCustomWidgets import CustomButton
from MyPages import *

from MySettings import SettingsObj as stg

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from MyCustomWidgets import SubPage

class Main(tk.Tk):
    def __init__(self, importedFlashcards = None):
        super().__init__()
        self.title('Main Application')
        self.geometry(f'600x400+{(self.winfo_screenwidth() // 2 - self.winfo_width()) // 2}+{(self.winfo_screenheight() // 2 - self.winfo_height()) // 2}')
        self.configure(background=stg.BACKGROUND_COLOUR)

        self.importedFlashcards: None | ImportFlashcards = importedFlashcards
        self.flashcards = None
        
        self.grid_columnconfigure((0), weight=1)
        self.grid_columnconfigure((1), weight=10)

        self.grid_rowconfigure((0), weight=1)
        self.grid_rowconfigure((1), weight=2)

        TitleWidget(
            master=self,
            text="QUIZ-IMI",
            columnspan=2
        )

        self.menuFrame = CustomFrame(
            master=self,
            column=1, row=1
        )
        self.menuFrame.grid_columnconfigure((0,1), weight=1)
        self.menuFrame.grid_rowconfigure((0,1,2), weight=1)

        self.pageButtons: dict[str, TopLevelButton] = {}

        self.pageButtons["Page 1"] = TopLevelButton(
            controller=self, 
            parent=self.menuFrame,
            text="[P]lay Flashcards", 
            file=PageOne, 
            column=0, columnspan=2, row=0
        )

        self.pageButtons["Test Your Knowledge"] = TopLevelButton(
            controller=self, 
            parent=self.menuFrame,
            text="[T]est Your Knowledge", 
            file=PageTwo, 
            column=0, columnspan=2, row=1
        )

        self.create_frames_dictionary()

        self.importButton = CustomButton(
            master=self.menuFrame,
            text='[I]mport New Flashcards',
            command=self.import_flashcards,
            column=0, row=2
        )

        self.exportButton = tk.Button(
            master=self.menuFrame,
            text="Export Flashcards To...",
            # TODO : make exportable flashcards, into whatever format
            command=lambda : print("TODO : make exportable flashcards, into whatever format"),
            background=stg.BUTTON_COLOUR,
            font=stg.COMMON_FONT
        ).grid(column=1, row=2, pady=stg.PADY, padx=stg.PADX, sticky='news')

        self.settingsFrame = CustomFrame(
            master=self,
            column=0, row=1
        )

        self.settingsFrame.grid_columnconfigure((0), weight=1)
        self.settingsFrame.grid_rowconfigure((0,1), weight=1)

        self.pageButtons["Settings"] = TopLevelButton(
            controller=self, 
            parent=self.settingsFrame,
            text="Settings", 
            file=SettingsPage, 
            column=0, row=0
        )

        self.viewDecksButton = tk.Button(
            master=self.settingsFrame,
            text="View Decks",
            # TODO : make view decks button work
            command=lambda : print("TODO : make view decks button work"),
            background=stg.BUTTON_COLOUR,
            font=stg.COMMON_FONT
        ).grid(column=0, row=1, pady=stg.PADY, padx=stg.PADX, sticky='news')

        self.focus_force()

        self.bind("<p>", lambda _ : self.pageButtons["Page 1"].configure_command())
        self.bind("<t>", lambda _ : self.pageButtons["Test Your Knowledge"].configure_command())
        self.bind("<i>", lambda _ : self.import_flashcards())

        self.bind("<Configure>", lambda _ : print("i detected this"))

    def create_frames_dictionary(self):
        self.frames: dict[str, SubPage] = {}
        listOfFiles = []
        for button in self.pageButtons:
            listOfFiles.append(self.pageButtons[button].file)

        for file in listOfFiles:
            self.frames[file.__name__.upper()] = None

    def recreate_flashcards(self, flashcardsParent = None):
        try:
            self.flashcards.destroy()
            self.flashcards = None
        except: pass

        try:
            if flashcardsParent is None:
                self.flashcards = Flashcards(dictionary=self.importedFlashcards.dictionary)
            else:
                self.flashcards = Flashcards(master=flashcardsParent, dictionary=self.importedFlashcards.dictionary)
                self.flashcards.pack(expand=True, fill='both')
        except:
            self.importedFlashcards = None

    def recreate_main(self):
        global main
        try:
            main.destroy()
        except:
            pass
        stg.refresh_values()
        main = Main(importedFlashcards=self.importedFlashcards)
        main.mainloop()

    def import_flashcards(self):
        if self.importedFlashcards != None:
            self.importedFlashcards.create_dictionary()
        else:
            self.importedFlashcards = ImportFlashcards()
            self.recreate_flashcards()
        
        if self.importedFlashcards.file == None:
            #self.importedFlashcards = None
            print(f"({__name__}) file. (MyOwnError): why didn't you choose a file.\n")

if __name__ == '__main__':
    main = Main()

    main.mainloop()