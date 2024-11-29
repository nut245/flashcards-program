import tkinter as tk

class Result(tk.Frame):
    def __init__(self, master, index, correctOrWrong, question, usrAnswer, correctAnswer = None):
        super().__init__(
            master=master,
            highlightbackground="black",
            highlightthickness=1
        )
        self.index = index
        self.correctOrWrong = correctOrWrong
        self.question = question
        self.usrAnswer = usrAnswer
        self.correctAnswer = correctAnswer

        self.wraplength = 400
        self.width = 10

        self.grid_columnconfigure((0), weight=1)
        self.grid_columnconfigure((1,2), weight=4)

        self.grid_rowconfigure((0,1), weight=1)

        self.questionNumberLabel = tk.Label(
            master=self, 
            text=f"Question {self.index+1}\n{self.correctOrWrong}",
            wraplength=self.wraplength, justify='left', width=self.width, anchor='w'
        )
        self.questionNumberLabel.grid(row=0, column=0, rowspan=2, sticky='news')

        self.usrAnswerLabel = tk.Label(
            master=self,
            text = f"Your Answer: {self.usrAnswer}",
            wraplength=self.wraplength, justify='left', width=self.width, anchor='w'
        )

        self.questionLabel = tk.Label(
            master=self,
            text=self.question,
            wraplength=self.wraplength, justify='left', width=self.width, anchor='w'
        )
        self.questionLabel.grid(column=1, row=0, columnspan=2, sticky="news")

        if not correctAnswer == None:
            self.usrAnswerLabel.grid(row=1, column=1, sticky='news')

            self.correctAnswerLabel = tk.Label(
                master=self,
                text=f"Actual Answer: {self.correctAnswer}",
                wraplength=self.wraplength, justify='left', width=self.width, anchor='w'
            )
            self.correctAnswerLabel.grid(row=1, column=2, sticky='news')
        else:
            self.usrAnswerLabel.grid(row=1, column=1, columnspan=2, sticky='news')
