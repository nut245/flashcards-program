import tkinter as tk
from MyCustomWidgets import VerticalScrolledFrame, Result

class ResultsPage(tk.Frame):
    def __init__(self, master, main):
        super().__init__(
            master=master
        )
        self.main = main

        self.grid_columnconfigure((0), weight=1)

        self.grid_rowconfigure((0), weight=1)
        self.grid_rowconfigure((1), weight=1)

        self.titleLabel = tk.Label(
            master=self,
            text="Results"
        )
        self.titleLabel.grid(column=0, row=0, sticky='news')

        self.resultsFrame = VerticalScrolledFrame(parent=self)
        self.resultsFrame.grid(column=0, row=1, sticky='news')

    def populate_page(self):
        for index, question in enumerate(self.master.frames["TestYourKnowledge"].questions):
            Result(
                master=self.resultsFrame.interior,
                index=index,
                correctOrWrong=question["correctOrWrong"],
                question=question["question"],
                usrAnswer=question["usrAnswer"],
                correctAnswer=question["correctAnswer"] if question["usrAnswer"] != question["correctAnswer"] else None
            ).pack(expand=True, fill='both', padx=5, pady=5)