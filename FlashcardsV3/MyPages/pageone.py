import tkinter as tk
from MyCustomWidgets import SubPage
import random

class PageOne(SubPage):
    def __init__(self, master = None):
        self.master = master
        super().__init__(master=self.master)
        self.title("Play Flashcards")

        self.grid_columnconfigure((0), weight=3)
        self.grid_columnconfigure((1), weight=1)

        self.grid_rowconfigure((0), weight=100)
        self.grid_rowconfigure((1), weight=25)

        self.create_flashcards_frame(column=0, row=0)

        self.create_traversal_frame(column=0, row=1)

        self.prevButton = tk.Button(
            master=self.traversalFrame, 
            text='Previous', 
            command=lambda : self.traversal_button_pressed('previous')
        ).grid(column=0, row=0, sticky='news')

        self.create_or_update_current_over_total_label(column=1, row=0)

        self.nextButton = tk.Button(
            master=self.traversalFrame, 
            text='Next', 
            command=lambda : self.traversal_button_pressed('next')
        ).grid(column=2, row=0, sticky='news')

        self.create_operations_frame(column=1, row=1)

        self.shuffleButton = tk.Button(
            master=self.operationsFrame,
            text='Shuffle',
            command=self.shuffle
        ).grid(column=0, row=0, sticky='news')

        self.refreshButton = tk.Button(
            master=self.operationsFrame,
            text='Reload',
            command=self.refresh
        ).grid(column=0, row=1, sticky='news')

    def create_flashcards_frame(self, column=0, row=0):
        self.flashcardFrame = tk.Frame(self)
        self.flashcardFrame.grid(column=column, row=row, columnspan=2, sticky='news')
        self.master.recreate_flashcards(self.flashcardFrame)

    def create_traversal_frame(self, column=0, row=0):
        self.traversalFrame = tk.Frame(self)
        self.traversalFrame.grid(column=column, row=row, sticky='news')

        self.traversalFrame.grid_columnconfigure((0,2), weight=5)
        self.traversalFrame.grid_columnconfigure((1), weight=1)
        self.traversalFrame.grid_rowconfigure((0), weight=1)

    def create_operations_frame(self, column=0, row=0):
        self.operationsFrame = tk.Frame(self)
        self.operationsFrame.grid(column=column, row=row, sticky='news')

        self.operationsFrame.grid_columnconfigure((0), weight=1)
        self.operationsFrame.grid_rowconfigure((0,1), weight=1)

    def create_or_update_current_over_total_label(self, update=False, column=0, row=0):
        self.lengthOfFlashcards = len(self.master.importedFlashcards.dictionary)
        self.index = self.master.flashcards.index
        self.currentOverTotalText = (f"{self.index+1 if self.index < self.lengthOfFlashcards else self.index} / {self.lengthOfFlashcards}\n"+
                                     f"{round((self.index+1)/self.lengthOfFlashcards*100)}%")
        
        if not update:
            self.currentOverTotalLabel = tk.Label(self.traversalFrame, text=self.currentOverTotalText)
            self.currentOverTotalLabel.grid(column=column, row=row, padx=5, pady=5, sticky='news')
        else:
            self.currentOverTotalLabel.configure(text=self.currentOverTotalText)

    def traversal_button_pressed(self, direction):
        if direction == 'next':
            self.master.flashcards.next()
        elif direction == 'previous':
            self.master.flashcards.previous()
        self.create_or_update_current_over_total_label(update=True)

    def shuffle(self):
        temporary_flashcards_list = list(self.master.flashcards.dictionary.items())
        random.shuffle(temporary_flashcards_list)
        self.master.flashcards.dictionary = dict(temporary_flashcards_list)
        self.master.flashcards.update()

    def refresh(self):
        self.master.importedFlashcards.create_dictionary(newFile=False)
        self.master.flashcards.dictionary = self.master.importedFlashcards.dictionary
        self.master.flashcards.restart()
        self.create_or_update_current_over_total_label(update=True)

if __name__ == '__main__':
    PageOne().mainloop()