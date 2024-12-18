import tkinter as tk

import static_json

from my_custom_widgets import VerticalScrolledFrame, CustomFrame, CustomButton

from my_custom_widgets.page_specfic_widgets.deck_widgets.deck_widget import DeckWidget

from my_flashcards_lib import ImportFlashcards

from my_settings_lib import settingsObj as stg

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from my_pages import DecksPage

class FolderContents(CustomFrame):
    def __init__(self, master):
        super().__init__(master=master)

        self.folder = None
        self.controller: DecksPage = None
        self.decks: dict[str] = {}
        self.deckWidgets: list[DeckWidget] = []
        self.decksIndex = 1

        self.configure(background=stg.BACKGROUND_COLOUR)
        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure((0), weight=1)
        self.grid_rowconfigure((1), weight=10)

        CustomButton(
            master=self,
            text="Import New Deck",
            command=self._import_new_deck,
            column=0, row=0
        )

        CustomButton(
            master=self,
            text="Create New Deck",
            command=self._create_new_deck,
            column=1, row=0
        )

        self.verticalScrolledFrame = VerticalScrolledFrame(parent=self)
        self.verticalScrolledFrame.grid_configure(row=1, columnspan=2, padx=0, pady=0)

    def initialise(self, controller, folder=None, decks: dict[str] = {}):
        self.controller: DecksPage = controller
        self.folder = folder
        self.decks = decks

        if not self.decks:
            return
        
        self._populate_decks()

    def _create_new_deck(self):
        self.decks[f"untitled deck {self.decksIndex}"] = {}
        static_json.update_json_file(
            file='decks_data.json',
            updated_value={
                "folders": {
                    f"{self.folder}": self.decks
                }
            }
        )
        self._update_widgets()

    def _import_new_deck(self):
        new_deck = ImportFlashcards()
        if len(new_deck.dictionary) < 1:
            print(f"({__name__}) file. (MyOwnError): why didn't you choose a file.\n")
            self.focus_force()
            return
        
        formattedDeckName = new_deck.file.split("//")[-1].split(".")[0]
        self.decks[f"{formattedDeckName}"] = new_deck.dictionary
        static_json.update_json_file(
            append=True,
            file='decks_data.json',
            updated_value={
                "folders": {
                    f"{self.folder}": self.decks
                }
            }
        )
        
        self._update_widgets()
        
        self.focus_force()

    def _update_widgets(self):
        for widget in self.verticalScrolledFrame.interior.winfo_children():
            widget.destroy()
        self.deckWidgets.clear()
        self._populate_decks()

    def _populate_decks(self):
        index = 0
        self.decks: dict[str] = static_json.parse_json(file="decks_data.json")["folders"][self.folder]
        for deck, flashcards in self.decks.items():
            if index % 2 == 0:
                self.tempFrame = tk.Frame(master=self.verticalScrolledFrame.interior)
                self.tempFrame = CustomFrame(
                    master=self.verticalScrolledFrame.interior,
                    grid_enabled=False)
                self.tempFrame.configure(bg=stg.BACKGROUND_COLOUR)

                self.decksIndex += 1

            self.deckWidgets.append(
                DeckWidget(
                    controller=self.controller,
                    parent=self.tempFrame,
                    folder=self.folder,
                    deck=deck,
                    flashcards=flashcards
                ).container.pack(
                    expand=True, 
                    fill='both', 
                    side='left', 
                    padx=stg.PADX
                )
            )
            
            index += 1

        # filler widget to be instantiated and take space when number of decks is not even
        if len(self.decks) % 2 == 1:
            tk.Label(
                master=self.verticalScrolledFrame.interior, 
                text='        ', 
                width=7, 
                state='disabled', 
                background=self.verticalScrolledFrame.interior.cget('bg')
            ).pack(
                expand=True, 
                fill='both', 
                side='left', 
                in_=self.tempFrame,
                padx=stg.PADX
            )
