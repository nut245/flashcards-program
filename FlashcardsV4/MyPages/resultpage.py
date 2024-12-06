import tkinter as tk
from MyCustomWidgets import VerticalScrolledFrame, ResultWidget, TitleWidget, CustomButton, CustomLabel

from .exportpage import ExportPage

from MySettings import SettingsObj as stg

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import Main
    from MyPages import PageTwo

class ResultsPage(tk.Frame):
    def __init__(self, master, main):
        self.master: PageTwo = master
        super().__init__(
            master=master,
            background=stg.BACKGROUND_COLOUR
        )
        self.main: Main = main

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

        self.resultsFrame = VerticalScrolledFrame(parent=self)
        self.resultsFrame.grid(column=0, row=2, columnspan=2, sticky='news', padx=stg.PADX, pady=stg.PADY)
        self.resultsFrame.interior.configure(background=stg.BACKGROUND_COLOUR)
        self.resultsFrame.canvas.configure(background=stg.BACKGROUND_COLOUR)

        self.resultWidgets: list[ResultWidget] = []

    def populate_page(self):
        self.calculate_percentage()
        self.create_stats_frame()

        for index, question in enumerate(self.master.frames["TestYourKnowledge"].questions):
            self.resultWidgets.append(ResultWidget(
                master=self.resultsFrame.interior,
                index=index,
                correctOrWrong=question["correctOrWrong"],
                question=question["question"],
                usrAnswer=question["usrAnswer"],
                correctAnswer=question["correctAnswer"] if question["usrAnswer"] != question["correctAnswer"] else None
            ))
            self.resultWidgets[index].pack(expand=True, fill='both', padx=stg.PADX, pady=stg.PADY)

    def create_stats_frame(self):
        self.statsFrame = tk.Frame(
            master=self,
            background=stg.FRAME_COLOUR
        )
        self.statsFrame.grid(column=0, row=1, columnspan=2, sticky='news', padx=stg.PADX)

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
        self.total = 0
        self.correct = 0
        self.wrong = 0
        for question in self.master.frames["TestYourKnowledge"].questions:
            self.total += 1
            if question['correctOrWrong'] == 'correct':
                self.correct += 1
            elif question['correctOrWrong'] == 'wrong':
                self.wrong += 1

        self.percentage = round((self.correct / self.total) * 100)