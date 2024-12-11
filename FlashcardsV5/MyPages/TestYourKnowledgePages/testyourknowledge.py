import tkinter as tk
from tkinter import ttk

from MyCustomWidgets import QuestionButton, CustomFrame, CustomLabel

from math import ceil
import random

from MySettings import SettingsObj as stg

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from MyPages import PageTwo

class TestYourKnowledge(tk.Frame):
    """
    tk.Frame that serves as primary application of 'Jeopardy'-esque aspect of program

    ### Parameters
    - master: PageTwo
        - to access static methods/attributes
        - to place widget into

    ### Returns
    - tk.Frame() object
        - not to be accessed by developers
    """
    def __init__(self, master):
        # All attributes and method calls outside of populate_page() become instantiated on PageTwo's creation.
        # Used, for example, to place flashcards into TestYourKnowledge.
        # Important for if flashcards fail to be imported before TestYourKnowledge()'s instantiation.

        super().__init__(master=master, background=stg.BACKGROUND_COLOUR)
        self.master: PageTwo = master

        self.questions = []

        self.grid_rowconfigure((0,2), weight=4)
        self.grid_rowconfigure((1), weight=1)
        self.grid_rowconfigure((2), weight=8)
        self.grid_columnconfigure((0), weight=1)

        self.master.create_flashcards_frame(master=self, row=0, column=0)

    def populate_page(self):
        """
        creates all properties dependant on previous user input (within TestConfigurer)
        """
        if self.master.frames["TestConfigurer"].options.entry.get() != '':
            try:
                self.buttonNumber = int(self.master.frames["TestConfigurer"].options.entry.get())
            except ValueError:
                self.buttonNumber = 3
        else:
            self.buttonNumber = 3

        self.chosenButton = random.choice(range(self.buttonNumber))

        tempList = list(self.master.flashcards.dictionary.items())
        random.shuffle(tempList)
        self.master.flashcards.dictionary = dict(tempList)

        self.master.flashcards.configure_clickable(clickable=False)

        self.create_question_buttons(row=2, column=0)

        self.create_progressbar(row=1, column=0)

        self.recreate_question_button_text()

    def create_progressbar(self, row=0, column=0):
        """
        styled ttk.Progressbar that matches status to number of questions
        """
        self.progressFrame = CustomFrame(
            master=self,
            row=row, column=column,
        )
        
        self.progressFrame.grid_columnconfigure((0), weight=1)
        self.progressFrame.grid_columnconfigure((1), weight=10)

        self.progressFrame.grid_rowconfigure((0), weight=1)

        if self.master.frames["TestConfigurer"].questions.entry.get() == '':
            maximum = 10
        else:
            try:
                maximum = int(self.master.frames["TestConfigurer"].questions.entry.get())
            except ValueError:
                maximum = 10
        self.progressbar = ttk.Progressbar(
            master=self.progressFrame, 
            orient='horizontal', 
            mode='determinate', 
            maximum=maximum
        )
        self.progressbar.grid(row=0, column=1, sticky='news', padx=stg.PADX, pady=stg.PADY)

        self.progressLabel = CustomLabel(
            master=self.progressFrame,
            text=f"{int(self.progressbar['value'])+1} / {self.progressbar.cget('maximum')}",
            column=0, row=0
        )

    def update_progressLabel(self):
        self.progressLabel.configure(text=f"{int(self.progressbar['value'])+1} / {self.progressbar.cget('maximum')}")
    
    def create_question_buttons(self, row=0, column=0):
        """
        instantiates a user dependant number of question buttons

        includes...
        - tk.Frame to store QuestionButtons
        - QuestionButtons, functionality managed within class
        """
        self.questionButtonsFrame = CustomFrame(
            master=self,
            row=row, column=column
        )
        self.questionButtonsFrame.configure(height=30)

        self.questionButtonsFrame.grid_rowconfigure(list(range(ceil(self.buttonNumber / 2))), weight=1)
        self.questionButtonsFrame.grid_columnconfigure((0,1), weight=1)

        self.listofButtons: list[tk.Button] = []
        for index, row in enumerate([val for val in range(ceil(self.buttonNumber / 2)) for _ in (0, 1)]):
            if self.buttonNumber >= index + 1:
                self.listofButtons.append(
                    QuestionButton(
                        parent=self.questionButtonsFrame, 
                        controller=self,
                        listOfButtons=self.listofButtons,
                        row=row,
                        column=0 if index % 2 == 0 else 1
                    )
                )

        if not len(self.listofButtons) % 2 == 0:
            self.listofButtons[-1].grid_configure(row=row, column=0, columnspan=2)

    def recreate_question_button_text(self):
        """
        - determines the next position of the correct button
        - randomises the labels of each other button
        """
        self.chosenButton = random.choice(range(self.buttonNumber))

        # TODO : logic may be optimised, since the refactoring of flashcards logic 
        self.master.flashcards.next()
        self.master.flashcards.switch_label()
        self.currentFlashcardKey = self.master.flashcards.key

        temporary_flashcard_keys = list(self.master.flashcards.dictionary.keys())
        random.shuffle(temporary_flashcard_keys)

        self.answerInButtons = False
        for index, button in enumerate(self.listofButtons):
            button.configure(text=temporary_flashcard_keys[index])
            button.update()
            
            if button.cget("text") == self.currentFlashcardKey:
                self.answerInButtons = True
                self.chosenButton = index

        if self.answerInButtons == False:
            self.listofButtons[self.chosenButton].configure(
                text=self.currentFlashcardKey
            )