import tkinter as tk

class TopLevelButton(tk.Button):
    def __init__(self, controller, parent, text, file=None):
        self.controller = controller
        self.file = file
        self.fileString = str(file).split(".")[-1][:-2].upper()

        super().__init__(
            master=parent, 
            text=text, 
            command=self.configure_command
        )

    def configure_command(self):
        frame_open = False

        for key in self.controller.frames:
            if self.controller.frames[key]:
                frame_open = True
                break

        if not frame_open:
            self.controller.frames[self.fileString] = self.file(master=self.controller)

        try:
            self.controller.frames[self.fileString].focus_force()
        except: # for if there was an attempt to open another window
            for key in self.controller.frames:
                try:
                    self.controller.frames[key].return_to_main()
                except: # to clear all instances of a window, regardless of existence
                    pass
            self.configure_command()