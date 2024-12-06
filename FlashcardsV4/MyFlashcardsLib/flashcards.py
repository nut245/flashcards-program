import tkinter as tk
from MySettings import SettingsObj as stg

class Flashcards(tk.Frame):
    def __init__(self, dictionary: dict, master=None):
        super().__init__(master=master, background=stg.FRAME_COLOUR)

        # flashcard setup
        self.dictionary = {}
        self.index = 0
        
        for key, val in dictionary.items():
            self.dictionary[key] = val
        self.key, self.value = list(self.dictionary.items())[self.index]

        self.switchVar = True

        # widgets
        self.label = tk.Label(self, text=self.key, wraplength=self.winfo_width(), justify='left', font=stg.FLASHCARDS_FONT, background=stg.KEYWORD_COLOUR)
        self.label.pack(expand=True, fill='both', padx=stg.PADX, pady=stg.PADY)

        self.label.bind("<Button-1>", self.switch_label)
        self.bind("<Configure>", lambda _ : self._update_wraplength())

    def _update_wraplength(self):
        self.label.configure(wraplength=self.winfo_width()-10)
        self.label.update()

    def configure_clickable(self, clickable: bool):
        if clickable == False:
            self.label.unbind("<Button-1>")

    def update(self):
        self.key, self.value = list(self.dictionary.items())[self.index]

        if self.switchVar == True:
            self.label.configure(text=self.key)
            self.label.configure(background=stg.KEYWORD_COLOUR)
            self.label.update()
        else:
            self.label.configure(text=self.value)
            self.label.configure(background=stg.DEFINITION_COLOUR)
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