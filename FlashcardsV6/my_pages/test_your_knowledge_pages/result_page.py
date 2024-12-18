import tkinter as tk
from my_custom_widgets import VerticalScrolledFrame, ResultWidget, TitleWidget, CustomButton, CustomLabel, CustomFrame

from ..export_page import ExportPage

from my_settings_lib import settingsObj as stg

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from my_pages import PageTwo

class ResultsPage(tk.Frame):
    """
    tk.Frame widget to gather user inputs for desired functionality of TestYourKnowledge()

    ### Parameters
    - **master**: PageTwo
        - to access static methods/attributes
        - to place widget into

    ### Attributes
    - **total**: int
        - total questions requested by user
    - **correct**: int
        - the number of correct answers
    - **wrong**: int
        - the number of wrong answers
    - **percentage**: int
        - from 0 to 100, of correct / total

    ### Returns
    - tk.Frame() object
        - not to be accessed by developers
    """
    def __init__(self, master):
        self.master: PageTwo = master
        super().__init__(
            master=master,
            background=stg.BACKGROUND_COLOUR
        )

        self.grid_columnconfigure((0), weight=5)
        self.grid_columnconfigure((1), weight=1)

        self.grid_rowconfigure((0), weight=1)
        self.grid_rowconfigure((1), weight=2)
        self.grid_rowconfigure((2), weight=10)

        TitleWidget(
            master=self,
            text='Result'
        )

        CustomButton(
            master=self,
            text="Export to...",
            command=lambda : ExportPage(master=self),
            column=1, row=0
        )

        self.resultsFrame = VerticalScrolledFrame(
            parent=self,
            column=0, row=2, columnspan=2
        ).interior

        self.resultWidgets: list[ResultWidget] = []

    def populate_page(self):
        """
        creates all properties dependant on previous user input (within TestYourKnowledge)
        """
        self.calculate_percentage()
        self.create_stats_frame()

        for index, question in enumerate(self.master.embeddedPages.frames["TestYourKnowledge"].questions):
            self.resultWidgets.append(ResultWidget(
                master=self.resultsFrame,
                index=index,
                correctOrWrong=question["correctOrWrong"],
                question=question["question"],
                usrAnswer=question["usrAnswer"],
                correctAnswer=question["correctAnswer"] if question["usrAnswer"] != question["correctAnswer"] else None
            ))
            self.resultWidgets[index].pack(expand=True, fill='both', padx=stg.PADX, pady=stg.PADY)

    def create_stats_frame(self):
        """
        displays the general overview of user performance

        which is a tk.Frame to store...
        - totalLabel
        - correctLabel
        - wrongLabel
        - percentageLabel
        """
        self.statsFrame = CustomFrame(
            master=self,
            column=0, row=1, columnspan=2
        )

        self.statsFrame.grid_columnconfigure((0,1,2,3), weight=1)
        self.statsFrame.grid_rowconfigure((0), weight=1)

        self.totalLabel = CustomLabel(
            master=self.statsFrame,
            text=f"Total: {self.total}",
            column=0, row=0
        )

        self.correctLabel = CustomLabel(
            master=self.statsFrame,
            text=f"Correct: {self.correct}",
            column=1, row=0
        ).configure(foreground=stg.CORRECT_COLOUR)

        self.wrongLabel = CustomLabel(
            master=self.statsFrame,
            text=f"Wrong: {self.wrong}",
            column=2, row=0
        ).configure(foreground=stg.WRONG_COLOUR)

        self.percentageLabel = CustomLabel(
            master=self.statsFrame,
            text=f"Grade: {self.percentage}%",
            column=3, row=0
        )

    def calculate_percentage(self):
        """
        collects information of user's performance
        """
        self.total = 0
        self.correct = 0
        self.wrong = 0
        for question in self.master.embeddedPages.frames["TestYourKnowledge"].questions:
            self.total += 1
            if question['correctOrWrong'] == 'correct':
                self.correct += 1
            elif question['correctOrWrong'] == 'wrong':
                self.wrong += 1

        self.percentage = round((self.correct / self.total) * 100)