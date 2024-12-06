import tkinter as tk
import random

from MySettings import SettingsObj as stg
from .custombutton import CustomButton

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from MyPages import TestYourKnowledge

class QuestionButton(CustomButton):
    def __init__(self, controller, parent, column, row, listOfButtons):
        super().__init__(
            master=parent,
            text='',
            command=self._questionButtonCommand,
            column=column, row=row
        )
        self.configure(width=20)
        self.controller: TestYourKnowledge = controller
        self.listOfButtons: list[tk.Button] = listOfButtons
        self.correctOrWrong = None

    def _update_labels(self):
            self.configure(wraplength=self.winfo_width()-30)
            self.update()
    
    def _questionButtonCommand(self):
        self.text = self.cget("text")
        self.correctText = self.listOfButtons[self.controller.chosenButton].cget("text")

        if self.text == self.correctText:
            self.controller.correct += 1
            self.correctOrWrong = "correct"
        else:
            self.controller.wrong += 1
            self.correctOrWrong = "wrong"

        self.controller.questions.append(
            {
                "question" : self.controller.main.flashcards.value,
                "correctOrWrong" : self.correctOrWrong,
                "usrAnswer" : self.text,
                "correctAnswer" : self.correctText
            }
        )

        self.controller.recreate_question_button_text()

        self.controller.progressbar["value"] += 1

        if self.controller.progressbar["value"] == int(self.controller.progressbar.cget("maximum")):
            self.controller.master.show_frame("ResultsPage")
            self.controller.master.next_page("ResultsPage")
