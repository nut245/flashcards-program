import tkinter as tk
from tkinter import ttk

from MyCustomWidgets import QuestionButton, CustomFrame

from math import ceil
import random

from MySettings import SettingsObj as stg

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import Main
    from MyPages import PageTwo

class TestYourKnowledge(tk.Frame):
    def __init__(self, master, main):
        super().__init__(master=master, background=stg.BACKGROUND_COLOUR)
        self.main: Main = main
        self.master: PageTwo = master

        self.correct = 0
        self.wrong = 0

        self.questions = []

        self.grid_rowconfigure((0,2), weight=4)
        self.grid_rowconfigure((1), weight=1)
        self.grid_rowconfigure((2), weight=8)
        self.grid_columnconfigure((0), weight=1)

        self.master.create_flashcards_frame(master=self, row=0, column=0)

    def populate_page(self):
        if self.master.frames["TestConfigurer"].options.entry.get() != '':
            try:
                self.buttonNumber = int(self.master.frames["TestConfigurer"].options.entry.get())
            except ValueError:
                self.buttonNumber = 3
        else:
            self.buttonNumber = 3

        self.chosenButton = random.choice(range(self.buttonNumber))


        self.create_question_buttons(row=2, column=0)

        self.create_progressbar(row=1, column=0)

        self.recreate_question_button_text()

    def create_progressbar(self, row=1, column=0):
        if self.master.frames["TestConfigurer"].questions.entry.get() == '':
            maximum = 10
        else:
            try:
                maximum = int(self.master.frames["TestConfigurer"].questions.entry.get())
            except ValueError:
                maximum = 10
        self.progressbar = ttk.Progressbar(
            master=self, 
            orient='horizontal', 
            mode='determinate', 
            maximum=maximum
        )
        self.progressbar.grid(row=row, column=column, sticky='news', padx=stg.PADX, pady=stg.PADY)

        tempList = list(self.master.flashcards.dictionary.items())
        random.shuffle(tempList)
        self.master.flashcards.dictionary = dict(tempList)

        self.master.flashcards.configure_clickable(clickable=False)

    def create_question_buttons(self, row=1, column=0):
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
        self.chosenButton = random.choice(range(self.buttonNumber))

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