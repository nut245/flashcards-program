import tkinter as tk
from my_settings_lib import settingsObj as stg

import static_json

from my_custom_widgets.page_specfic_widgets.deck_widgets.folder_button import FolderButton
from .folder_configurer import FolderConfigurer
from my_custom_widgets import CustomButton

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from my_pages import DecksPage

class FolderManager():
    """
    responsible for assigning commands/functionality to all FolderButton()s

    creates FolderButton()s with respective names and deck data, within decks_data.json
    """
    def __init__(self, controller, parent, folderFrame, row=0, column=0):
        """
        ### Paramaters
        - controller: DecksPage
            - for access to attributes and methods within DecksPage(), just out of scope
        - parent: tk.Frame
            - only to place FolderManager()'s 'self.manageFolderButton'
        - folderFrame: tk.Frame
            - to place the FolderButton()s into
        - row, column: int, int = 0, 0
            - to place 'self.manageFolderButton'

        ### Properties
        - self.folders: dict[str]
            - the python dictionary version of decks_data.json
        - self.folderButtons: list[tk.Button]
            - ...a list of the FolderButton()s
        """
        self.controller: DecksPage = controller
        self.parent = parent
        self.folderFrame = folderFrame
        
        self.folders: dict[str] = static_json.parse_json("decks_data.json")["folders"]

        self.folderButtons: list[tk.Button] = []

        self.untitledIndex = 1
        for folder, value in self.folders.items():
            self.folderButtons.append(
                FolderButton(
                    controller=self.controller,
                    parent=self.folderFrame,
                    folder=folder,
                    grid_enabled=False
                )
            )
            self.untitledIndex += 1

        self.manageFoldersButton = CustomButton(
            master=self.parent,
            text='Manage Folders',
            command=self._create_new_folders,
            row=row,
            column=column)

    def _create_new_folders(self):
        """
        recreates/re-instantiates new FolderButtons

        accounting for updation, deletion, or addition 'anomalies'
        """
        self.folders: dict[str] = static_json.parse_json("decks_data.json")["folders"]

        for folderButton in self.folderButtons:
            folderButton.pack_forget()
            # must not delete folderButtons, in case FolderConfigurer was escaped early
        
        folderConfigurer = FolderConfigurer(controller=self, parent=self.controller)

        if folderConfigurer.successful:
            self.folderButtons.clear()
            for folderWidget in folderConfigurer.folderDetailsWidgets:
                self.folderButtons.append(
                    FolderButton(
                        controller=self.controller,
                        parent=self.folderFrame,
                        folder=folderWidget.folderName,
                        grid_enabled=False))

            for frame in self.controller.embeddedPages.frames.values():
                frame.grid_forget()
            self.controller.embeddedPages.clear_frames()

        for folderButton in self.folderButtons:
            folderButton.pack(expand=True, fill='both', pady=stg.PADY, padx=stg.PADX)

        static_json.write_to_json_file(
            file="decks_data.json",
            data={
                "folders": self.folders
            }
        )