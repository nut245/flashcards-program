import tkinter as tk

class SubPage(tk.Toplevel):
    """"
    some more documentation
    """
    def __init__(self, master = None):
        self.master = master
        super().__init__(master=self.master)
        self.title('Toplevel Application')
        self.geometry('600x400')

        self.bind('<Escape>', lambda x : self.return_to_main())

    def return_to_main(self):
        self.master.focus_force()
        try:
            self.master.frames[str(self)[2:].upper().rstrip("0123456789")] = None
            self.destroy()
        except AttributeError:
            print("MyOwnError: master attribute was not passed, likely due to subpage being run independantly")