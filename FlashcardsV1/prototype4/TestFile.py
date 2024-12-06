import customtkinter as ctk

import CustomButton

WINDOW_COLOR = "#000"

class Test(ctk.CTkFrame):
    def __init__(self, parent, controller, *args, **kwargs):

        # window setup
        self.controller = controller

        super().__init__(master=parent, fg_color=WINDOW_COLOR)

        # layout
        self.columnconfigure((0,1), weight=1, uniform='a')
        self.rowconfigure((0,1,2,3,4,5,6,7,8), weight=1, uniform='a')

        # data
        self.flashcards = self.controller.importedFlashcards.flashcards
        self.correctDict = {}
        self.wrongDict = {}
        self.flashcardsIndex = 0

        # widgets
        self.create_flashcards()
        self.create_current_over_total_label()
        self.buttons = []
        self.buttons.append(self.create_wrong_button())
        self.buttons.append(self.create_correct_button())

        self.resultLabel = ctk.CTkLabel(self)
        
    def create_correct_button(self):
        self.correctButton = CustomButton.AccuracyButton(parent=self, controller=self ,text="correct")
        self.correctButton.grid(column=1, row=7, rowspan=2, padx=5, pady=5, sticky='news')
        return self.correctButton

    def create_wrong_button(self):
        self.wrongButton = CustomButton.AccuracyButton(parent=self, controller=self ,text="wrong")
        self.wrongButton.grid(column=0, row=7, rowspan=2, padx=5, pady=5, sticky='news')
        return self.wrongButton

    def create_flashcards(self):
        for flashcard in self.flashcards:
            flashcard.destroy()
        self.flashcards = self.controller.importedFlashcards.flashcards
        for flashcard in self.flashcards:
            flashcard.set_parent(self)
            flashcard.grid(column=0,row=0, rowspan=6, columnspan=2, padx=5, pady=5, sticky='news')
        self.flashcards[0].tkraise()

    def create_current_over_total_label(self):
        self.currentOverTotalLabel = ctk.CTkLabel(self, text=f"{self.flashcardsIndex+1} / {len(self.flashcards)}")
        self.currentOverTotalLabel.grid(column=0, row=6, columnspan=2, sticky='news')

    def update_flashcards(self):
        for index in range(len(self.flashcards)):
            self.flashcards[index].label.configure(text=self.flashcards[index].key)
            self.flashcards[index].update()
            self.flashcards[index].switchVar = True

        try:
            self.flashcards[self.flashcardsIndex].tkraise()
        except IndexError:
            pass

        self.currentOverTotalLabel.configure(text=f"{self.flashcardsIndex+1 if self.flashcardsIndex < len(self.flashcards) else self.flashcardsIndex} / {len(self.flashcards)}")
        self.currentOverTotalLabel.update()

        for button in self.buttons:
            if button.complete == True:
                self.display_end()

    def display_end(self):
        for button in self.buttons:
                button.grid_forget()
        for flashcard in self.controller.importedFlashcards.flashcards:
            flashcard.grid_forget()
        self.currentOverTotalLabel.grid_forget()

        self.resultLabel = ctk.CTkLabel(self, text=f"You got {len(self.correctDict)} out of {len(self.flashcards)}\n\nwhich is {round(100 * float(len(self.correctDict))/float(len(self.flashcards)), 2)}%")
        self.resultLabel.grid(row=0, column=0, columnspan=2, rowspan=9, sticky='news')