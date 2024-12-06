import tkinter as tk
from MyCustomWidgets import OptionWidget, CustomButton
from MySettings import SettingsObj as stg

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from MyPages import PageTwo

class TestConfigurer(tk.Frame):
    def __init__(self, master, main):
        super().__init__(master=master, background=stg.BACKGROUND_COLOUR)
        self.master.geometry("600x200")
        self.master.resizable(False, False)
        self.master: PageTwo = master

        self.grid_rowconfigure((0,1), weight=1)
        self.grid_columnconfigure((0), weight=1)

        self.questions = OptionWidget(
            parent=self, 
            text="Number Of Questions" , 
            column=0, row=0
        )

        self.options = OptionWidget(
            parent=self, 
            text="Number Of Options",
            column=0, row=1
        )
        
        CustomButton(
            master=self, 
            text='Start', 
            command=self.start_quiz, 
            row=2, column=0
        )

    def start_quiz(self):
        self.master.geometry("600x400")
        self.master.resizable(True, True)
        self.master.show_frame("TestYourKnowledge")
        self.master.next_page("TestYourKnowledge")