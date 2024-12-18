import tkinter as tk

from my_custom_widgets import SubPage, EmbeddedPages

from .test_configurer import TestConfigurer
from .test_your_knowledge import TestYourKnowledge
from .result_page import ResultsPage

class PageTwo(SubPage):
    """
    The window that handles "Jeopardy"-esque features of program

    allows access to Main().flashcards attribute to TestYourKnowledge() frame on instantiation

    ### Parameters
    - master: Main()
        - to access static methods/attributes
        - to bind/connect widget to, on destruction of Main()
    
    Parameter only to be passed within population of Main().frames dict. Not by developers

    ### Properties
    - self.frames: dict[str, TestConfigurer | TestYourKnowledge | ResultsPage]
        - the dictionary that holds all pages stemming from PageTwo
        - allows shared access to each page's properties

    ### Returns
    - SubPage() object
        - for Toplevel/window handling within TopLevelButton()
    """
    def __init__(self, master = None):
        self.master = master
        super().__init__(master=self.master)
        self.title("Page 2")

        self.grid_rowconfigure((0), weight=1)
        self.grid_columnconfigure((0), weight=1)

        self.embeddedPages = EmbeddedPages(
            controller=self,
            pages=[TestConfigurer, TestYourKnowledge, ResultsPage]
        )

        self.embeddedPages.show_frame("TestConfigurer")