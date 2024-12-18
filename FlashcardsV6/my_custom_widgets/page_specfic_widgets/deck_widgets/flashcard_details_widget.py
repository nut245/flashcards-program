import tkinter as tk
from tkinter import messagebox as mb
from my_settings_lib import settingsObj as stg

from ...universal_widgets.custom_frame import CustomFrame
from ...universal_widgets.custom_label import CustomLabel
from ...universal_widgets.custom_button import CustomButton

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from my_pages.decks_pages.deck_configurer import DeckConfigurer

class FlashcardsDetailsWidget(CustomFrame):
    def __init__(self, controller, parent, index, term, definition, column=0, row=0, columnspan=1, rowspan=1, grid_enabled=True):
        super().__init__(parent, column, row, columnspan, rowspan, grid_enabled)
        self.controller: DeckConfigurer = controller
        self.term = term
        self.definition = definition

        self.grid_columnconfigure((0), weight=2)
        self.grid_columnconfigure((1), weight=10)
        self.grid_columnconfigure((2), weight=1)
        self.grid_rowconfigure((0), weight=1)
        self.grid_rowconfigure((1), weight=5)

        self.flashcardIndexLabel = CustomLabel(
            master=self,
            text=f"flashcard {index}",
            columnspan=2
        )

        self.termLabel = FlashcardComponent(
            master=self,
            text='Term',
            info=self.term,
            column=0, row=1
        )
        self.termLabel.grid_configure(
            sticky='new', padx=0
        )

        self.definitionLabel = FlashcardComponent(
            master=self,
            text='Definition',
            info=self.definition,
            column=1, row=1
        )
        self.definitionLabel.grid_configure(
            sticky='new', padx=0
        )

        self.functionFrame = CustomFrame(
            master=self,
            column=2, row=0, rowspan=2
        )
        self.functionFrame.grid_configure(padx=0, pady=0)
        self.functionFrame.grid_columnconfigure((0,1), weight=1)
        self.functionFrame.grid_rowconfigure((0,1,2), weight=1)

        CustomButton(
            master=self.functionFrame,
            text='↑',
            command=self._move_up,
            column=0, row=0
        ).configure(height=1)

        CustomButton(
            master=self.functionFrame,
            text='↓',
            command=self._move_down,
            column=1, row=0
        ).configure(height=1)

        CustomButton(
            master=self.functionFrame,
            text='Add Image',
            command=lambda:print("stop ittt"),
            column=0, row=1,
            columnspan=2)

        CustomButton(
            master=self.functionFrame,
            text='delete',
            command=self._delete,
            column=0, row=2,
            columnspan=2)

    def _delete(self):
        deleteVerification = mb.askokcancel(title="deleting file", message = "are you sure?")
        if deleteVerification:
            try:
                self.controller.flashcardDetailWidgets.remove(self)
                self._update_display_and_data()
                self.destroy()
            except ValueError:
                pass # the user pressed the delete button twice

    def _move_up(self):
        index = self.controller.flashcardDetailWidgets.index(self)
        self.controller.flashcardDetailWidgets[index], self.controller.flashcardDetailWidgets[index-1] = self.controller.flashcardDetailWidgets[index-1], self.controller.flashcardDetailWidgets[index]

        self._update_display_and_data()

    def _move_down(self):
        index = self.controller.flashcardDetailWidgets.index(self)
        self.controller.flashcardDetailWidgets[index], self.controller.flashcardDetailWidgets[index+1] = self.controller.flashcardDetailWidgets[index+1], self.controller.flashcardDetailWidgets[index]

        self._update_display_and_data()

    def _update_display_and_data(self):
        index = 1
        for flashcardDetailWidget in self.controller.flashcardDetailWidgets:
            flashcardDetailWidget.pack_forget()
            flashcardDetailWidget.flashcardIndexLabel.configure(text=f"flashcard {index}")
            flashcardDetailWidget.pack(expand=True, fill='both', padx=stg.PADX, pady=stg.PADY)
            index += 1

    def update_flashcard_info(self):
        self.term = self.termLabel.info
        self.definition = self.definitionLabel.info

class FlashcardComponent(CustomFrame):
    def __init__(self, master: FlashcardsDetailsWidget, text, info, column=0, row=0, columnspan=1, rowspan=1, grid_enabled=True):
        self.master: FlashcardsDetailsWidget = master
        super().__init__(self.master, column, row, columnspan, rowspan, grid_enabled)
        self.grid_rowconfigure((0), weight=1)
        self.grid_rowconfigure((1), weight=5)
        self.grid_columnconfigure((0,1), weight=1)

        self.info = info
        
        CustomLabel(
            master=self,
            text=text,
            column=0, row=0
        ).grid_configure(
            sticky='new',
            pady=0)

        CustomButton(
            master=self,
            text='Edit',
            command=self._edit,
            column=1, row=0
        ).grid_configure(
            sticky='new',
            pady=0)

        self.infoLabel = CustomLabel(
            master=self,
            text=info,
            largetexttype=1,
            column=0, row=1,
            columnspan=2)
        self.infoLabel.grid_configure(
            sticky='new',)

    def _edit(self):
        self.entryFrame = CustomFrame(
            master=self,
            column=0, row=1, columnspan=2)
        self.entryFrame.grid_configure(sticky='new')
        self.entryFrame.configure(
            width=self.infoLabel.winfo_width(),
            height=self.infoLabel.winfo_height())
        self.entryFrame.pack_propagate(False)

        self.entry = tk.Text(
            master=self.entryFrame,
            width=1, height=1,
            background=stg.KEYWORD_COLOUR, 
            wrap=tk.WORD,
            font=stg.COMMON_FONT)
        self.entry.insert(tk.INSERT, self.info)

        self.entry.tag_add(tk.SEL, "1.0", tk.END)
        self.entry.mark_set(tk.INSERT, "1.0")
        self.entry.see(tk.INSERT)

        self.entry.pack(expand=True, fill='both')

        self.entry.focus()
        if stg.MODE == 'dark':
            self.infoLabel.configure(fg=stg.DARK_TEXT_COLOUR)

        self.done = CustomButton(
            master=self,
            text='done',
            command=self._done,
            column=1, row=0)
        self.done.grid_configure(
            sticky='new',
            pady=0)

        self.grid_configure(sticky='new')

    def _done(self):    
        self.info = self.entry.get("1.0", tk.END)[:-1]
        self.infoLabel.configure(text=self.info)

        self.entryFrame.destroy()
        self.entry.destroy()
        self.done.destroy()

        self.infoLabel.grid(column=0, row=1, columnspan=2, sticky='new', padx=stg.PADX, pady=stg.PADY)
        self.update()

        self.master.update_flashcard_info()