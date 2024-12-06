import tkinter as tk

from MyCustomWidgets import SubPage

from .testconfigurer import TestConfigurer
from .testyourknowledge import TestYourKnowledge
from .resultpage import ResultsPage

class PageTwo(SubPage):
    def __init__(self, master = None):
        self.master = master
        super().__init__(master=self.master)
        self.title("Page 2")

        self.grid_rowconfigure((0), weight=1)
        self.grid_columnconfigure((0), weight=1)

        self.frames: dict[str, TestConfigurer | TestYourKnowledge | ResultsPage] = {}
        for F in (TestConfigurer, TestYourKnowledge, ResultsPage):
            page_name = F.__name__
            frame = F(master=self, main=self.master)
            self.frames[page_name] = frame

        self.show_frame("TestConfigurer")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        for frame in self.frames.values():
            frame.grid_forget()

        frame = self.frames[page_name]
        frame.grid(row=0, column=0, sticky="nsew")
        frame.focus_force()

    def next_page(self, page_name):
        self.frames[page_name].populate_page()