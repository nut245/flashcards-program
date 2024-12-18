

from my_custom_widgets import SubPage, VerticalScrolledFrame, CustomButton
from my_custom_widgets import FolderDetailsWidget

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .folder_manager import FolderManager

class FolderConfigurer(SubPage):
    """
    window that allows users to add, update/rename, delete their folders

    all functionality (attributes/methods) work internally, developers are not touch!
    """
    def __init__(self, controller, parent):
        """
        ### Paramaters
        - controller: FolderManager
            - to give access to properties within FolderManager()
        - parent: DecksPage
            - to assign ownership to

        ### Properties
        - self.successful: bool
            - to determine whether the 'Save & Continue' button was pressed
            - otherwise all processes skipped
        - self.folderDetailsWidgets: list[FolderDetailsWidget]
            - the widgets that displayed the individual folders, allowing for their updation/renaming and deletion
            - contains information about which folder they represent
        """
        self.controller: FolderManager = controller

        self.successful = False
        self.folderDetailsWidgets: list[FolderDetailsWidget] = []

        super().__init__(master=parent)
        self.geometry(f'600x400+{(self.winfo_screenwidth() // 2 - self.winfo_width()) // 8}+{(self.winfo_screenheight() // 2 - self.winfo_height()) // 8}')

        self.grid_rowconfigure((0), weight=1)
        self.grid_columnconfigure((0,1), weight=1)

        self.foldersFrame = VerticalScrolledFrame(
            parent=self,
            column=0, row=0, columnspan=2).interior

        for folder in self.controller.folderButtons:
            self.folderDetailsWidgets.append(
                FolderDetailsWidget(
                    controller=self,
                    parent=self.foldersFrame,
                    folderName=folder.cget("text"),
                    grid_enabled=False))
        
        CustomButton(
            master=self, 
            text='New Folder', 
            command=self._new_folder, 
            row=1, column=0)
        CustomButton(
            master=self, 
            text='Save & Continue', 
            command=self._retrieve_folders, 
            row=1, column=1)

        # The following commands keep the popup on top.
        self.transient(self.master)      # set to be on top of the main window
        self.grab_set()                  # hijack all commands from the master (clicks on the main window are ignored)
        self.master.wait_window(self)    # pause anything on the main window until this one closes

    def _new_folder(self):
        """
        creates a new folder... simple

        ensures folders do not share the same name (otherwise keys() would be overridden), by incrementing untitledIndex
        """
        self.folderDetailsWidgets.append(
            FolderDetailsWidget(
                controller=self,
                parent=self.foldersFrame,
                folderName=f"untitled {self.controller.untitledIndex}",
                grid_enabled=False
            )
        )
        self.controller.untitledIndex += 1

    def _retrieve_folders(self):
        """
        reconfigures FolderManager()'s folders dictionary, after potential edits have been made by the user
        """
        for folderWidget in self.folderDetailsWidgets:
            try:
                if folderWidget.nameEdited == True:
                    # a folder was renamed
                    self.controller.folders[folderWidget.folderName] = self.controller.folders[folderWidget.previousName]
                    del self.controller.folders[folderWidget.previousName]
                else:
                    # nothing happened to the folder
                    self.controller.folders[folderWidget.folderName] = self.controller.folders[folderWidget.folderName]
            except KeyError:
                # a folder was created
                self.controller.folders[folderWidget.folderName] = {}

        # checks as to whether a folder was deleted
        if len(self.controller.folders) > len(self.folderDetailsWidgets):
            foldersToDelete = []
            for folder in list(self.controller.folders.keys()):
                folderFound = False

                for folderWidget in self.folderDetailsWidgets:
                    if folder == folderWidget.folderName:
                        folderFound = True
                    
                if folderFound == False:
                    foldersToDelete.append(folder)

            for folder in foldersToDelete:
                del self.controller.folders[folder]

        self.successful = True
        self.return_to_main()
