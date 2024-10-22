import customtkinter as ctk
import SettingsFile

class Flashcards(ctk.CTkFrame):
    def __init__(self, dictionary: dict, parent=None):

        # flashcard setup
        self.dictionary = {}
        for key, val in dictionary.items():
            self.dictionary[key] = val
        self.index = 0
        self.key, self.value = list(self.dictionary.items())[self.index]
        super().__init__(master=parent, fg_color="#504c54")

        self.switchVar = True

        # widgets
        font = ctk.CTkFont(family='calibri', size=SettingsFile.FLASHCARD_FONT_SIZE)
        self.label = ctk.CTkLabel(self, text=self.key, wraplength=900, justify='left', font=font)
        self.label.pack(expand=True, fill='both')

        self.label.bind("<Button-1>", self.switch_label)

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