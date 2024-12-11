import tkinter as tk
import random
from MySettings import SettingsObj as stg

class Flashcards(tk.Frame):
    def __init__(self, dictionary: dict, master=None):
        """
        tk.Frame widget that replicates physical flashcards

        ### Parameters
        - dictionary: dict
            - to create all flashcards from
            - keys are terms
            - values are definitions
        - master: tk.Frame | tk.Widget
            - to place flashcards into

        ### Properties
        - self.dictionary: dict
            - access to raw text of flashcards
        - self.index: int
            - the current position within flashcards
        - self.key, self.value:
            - the current term and definition
        - self.label: tk.Label
            - widget used to display text

        #### Methods
        - self.configure_clickable(clickable: bool) -> None
            - decides whether flashcards can be flipped
        - self.switch_label() -> None
            - to flip flashcards independant of user input
        - self.next() -> None
            - displays the next flashcards in dictionary
        - self.previous() -> None
            - displays the previous flashcard in dictionary
        - self.restart() -> None
            - sets all internal variables to default values

        ### Returns
        - tk.Frame object
        """
        super().__init__(master=master, background=stg.FRAME_COLOUR)

        # flashcard setup
        self.dictionary = dictionary
        self._copy_of_dictionary = dict(self.dictionary)
        self.index = 0
        
        for key, val in self.dictionary.items():
            self.dictionary[key] = val
        self.key, self.value = list(self.dictionary.items())[self.index]

        self._switchVar = True

        # widgets
        self.label = tk.Label(self, text=self.key, wraplength=self.winfo_width(), justify='left', font=stg.FLASHCARDS_FONT, background=stg.KEYWORD_COLOUR)
        self.label.pack(expand=True, fill='both', padx=stg.PADX, pady=stg.PADY)

        self.label.bind("<Button-1>", self.switch_label)
        self.bind("<Configure>", lambda _ : self._update_wraplength())

    def _update_wraplength(self):
        """
        used to adapt wraplength to changing windows sizes
        """
        self.label.configure(wraplength=self.winfo_width()-10)
        self.label.update()

    def _update(self):
        """
        re-configures the state of...
        - self.key, self.value to current index value
        - label text, what is displayed to user
        """
        self.key, self.value = list(self.dictionary.items())[self.index]

        if self._switchVar == True:
            self.label.configure(text=self.key)
            self.label.configure(background=stg.KEYWORD_COLOUR)
        else:
            self.label.configure(text=self.value)
            self.label.configure(background=stg.DEFINITION_COLOUR)
        self.label.update()

    def configure_clickable(self, clickable: bool):
        """
        enables/disables user from switching to the key or value of flashcards
        """
        if clickable == False:
            self.label.unbind("<Button-1>")

    def switch_label(self, *args, **kwargsargs):
        """
        flips to current key or value
        """
        self._switchVar = not self._switchVar
        self._update()

    def next(self):
        """
        increments to the next flashcard within the dictionary
        
        automatically displays the key
        """
        self.index += 1
        if self.index > len(self.dictionary)-1:
            self.index = 0
        self._switchVar = True
        self._update()

    def previous(self):
        """
        decrements to the previous flashcard within the dictionary
        
        automatically displays the key
        """
        self.index -= 1
        if self.index < 0:
            self.index = len(self.dictionary)-1
        self._switchVar = True
        self._update()

    def restart(self, newlyImported=False):
        """
        sets the state of all Flashcard()'s properties to default values

        ### Parameters
        - newlyImported: bool (automatically False)
            - replaces flashcards with saved version of old importation
            - if specified otherwise, will not override potentially new import that may be called before this method
        """
        if not newlyImported:
            self.dictionary = dict(self._copy_of_dictionary)
        self.index = 0
        self._switchVar = True
        self._update()

    def shuffle(self):
        """
        randomly shuffles the position of each key and value pair within dictionary
        """
        temporary_flashcards_list = list(self.dictionary.items())
        random.shuffle(temporary_flashcards_list)
        self.dictionary = dict(temporary_flashcards_list)
        self._update()