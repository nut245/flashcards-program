import tkinter as tk
from tkinter import ttk

from MyCustomWidgets import QuestionButton

from math import ceil
import random

NUMBER_OF_BUTTONS = 4

class TestYourKnowledge(tk.Frame):
    def __init__(self, master, main):
        super().__init__(master=master)
        self.main = main

        self.correct = 0
        self.wrong = 0
        self.buttonNumber = NUMBER_OF_BUTTONS
        self.chosenButton = random.choice(range(self.buttonNumber))

        self.questions = []

        self.grid_rowconfigure((0,2), weight=4)
        self.grid_rowconfigure((1), weight=1)
        self.grid_rowconfigure((2), weight=8)
        self.grid_columnconfigure((0), weight=1)

    def populate_page(self):
        self.create_flashcards_frame(row=0, column=0)

        self.create_question_buttons(row=2, column=0)

        self.create_progressbar(row=1, column=0)

        self.shuffle_question_button_text()

    def create_progressbar(self, row=1, column=0):
        if self.master.frames["TestConfigurer"].questions.entry.get() == '':
            maximum = 10
        else:
            maximum = int(self.master.frames["TestConfigurer"].questions.entry.get())
        self.progressbar = ttk.Progressbar(
            master=self, 
            orient='horizontal', 
            mode='determinate', 
            maximum=maximum
        )
        self.progressbar.grid(row=row, column=column, sticky='news')

    def create_flashcards_frame(self, row=0, column=0):
        self.flashcardFrame = tk.Frame(self)
        self.flashcardFrame.grid(row=row, column=column, sticky='news')

        self.main.recreate_flashcards(self.flashcardFrame)

        tempList = list(self.main.flashcards.dictionary.items())
        random.shuffle(tempList)
        self.main.flashcards.dictionary = dict(tempList)

        self.main.flashcards.configure_clickable(clickable=False)

    def create_question_buttons(self, row=1, column=0):
        self.questionButtonsFrame = tk.Frame(self)
        self.questionButtonsFrame.grid(row=row, column=column, sticky='news')

        self.questionButtonsFrame.grid_rowconfigure(list(range(ceil(self.buttonNumber / 2))), weight=1)
        self.questionButtonsFrame.grid_columnconfigure((0,1), weight=1)

        self.listofButtons = []
        for index, row in enumerate([val for val in range(ceil(self.buttonNumber / 2)) for _ in (0, 1)]):
            if self.buttonNumber >= index + 1:
                self.listofButtons.append(QuestionButton(
                    parent=self.questionButtonsFrame, 
                    controller=self,
                    listOfButtons=self.listofButtons
                ))
                self.listofButtons[index].grid(
                    row=row, 
                    column=0 if index % 2 == 0 else 1,
                    sticky='news'
                )

        if not len(self.listofButtons) % 2 == 0:
            self.listofButtons[-1].grid(row=row, column=0, columnspan=2, sticky='news')

    def shuffle_question_button_text(self):
        self.main.flashcards.next()
        self.main.flashcards.switch_label()
        self.currentFlashcardKey = self.main.flashcards.key

        temporary_flashcards_list = list(self.main.flashcards.dictionary.keys())
        random.shuffle(temporary_flashcards_list)

        self.answerInButtons = False
        for index, button in enumerate(self.listofButtons):
            button.configure(text=temporary_flashcards_list[index])
            button.update()
            
            if button.cget("text") == self.currentFlashcardKey:
                self.answerInButtons = True

        if self.answerInButtons == False:
            self.listofButtons[self.chosenButton].configure(
                text=self.currentFlashcardKey
            )