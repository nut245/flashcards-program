import tkinter as tk
from MyFlashcardsLib import *
from MyCustomWidgets import TopLevelButton
from MyPages import *

class Main(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Main Application')
        self.geometry('600x400')

        self.importedFlashcards = ImportFlashcards()

        self.flashcards = Flashcards(dictionary=self.importedFlashcards.dictionary)
        
        self.grid_columnconfigure((0), weight=1)
        self.grid_columnconfigure((1), weight=10)

        self.grid_rowconfigure((0), weight=1)
        self.grid_rowconfigure((1), weight=2)

        self.titleFrame = tk.Frame(self)
        self.titleFrame.grid(column=0, columnspan=2, row=0, sticky='news')

        self.titleLabel = tk.Label(
            master=self.titleFrame,
            text="Quiz-imi"
        )
        self.titleLabel.pack(expand=True, fill='both')

        self.menuFrame = tk.Frame(self)
        self.menuFrame.grid(column=1, row=1, sticky='news')

        self.menuFrame.grid_columnconfigure((0,1), weight=1)
        self.menuFrame.grid_rowconfigure((0,1,2), weight=1)

        self.pageButtons = {}

        self.pageButtons["Page 1"] = TopLevelButton(
            controller=self, 
            parent=self.menuFrame,
            text="Play Flashcards", 
            file=PageOne, 
        )
        self.pageButtons["Page 1"].grid(
            column=0, columnspan=2, row=0, pady=10, padx=5, sticky='news'
        )

        self.pageButtons["Test Your Knowledge"] = TopLevelButton(
            controller=self, 
            parent=self.menuFrame,
            text="Test Your Knowledge", 
            file=PageTwo, 
        )
        self.pageButtons["Test Your Knowledge"].grid(
            column=0, columnspan=2, row=1, pady=10, padx=5, sticky='news'
        )

        self.create_frames_dictionary()

        self.importButton = tk.Button(
            master=self.menuFrame,
            text='Import New Flashcards',
            command=self.importedFlashcards.create_dictionary
        ).grid(column=0, row=2, pady=10, padx=5, sticky='news')

        self.exportButton = tk.Button(
            master=self.menuFrame,
            text="Export Flashcards To...",
            # TODO : make exportable flashcards, into whatever format
            command=lambda : print("TODO : make exportable flashcards, into whatever format") 
        ).grid(column=1, row=2, pady=10, padx=5, sticky='news')

        self.settingsFrame = tk.Frame(self)
        self.settingsFrame.grid(column=0, row=1, sticky='news')

        self.settingsFrame.grid_columnconfigure((0), weight=1)
        self.settingsFrame.grid_rowconfigure((0,1), weight=1)

        self.settingsButton = tk.Button(
            master=self.settingsFrame,
            text="Settings",
            # TODO : make settings button work
            command=lambda : print("TODO : make settings button work") 
        ).grid(column=0, row=0, pady=10, padx=5, sticky='news')

        self.viewDecksButton = tk.Button(
            master=self.settingsFrame,
            text="View Decks",
            # TODO : make view decks button work
            command=lambda : print("TODO : make view decks button work") 
        ).grid(column=0, row=1, pady=10, padx=5, sticky='news')

        self.focus_force()

    def create_frames_dictionary(self):
        self.frames = {}
        listOfFiles = []
        for button in self.pageButtons:
            listOfFiles.append(self.pageButtons[button].file)

        for file in listOfFiles:
            self.frames[str(file).split(".")[-1][:-2].upper()] = None

    def recreate_flashcards(self, flashcardsParent):
        try:
            self.flashcards.destroy()
        except: pass
        self.flashcards = Flashcards(master=flashcardsParent, dictionary=self.importedFlashcards.dictionary)
        self.flashcards.pack(expand=True, fill='both')

if __name__ == '__main__':
    Main().mainloop()