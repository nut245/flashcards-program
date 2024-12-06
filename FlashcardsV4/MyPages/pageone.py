import tkinter as tk
from MyCustomWidgets import SubPage, CustomFrame, CustomButton, CustomLabel
import random
from MySettings import SettingsObj as stg

from copy import deepcopy

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import Main

class PageOne(SubPage):
    def __init__(self, master=None):
        self.master: Main = master
        super().__init__(master=self.master)
        self.title("Play Flashcards")

        self.grid_columnconfigure((0), weight=3)
        self.grid_columnconfigure((1), weight=1)

        self.grid_rowconfigure((0), weight=10)
        self.grid_rowconfigure((1), weight=1)

        self.create_flashcards_frame(master=self, column=0, row=0)

        self.create_traversal_frame(column=0, row=1)

        self.next = CustomButton(
            master=self.traversalFrame,
            text='Previous', 
            command=lambda : self.traversal_button_pressed('previous')
        )

        self.create_or_update_current_over_total_label(column=1, row=0)

        CustomButton(
            master=self.traversalFrame, 
            text='Next', 
            command=lambda : self.traversal_button_pressed('next'),
            column=2, row=0
        )

        self.create_operations_frame(column=1, row=1)

        CustomButton(
            master=self.operationsFrame,
            text='Shuffle',
            command=self.shuffle
        )

        CustomButton(
            master=self.operationsFrame,
            text='Reload',
            command=self.refresh,
            column=0, row=1
        )

        self.bind("<Right>", lambda _ : self.traversal_button_pressed(direction='next'))
        self.bind("<Left>", lambda _ : self.traversal_button_pressed(direction='previous'))
        self.bind('<a>', lambda _ : self.flashcards.switch_label())
        self.bind('<s>', lambda _ : self.shuffle())
        self.bind('<r>', lambda _ : self.refresh())

    def create_flashcards_button(self, master, text, command, column=0, row=0):
        button = tk.Button(
            master=master,
            text=text,
            command=command,
            background=stg.BUTTON_COLOUR,
            font=stg.COMMON_FONT
        )
        button.grid(
            column=column, 
            row=row,
            sticky='news', 
            padx=stg.PADX, 
            pady=stg.PADY
        )

    def create_traversal_frame(self, column=0, row=0):
        self.traversalFrame = CustomFrame(
            master=self,
            column=column, row=row
        )
        self.traversalFrame.grid_columnconfigure((0,2), weight=5)
        self.traversalFrame.grid_columnconfigure((1), weight=1)
        self.traversalFrame.grid_rowconfigure((0), weight=1)

    def create_operations_frame(self, column=0, row=0):
        self.operationsFrame = CustomFrame(
            master=self,
            column=column, row=row
        )
        self.operationsFrame.grid_columnconfigure((0), weight=1)
        self.operationsFrame.grid_rowconfigure((0,1), weight=1)

    def create_or_update_current_over_total_label(self, update=False, column=0, row=0):
        self.lengthOfFlashcards = len(self.flashcards.dictionary)
        self.index = self.flashcards.index
        self.currentOverTotalText = (f"{self.index+1 if self.index < self.lengthOfFlashcards else self.index} / {self.lengthOfFlashcards}\n"+
                                     f"{round((self.index+1)/self.lengthOfFlashcards*100)}%")
        
        if not update:
            self.currentOverTotalLabel = CustomLabel(
                master=self.traversalFrame, 
                text=self.currentOverTotalText, 
                column=column, row=row
            )
        else:
            self.currentOverTotalLabel.configure(text=self.currentOverTotalText)



    def traversal_button_pressed(self, direction):
        if direction == 'next':
            self.flashcards.next()
        elif direction == 'previous':
            self.flashcards.previous()
        self.create_or_update_current_over_total_label(update=True)

    def shuffle(self):
        temporary_flashcards_list = list(self.flashcards.dictionary.items())
        random.shuffle(temporary_flashcards_list)
        self.flashcards.dictionary = dict(temporary_flashcards_list)
        self.flashcards.update()

    def refresh(self):
        self.importedFlashcards.create_dictionary(newFile=False)
        self.flashcards.dictionary = self.importedFlashcards.dictionary
        self.flashcards.restart()
        self.create_or_update_current_over_total_label(update=True)