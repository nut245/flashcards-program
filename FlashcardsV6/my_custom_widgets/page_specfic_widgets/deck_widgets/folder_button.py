import tkinter as tk

import static_json

from ...universal_widgets.custom_button import CustomButton
from my_pages.decks_pages.folder_contents import FolderContents

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from my_pages import DecksPage

class FolderButton(CustomButton):
    """
    button that is the path to folders, within decks_data.json, for users
    """
    def __init__(self, controller, parent, folder, column=0, row=0, columnspan=1, rowspan=1, grid_enabled=True):
        """
        ### Paramaters
        - controller: DecksPage
            - to give access to its properties
        - parent: tk.Frame
            - to place FolderButton() into, which in this case is DeckPage()'s tabsFrame
        - folder: str
            - the name of the folder, displayed as text
            - also used for path to DeckPage()'s EmbeddedPages()'s frames - that display the contents of the folder
        - folderValue: dict[str]
            - the contents within the folder FolderButton() represents
        """
        self.controller: DecksPage = controller

        self.folder = folder

        super().__init__(
            master=parent, 
            text=self.folder, 
            command=self._open_folder, 
            column=column, 
            row=row, 
            columnspan=columnspan, 
            rowspan=rowspan, 
            grid_enabled=grid_enabled
        )

    def _open_folder(self):
        """
        attempts to display folder contents to user, but will instatiate a new one in case it does not exist
        """
        self.folderValue = static_json.parse_json(file="decks_data.json")["folders"][self.folder]
        try:
            self.controller.embeddedPages.show_frame(self.folder)
        except KeyError:
            self._populate_folder()

    def _populate_folder(self):
        """
        instatiates the contents within folder

        re-utilising EmbeddedPages() code has meant initialising values must be slightly unorthodox/un-pythonic
        """
        self.controller.embeddedPages.construct_frames(newFrame=FolderContents, frameName=self.folder)

        self.controller.embeddedPages.frames[self.folder].initialise(
            controller=self.controller,
            folder=self.folder,
            decks=self.folderValue)