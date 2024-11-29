import tkinter as tk
from MyCustomWidgets import OptionWidget

class TestConfigurer(tk.Frame):
    def __init__(self, master, main):
        super().__init__(master=master)
        self.master.geometry("350x125")
        self.master.resizable(False, False)
        self.master = master

        self.grid_rowconfigure((0,1), weight=1)
        self.grid_columnconfigure((0), weight=1)

        self.questions = OptionWidget(parent=self, text="Number Of Questions")
        self.questions.grid(row=0, column=0, sticky='news')

        self.timer = OptionWidget(parent=self, text="Set Timer?")
        self.timer.grid(row=1, column=0, sticky='news')

        self.startbutton = tk.Button(master=self, text='Start', command=self.start_quiz)
        self.startbutton.grid(row=2, column=0, sticky='news')

    def start_quiz(self):
        self.master.geometry("600x400")
        self.master.resizable(True, True)
        self.master.show_frame("TestYourKnowledge")
        self.master.next_page("TestYourKnowledge")