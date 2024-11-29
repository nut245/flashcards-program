import tkinter as tk

class Flashcards(tk.Frame):
    def __init__(self, dictionary: dict, master=None):
        super().__init__(master=master)

        # flashcard setup
        self.dictionary = {}
        self.index = 0
        
        for key, val in dictionary.items():
            self.dictionary[key] = val
        self.key, self.value = list(self.dictionary.items())[self.index]

        self.switchVar = True

        # widgets
        self.label = tk.Label(self, text=self.key, wraplength=600, justify='left')
        self.label.pack(expand=True, fill='both')

        self.label.bind("<Button-1>", self.switch_label)

    def configure_clickable(self, clickable: bool):
        if clickable == False:
            self.label.unbind("<Button-1>")

    def update(self):
        self.key, self.value = list(self.dictionary.items())[self.index]

        if self.switchVar == True:
            self.label.configure(text=self.key)
            self.label.update()
        else:
            self.label.configure(text=self.value)
            self.label.update()

    def switch_label(self, *args, **kwargs):
        self.switchVar = not self.switchVar
        self.update()

    def next(self):
        self.index += 1
        if self.index > len(self.dictionary)-1:
            self.index = 0
        self.switchVar = True
        self.update()

    def previous(self):
        self.index -= 1
        if self.index < 0:
            self.index = len(self.dictionary)-1
        self.switchVar = True
        self.update()

    def restart(self):
        self.index = 0
        self.switchVar = True
        self.update()