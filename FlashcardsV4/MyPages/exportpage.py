import tkinter as tk
from MyCustomWidgets import SubPage

class ExportPage(SubPage):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.geometry("600x200")
        self.resizable(False, False)

        tk.Label(
            master=self,
            text='must allow user to...\n- choose type of file to export to\n- where to save to',
            justify='left',
            anchor='center'
        ).pack()