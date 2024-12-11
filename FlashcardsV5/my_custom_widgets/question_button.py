"""
Found and used only within TestYourKnowledge()
"""

import tkinter as tk

from my_settings_lib import settingsObj as stg
from .universal_widgets.custom_button import CustomButton

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from my_pages import TestYourKnowledge

class QuestionButton(CustomButton):
    def __init__(self, controller, parent, listOfButtons, column, row):
        """
        tk.Button widget to display varying options within TestYourKnowledge

        ### Parameters
        - controller: TestYourKnowledge()
            - to access static methods/attributes
        - parent: tk.Frame() | tk.Widget()
            - to place widget into
        - listOfButtons: list[tk.Button]
            - to search and check whether this button has the correctText
        - column, row: int, int
            - the position of this widget, using solely grid
        - columnspan, rowspan: int, int
            - how many rows and columns the widget expands

        ### Returns
        - tk.Frame object
            - styled with data in settings_config.json
        """
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
    
    def _questionButtonCommand(self):
        """
        - collects information of the question button pressed to be displayed into ResultPage
        - begins TestYourKnowledge().recreate_question_button_text()
        - updates progress bar
        """
        self.text = self.cget("text")
        self.correctText = self.listOfButtons[self.controller.chosenButton].cget("text")

        if self.text == self.correctText:
            self.correctOrWrong = "correct"
        else:
            self.correctOrWrong = "wrong"

        self.controller.questions.append(
            {
                "question" : self.controller.master.flashcards.value,
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
            # TODO: create new flashcardsData.json file to store information of user inputs

        self.controller.update_progressLabel()