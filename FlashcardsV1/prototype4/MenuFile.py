import customtkinter as ctk
import PlayFile
import TestFile

WINDOW_COLOR = "#000"

class Menu(ctk.CTkFrame):
    def __init__(self, parent, controller, *args, **kwargs):

        # window setup
        self.controller = controller

        super().__init__(master=parent, fg_color=WINDOW_COLOR)

        self.rowconfigure((0, 1, 2, 3, 4, 5), weight=1, uniform='a')
        self.columnconfigure((0,1,2,4), weight=1, uniform='a')

        self.playButton = self.create_menu_button("Play", row=1)

        self.testButton = self.create_menu_button("Test", row=2)

        self.editButton = self.create_menu_button("Edit", row=3)
        
        self.importButton = self.create_menu_button("Import", row=4)

    def create_menu_button(self, text, row):
        def configure_command():
            if text == "Play":
                self.controller.show_frame(PlayFile.Play)
                self.bind_flashcards(PlayFile.Play)

            elif text == "Test":
                self.controller.show_frame(TestFile.Test)
                self.controller.frames[TestFile.Test].correctDict = {}
                self.controller.frames[TestFile.Test].wrongDict = {}

                for button in self.controller.frames[TestFile.Test].buttons:
                    button.destroy()
                self.controller.frames[TestFile.Test].currentOverTotalLabel.destroy()
                self.controller.frames[TestFile.Test].resultLabel.destroy()
                
                self.controller.frames[TestFile.Test].buttons = []
                self.controller.frames[TestFile.Test].buttons.append(self.controller.frames[TestFile.Test].create_correct_button())
                self.controller.frames[TestFile.Test].buttons.append(self.controller.frames[TestFile.Test].create_wrong_button())
                self.controller.frames[TestFile.Test].create_current_over_total_label()
                
                self.bind_flashcards(TestFile.Test)

            elif text == "Edit":
                print("you have pressed edit")

            elif text == "Import":
                self.controller.importedFlashcards.dictionary = {}
                self.controller.importedFlashcards.flashcards = []
                self.controller.importedFlashcards.create_dictionary()
                self.controller.importedFlashcards.create_flashcards()

            else:
                print("MyOwnError (Menu): that was not a valid input")

            if text != "Import":
                self.controller.backButton.grid(column=0, row=0, sticky='news')

        button = ctk.CTkButton(self, text=text, 
                                        width=250,
                                        height=50,
                                        command=configure_command)
        button.grid(row=row, column=1, pady=10, columnspan=2, sticky='news')
        return button
    
    def bind_flashcards(self, frame):
        self.controller.frames[frame].flashcardsIndex = 0
        self.controller.frames[frame].create_flashcards()
        self.controller.flashcards = self.controller.importedFlashcards.flashcardsSaved
        self.controller.flashcards[0].tkraise()
        self.controller.frames[frame].update_flashcards()