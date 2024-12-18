from my_settings_lib import settingsObj as stg

from my_custom_widgets import SubPage, TitleWidget, VerticalScrolledFrame, EmbeddedPages

from .folder_manager import FolderManager

class DecksPage(SubPage):
    """
    window that hosts all 'decks', that stores pre-imported flashcards into program

    all decks found with decks_data.json

    allows for organisation of decks through dynamic folders system
    """
    def __init__(self, master):
        super().__init__(master=master)
        self.title("Decks")

        self.grid_columnconfigure((0), weight=1)
        self.grid_columnconfigure((1), weight=10)

        self.grid_rowconfigure((0), weight=2)
        self.grid_rowconfigure((1), weight=1)
        self.grid_rowconfigure((2), weight=10)

        TitleWidget(
            master=self,
            text="Decks").titleLabel.configure(
            font=(stg.TITLE_FONT[0], stg.TITLE_FONT[1]-10, stg.TITLE_FONT[2]))

        self.tabsFrame = VerticalScrolledFrame(
            parent=self,
            column=0, row=2).interior

        self.embeddedPages = EmbeddedPages(
            controller=self,
            pages=None,
            column=1, row=0, rowspan=3)

        self.folderManager = FolderManager(
            controller=self, 
            parent=self, 
            folderFrame=self.tabsFrame, 
            row=1, column=0)