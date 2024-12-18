import tkinter as tk
import static_json
from my_settings_lib import settingsObj as stg
import static_json

from tkinter import messagebox as mb

from my_custom_widgets import SubPage, CustomFrame, CustomLabel, CustomButton, FlashcardsDetailsWidget, VerticalScrolledFrame

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from my_pages import DecksPage

class DeckConfigurer(SubPage):
    def __init__(self, master, folder: str, deck: str, flashcards: dict[str]):
        self.master: DecksPage = master
        self.folder = folder
        self.deck = deck
        self.flashcards = flashcards
        self.flashcardDetailWidgets: list[FlashcardsDetailsWidget] = []
        super().__init__(master=self.master)
        self.geometry(f'900x600+{(self.winfo_screenwidth() // 2 - self.winfo_width()) // 4}+{(self.winfo_screenheight() // 2 - self.winfo_height()) // 4}')

        self.grid_columnconfigure((0), weight=5)
        self.grid_columnconfigure((1), weight=1)
        self.grid_columnconfigure((2), weight=1)
        self.grid_rowconfigure((0), weight=1)
        self.grid_rowconfigure((1), weight=10)
        self.grid_rowconfigure((2), weight=1)

        self.update()

        self.deckLabel = CustomLabel(
            master=self,
            text=deck,
            largetexttype=2
        )
        self.deckLabel.configure(
            font=(stg.COMMON_FONT[0], stg.COMMON_FONT[1]+10)
        )

        self.controlsFrame = CustomFrame(
            master=self,
            column=1, row=0
        )
        self.controlsFrame.grid_columnconfigure((0), weight=1)
        self.controlsFrame.grid_rowconfigure((0,1), weight=1)

        CustomButton(
            master=self.controlsFrame,
            text="Edit",
            command=self._edit_deck_name,
            column=0, row=0
        )

        CustomButton(
            master=self.controlsFrame,
            text="Delete",
            command=self._delete,
            column=0, row=1
        )

        CustomButton(
            master=self,
            text="Save & Continue",
            command=self._save_and_continue,
            column=2, row=0
        )

        self.verticalScrolledFrame = VerticalScrolledFrame(
            parent=self,
            column=0, row=1,
            columnspan=3
        )
        self.verticalScrolledFrame.grid_configure(padx=0, pady=0)

        index = 1
        for term, definition in self.flashcards.items():
            self.flashcardDetailWidgets.append(
                FlashcardsDetailsWidget(
                    controller=self,
                    parent=self.verticalScrolledFrame.interior,
                    index=index,
                    term=term,
                    definition=definition,
                    grid_enabled=False
            ))
            index += 1

        CustomButton(
            master=self,
            text='Add New Flashcard',
            command=self._add_new_flashcard,
            column=1, row=2,
            columnspan=2
        ).configure(padx=0, pady=0)

        # The following commands keep the popup on top.
        self.transient(self.master)      # set to be on top of the main window
        self.grab_set()                  # hijack all commands from the master (clicks on the main window are ignored)
        self.master.wait_window(self)    # pause anything on the main window until this one closes

    def _add_new_flashcard(self):
        self.flashcardDetailWidgets.append(
            FlashcardsDetailsWidget(
                controller=self,
                parent=self.verticalScrolledFrame.interior,
                index=len(self.flashcardDetailWidgets)+1,
                term=f"untitled flashcard {len(self.flashcardDetailWidgets)+1}",
                definition="",
                grid_enabled=False))

        self.flashcardDetailWidgets[len(self.flashcardDetailWidgets)-1].update()
        self.flashcardDetailWidgets[len(self.flashcardDetailWidgets)-1].definitionLabel._edit()
        self.flashcardDetailWidgets[len(self.flashcardDetailWidgets)-1].termLabel._edit()
        self.verticalScrolledFrame.update()
        self.verticalScrolledFrame.canvas.yview_moveto(1)

    def _delete(self):
        deleteVerification = mb.askokcancel(title="deleting file", message = "are you sure?")
        if deleteVerification:
            folders: dict[str] = static_json.parse_json("decks_data.json")["folders"]
            decks: dict[str] = static_json.parse_json(file="decks_data.json")["folders"][self.folder]

            del decks[self.deck]
            folders[self.folder] = decks

            static_json.write_to_json_file(
                file="decks_data.json",
                data={
                    "folders": folders
                }
            )

            self.flashcards.clear()
            
            for flashcardDetailWidget in self.flashcardDetailWidgets:
                self.flashcards[flashcardDetailWidget.term] = flashcardDetailWidget.definition

            self.master.embeddedPages.frames[self.folder]._update_widgets()

            self.return_to_main()

    def _edit_deck_name(self):
        self.entry = tk.Entry(
            master=self, 
            background=stg.KEYWORD_COLOUR, 
            font=(stg.COMMON_FONT[0], stg.COMMON_FONT[1]+10))
        self.entry.insert(0, self.deckLabel.cget('text'))
        self.entry.selection_range(0, 'end')
        self.entry.grid(column=0, row=0, sticky='news', padx=stg.PADX, pady=stg.PADY)
        self.entry.focus()
        if stg.MODE == 'dark':
            self.deckLabel.configure(fg=stg.DARK_TEXT_COLOUR)

        self.done = CustomButton(
            master=self.controlsFrame,
            text='done',
            command=self._done,
            column=0, row=0, rowspan=2)

    def _done(self):
        if self.entry.get() == "" or self.entry.get() == self.deck:
            self.entry.destroy()
            self.done.destroy()
            return
        
        decks: dict[str] = static_json.parse_json(file="decks_data.json")["folders"][self.folder]
        for deck in decks.keys():
            if self.entry.get() == deck:
                mb.showerror(title="Name Error", message="Deck name already taken")
                self.entry.destroy()
                self.done.destroy()
                return

        self.deckLabel.configure(text=self.entry.get())

        self.entry.destroy()
        self.done.destroy()

    def _save_and_continue(self):
        folders: dict[str] = static_json.parse_json("decks_data.json")["folders"]
        decks: dict[str] = static_json.parse_json(file="decks_data.json")["folders"][self.folder]
        if self.deck != self.deckLabel.cget("text"):
            decks[self.deckLabel.cget("text")] = decks[self.deck]
            del decks[self.deck]
            self.deck = self.deckLabel.cget("text")

        folders[self.folder] = decks

        static_json.write_to_json_file(
            file="decks_data.json",
            data={
                "folders": folders
            }
        )

        folders: dict[str] = static_json.parse_json("decks_data.json")["folders"]
        decks: dict[str] = static_json.parse_json(file="decks_data.json")["folders"][self.folder]

        self.flashcards.clear()
        
        for flashcardDetailWidget in self.flashcardDetailWidgets:
            self.flashcards[flashcardDetailWidget.term] = flashcardDetailWidget.definition

        # to clear all flashcards within the deck
        # as dictionaries do not have an order
        # hence repopulating the deck with the same terms and definitions
        # (the only difference being the order)
        # would have no effect
        static_json.update_json_file(
            file="decks_data.json",
            updated_value={"folders": {f"{self.folder}": {self.deck: None}}})

        static_json.update_json_file(
            append=True,
            file="decks_data.json",
            updated_value={
                "folders": {
                    f"{self.folder}": {
                        self.deck: self.flashcards
                    }
                }
            }
        )

        self.master.embeddedPages.frames[self.folder]._update_widgets()

        self.return_to_main()