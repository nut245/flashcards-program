import tkinter as tk
from my_custom_widgets import OptionWidget, CustomButton
from my_settings_lib import settingsObj as stg

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from my_pages import PageTwo

class TestConfigurer(tk.Frame):
    """
    tk.Frame widget to gather user inputs for desired functionality of TestYourKnowledge()

    ### Parameters
    - master: PageTwo
        - to access static methods/attributes
        - to place widget into

    ### Attributes
    - questions: OptionWidget()
        - options.questions.get() provides user input of 'number of questions'
    - options: OptionWidget()
        - options.entry.get() provides user input of 'number of options'

    ### Returns
    - tk.Frame object
        - not to be accessed by developers
    """
    def __init__(self, master):
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
        """
        instantiates and displays "TestYourKnowledge" page
        """
        self.master.geometry("600x400")
        self.master.resizable(True, True)
        self.master.embeddedPages.next_page("TestYourKnowledge")