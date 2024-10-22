import customtkinter as ctk
import SettingsFile
import PlayFile

class Menu(ctk.CTkFrame):
    def __init__(self, parent):

        # window setup
        self.parent = parent
        super().__init__(master=self.parent, fg_color=SettingsFile.WINDOW_COLOR)

        # layout
        self.rowconfigure((0, 1, 2, 3, 4, 5), weight=1, uniform='a')
        self.columnconfigure((0,1,2,4), weight=1, uniform='a')

        # widgets
        self.playButton = self.create_menu_button(text="Play", file=PlayFile.Play, row=1)
        self.importButton = self.create_menu_button(text="Import", row=4)

    def create_menu_button(self, text, row, file=None):
        def configure_command():
            if text != "Import":
                self.parent.backButton.grid(column=0, row=0, sticky='news')
                self.parent.show_frame(file)

                self.parent.recreate_flashcards(flashcardsParent=self.parent.frames[file].flashcardFrame)
                self.parent.flashcards.pack(expand=True, fill='both')

            # when 'Import' passed as text
            else:
                self.parent.importedFlashcards.create_dictionary()

            if text == "Play":
                self.parent.frames[file].update_current_over_total_label()

        button = ctk.CTkButton(self, text=text, 
                                        width=250,
                                        height=50,
                                        command=configure_command)
        button.grid(row=row, column=1, pady=10, columnspan=2, sticky='news')
        return button