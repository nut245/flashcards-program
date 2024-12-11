"""
Found and used only within ResultsPage()
"""

import tkinter as tk

from my_settings_lib import settingsObj as stg
from .universal_widgets.custom_label import CustomLabel

class ResultWidget(tk.Frame):
    def __init__(self, master, index: int, correctOrWrong: str, question: str, usrAnswer: str, correctAnswer: str | None = None):
        """
            Dynamically styled tk.Frame widget to display information per question asked of user within TestYourKnowledge

            ### Parameters
            - master: Main()
                - to access static methods/attributes
                - to place widget into
            - index: int
                - used to number questions
            - correctOrWrong:
                - either 'correct' or 'wrong'
                - used to display display usrAnswer only or correctAnswer as well
            - usrAnswer:
                - the text on button, pressed by user
            - correctAnswer:
                - the actual answer of each question

            ### Properties
            - all parameters usable by each result widget
            - planned to be outputted to a new json file

            ### Returns
            - tk.Frame object
                - styled with data in settings_config.json
            """
        super().__init__(
            master=master,
            background=stg.FRAME_COLOUR
        )
        self.index = index
        self.correctOrWrong = correctOrWrong
        self.question = question
        self.usrAnswer = usrAnswer
        self.correctAnswer = correctAnswer

        self.labels: dict[str, CustomLabel] = {}

        self.grid_columnconfigure((0), weight=1)
        self.grid_columnconfigure((1,2), weight=4)

        self.grid_rowconfigure((0,1), weight=1)

        self.labels["Question Number"] = CustomLabel(
            master=self, 
            text=f"Question {self.index+1}\n{self.correctOrWrong}",
            row=0, column=0, rowspan=2,
            largetexttype=1,
            bold=True
        )

        if self.correctOrWrong == 'correct':
            self.labels["Question Number"].configure(foreground=stg.CORRECT_COLOUR)
        elif self.correctOrWrong == 'wrong':
            self.labels["Question Number"].configure(foreground=stg.WRONG_COLOUR)
        else:
            pass # for debugging

        self.labels["User Answer"] = CustomLabel(
            master=self,
            text = f"Your Answer: {self.usrAnswer}",
            row=1, column=1, columnspan=2,
            largetexttype=1
        )

        self.labels["Question"] = CustomLabel(
            master=self,
            text=self.question,
            column=1, row=0, columnspan=2,
            largetexttype=1
        )

        if not correctAnswer == None:
            self.labels["User Answer"].grid_configure(row=1, column=1, columnspan=1)

            self.labels["Correct Answer"] = CustomLabel(
                master=self,
                text=f"Actual Answer: {self.correctAnswer}",
                row=1, column=2,
                largetexttype=1
            )

        self.bind("<Configure>", lambda _ : self._update_labels())
    
    def _update_labels(self):
        """
        reconfigures the wraplength property of each label within a result widget
        to fit screen size
        """
        for label in self.labels.values():
            label.configure(wraplength=label.winfo_width()-10)
            label.update()