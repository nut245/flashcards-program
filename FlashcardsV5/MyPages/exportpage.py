import tkinter as tk
from MyCustomWidgets import SubPage

class ExportPage(SubPage):
    def __init__(self, master=None):
        """
        currently no functionality
        """
        super().__init__(master=master)
        self.geometry(f"600x200+{(self.winfo_screenwidth() // 2 - self.winfo_width()) // 8}+{(self.winfo_screenheight() // 2 - self.winfo_height()) // 8}")
        self.resizable(False, False)

        tk.Label(
            master=self,
            text='must allow user to...\n- choose type of file to export to\n- where to save to',
            justify='left',
            anchor='center'
        ).pack()