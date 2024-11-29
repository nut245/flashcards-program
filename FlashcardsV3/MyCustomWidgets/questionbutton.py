import tkinter as tk
import random

class QuestionButton(tk.Button):
    def __init__(self, controller, parent, listOfButtons):
        super().__init__(
            master=parent,
            command=self.questionButtonCommand,
            width=20
        )
        self.controller = controller
        self.listOfButtons = listOfButtons
        self.correctOrWrong = None
    
    def questionButtonCommand(self):
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

        self.controller.chosenButton = random.choice(range(self.controller.buttonNumber))

        self.controller.shuffle_question_button_text()

        self.controller.progressbar["value"] += 1

        if self.controller.progressbar["value"] == int(self.controller.progressbar.cget("maximum")):
            self.controller.master.show_frame("ResultsPage")
            self.controller.master.next_page("ResultsPage")
