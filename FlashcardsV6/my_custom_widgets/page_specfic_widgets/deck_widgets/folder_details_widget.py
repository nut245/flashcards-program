import tkinter as tk
from my_settings_lib import settingsObj as stg

from tkinter import messagebox as mb

from ...universal_widgets.custom_frame import CustomFrame
from ...universal_widgets.custom_label import CustomLabel
from ...universal_widgets.custom_button import CustomButton

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from my_pages import FolderConfigurer

class FolderDetailsWidget(CustomFrame):
    def __init__(self, controller, parent, folderName, column=0, row=0, columnspan=1, rowspan=1, grid_enabled=True):
        self.controller: FolderConfigurer = controller
        super().__init__(parent, column, row, columnspan, rowspan, grid_enabled)

        self.previousName = folderName
        self.folderName = folderName

        self.nameEdited = False

        self.grid_columnconfigure((0), weight=10)
        self.grid_columnconfigure((1,2), weight=1)
        self.grid_rowconfigure((0), weight=1)

        self.label = CustomLabel(
            master=self,
            text=self.folderName,
            column=0, row=0)

        self.edit = CustomButton(
            master=self,
            text='Edit',
            command=self._edit,
            column=1, row=0)

        self.delete = CustomButton(
            master=self,
            text='Delete',
            command=self._delete,
            column=2, row=0)

    def _edit(self):
        self.entry = tk.Entry(
            master=self, 
            background=stg.KEYWORD_COLOUR, 
            font=stg.COMMON_FONT)
        self.entry.insert(0, self.folderName)
        self.entry.selection_range(0, 'end')
        self.entry.grid(column=0, row=0, sticky='news', padx=stg.PADX, pady=stg.PADY)
        self.entry.focus()
        if stg.MODE == 'dark':
            self.label.configure(fg=stg.DARK_TEXT_COLOUR)

        self.done = CustomButton(
            master=self,
            text='done',
            command=self._done,
            column=1, row=0)

    def _done(self):
        if self.entry.get() == "" or self.entry.get() == self.folderName:
            self.entry.destroy()
            self.done.destroy()
            return
        
        for folderWidget in self.controller.folderDetailsWidgets:
            if self.entry.get() == folderWidget.folderName:
                mb.showerror(title="Name Error", message="Folder name already taken")
                self.entry.destroy()
                self.done.destroy()
                return

        self.folderName = self.entry.get()
        self.label.configure(text=self.folderName)
        self.nameEdited = True

        self.entry.destroy()
        self.done.destroy()

    def _delete(self):
        deleteVerification = mb.askokcancel(title="deleting file", message = "are you sure?")
        if deleteVerification:
            try:
                self.controller.folderDetailsWidgets.remove(self)
                self.destroy()
            except ValueError:
                pass # the user pressed the delete button twice