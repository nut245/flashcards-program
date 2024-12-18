import tkinter as tk

from my_settings_lib import settingsObj as stg

from ...universal_widgets.custom_frame import CustomFrame
from ...universal_widgets.custom_label import CustomLabel
from ...universal_widgets.custom_button import CustomButton

from my_pages.decks_pages.deck_configurer import DeckConfigurer

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from my_pages.decks_pages.decks_page import DecksPage

class DeckWidget():
    def __init__(self, controller, parent, folder, deck, flashcards):
        self.controller: DecksPage = controller
        self.folder = folder
        self.deck = deck
        self.flashcards = flashcards

        self.container = CustomFrame(
            master=parent,
            grid_enabled=False
        )

        self.container.grid_columnconfigure((0,1), weight=1)
        self.container.grid_rowconfigure((0), weight=1)
        self.container.grid_rowconfigure((1), weight=1)

        CustomLabel(
            master=self.container,
            text=deck,
            column=0, row=0,
            columnspan=2,
            largetexttype=2
        ).configure(
            width=1,
            height=7
        )
        
        CustomButton(
            master=self.container,
            text="Play",
            command=self._open_new_deck,
            column=0, row=1
        ).configure(
            width=1
        )

        CustomButton(
            master=self.container,
            text="Edit",
            command=self._edit_deck,
            column=1, row=1
        ).configure(
            width=1
        )

    def _open_new_deck(self):
        self.controller.master.recreate_main(newDeck=self.flashcards)

    def _edit_deck(self):
        DeckConfigurer(
            folder = self.folder,
            master=self.controller,
            deck=self.deck,
            flashcards=self.flashcards
        )