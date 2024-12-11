import tkinter as tk
from my_custom_widgets import SubPage, CustomFrame, CustomButton, CustomLabel
import random
from my_settings_lib import settingsObj as stg

from copy import deepcopy

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import Main

class PlayFlashcardsPage(SubPage):
    """
    The primary window for flashcards program. Simply the flashcards with UI/UX

    accesses Main().flashcards attribute on instantiation (within SubPage)

    ### Parameters
    - master: Main()
        - to access static methods/attributes
        - to bind/connect widget to, on destruction of Main()
    
    Parameter only to be passed within creation/population of Main().frames dictionary. Not by developers

    ### Returns
    - SubPage() object
        - for Toplevel/window handling within TopLevelButton()
    """
    def __init__(self, master=None):
        self.master: Main = master
        super().__init__(master=self.master)
        self.title("Play Flashcards")

        self.grid_columnconfigure((0), weight=3)
        self.grid_columnconfigure((1), weight=1)

        self.grid_rowconfigure((0), weight=10)
        self.grid_rowconfigure((1), weight=1)

        self.create_flashcards_frame(master=self, column=0, row=0)

        self.create_traversal_frame(column=0, row=1)

        self.next = CustomButton(
            master=self.traversalFrame,
            text=f"Previous [{stg.KEYBINDS['flashcards previous']}]", 
            command=self.flashcards_previous
        )

        self.create_or_update_current_over_total_label(column=1, row=0)

        CustomButton(
            master=self.traversalFrame, 
            text=f"Next [{stg.KEYBINDS['flashcards next']}]", 
            command=self.flashcards_next,
            column=2, row=0
        )

        self.create_operations_frame(column=1, row=1)

        CustomButton(
            master=self.operationsFrame,
            text=f"Shuffle [{stg.KEYBINDS['flashcards shuffle']}]",
            command=self.flashcards.shuffle
        )

        CustomButton(
            master=self.operationsFrame,
            text=f"Reload [{stg.KEYBINDS['flashcards refresh']}]",
            command=self.refresh,
            column=0, row=1
        )

        self.bind(stg.format_keybind_string("flashcards next"), lambda _ : self.flashcards_next())
        self.bind(stg.format_keybind_string("flashcards previous"), lambda _ : self.flashcards_previous())
        self.bind(stg.format_keybind_string("flashcards switch"), lambda _ : self.flashcards.switch_label())
        self.bind(stg.format_keybind_string("flashcards shuffle"), lambda _ : self.flashcards.shuffle())
        self.bind(stg.format_keybind_string("flashcards refresh"), lambda _ : self.refresh())

    def create_traversal_frame(self, column=0, row=0):
        """
        The tk.Frame that houses...
        - Previous Button
        - Current-over-total Label
        - Next Button
        """
        self.traversalFrame = CustomFrame(
            master=self,
            column=column, row=row
        )
        self.traversalFrame.grid_columnconfigure((0,2), weight=5)
        self.traversalFrame.grid_columnconfigure((1), weight=1)
        self.traversalFrame.grid_rowconfigure((0), weight=1)

    def create_operations_frame(self, column=0, row=0):
        """
        The tk.Frame that houses...
        - Shuffle Button
        - Reload Button
        """
        self.operationsFrame = CustomFrame(
            master=self,
            column=column, row=row
        )
        self.operationsFrame.grid_columnconfigure((0), weight=1)
        self.operationsFrame.grid_rowconfigure((0,1), weight=1)

    def create_or_update_current_over_total_label(self, update=False, column=0, row=0):
        """
        For the instantiation of tk.Label that displays progress through flashcards

        Used also to update number displayed, through 'update' parameter
        """
        self.lengthOfFlashcards = len(self.flashcards.dictionary)
        self.index = self.flashcards.index
        self.currentOverTotalText = (f"{self.index+1 if self.index < self.lengthOfFlashcards else self.index} / {self.lengthOfFlashcards}\n"+
                                     f"{round((self.index+1)/self.lengthOfFlashcards*100)}%")
        
        if not update:
            self.currentOverTotalLabel = CustomLabel(
                master=self.traversalFrame, 
                text=self.currentOverTotalText, 
                column=column, row=row
            )
        else:
            self.currentOverTotalLabel.configure(text=self.currentOverTotalText)

    def flashcards_next(self):
        self.flashcards.next()
        self.create_or_update_current_over_total_label(update=True)

    def flashcards_previous(self):
        self.flashcards.previous()
        self.create_or_update_current_over_total_label(update=True)

    def refresh(self):
        """
        recreates the flashcards, with check as to whether new flashcards were imported
        """
        self.importedFlashcards.create_dictionary(newFile=False)
        self.flashcards.dictionary = self.importedFlashcards.dictionary
        self.flashcards.restart(newlyImported=True)
        self.create_or_update_current_over_total_label(update=True)