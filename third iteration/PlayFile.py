import customtkinter as ctk

import ArrowButton
import CustomButton

WINDOW_COLOR = "#000"

class Play(ctk.CTkFrame):
    def __init__(self, parent, controller, *args, **kwargs):

        # window setup
        self.controller = controller

        super().__init__(master=parent, fg_color=WINDOW_COLOR)

        # data
        self.correctDict = {}
        self.wrongDict = {}

        # layout
        self.columnconfigure((0), weight=1, uniform='a')
        self.rowconfigure((0,1,2,3,4,5,6,7,8), weight=1, uniform='a')

        self.arrowFrame = ctk.CTkFrame(self, fg_color='transparent')
        self.arrowFrame.grid(column=0, row=6, padx=5, sticky='news')
        self.arrowFrame.columnconfigure((0,1,2,3,4), weight=1, uniform='a')
        self.arrowFrame.rowconfigure((0), weight=1, uniform='a')

        self.buttonFrame = ctk.CTkFrame(self, fg_color='transparent')
        self.buttonFrame.grid(column=0, row=7, rowspan=2, padx=5, pady=5, sticky='news')
        self.buttonFrame.columnconfigure((0,1), weight=1, uniform='a')
        self.buttonFrame.rowconfigure((0,1), weight=1, uniform='a')

        # widgets
        self.flashcards = self.controller.importedFlashcards.flashcards
        for flashcard in self.flashcards:
            flashcard.set_parent(self)
            flashcard.grid(column=0,row=0, rowspan=6, padx=5, pady=5, sticky='news')
        self.flashcards[0].tkraise()

        self.flashcardsIndex = 0

        self.create_current_over_total_label(frame=self.arrowFrame, column=2, row=0)
        self.create_arrow_button(frame=self.arrowFrame, arrowText='<<<', leftOrRight='Left', column=0, row=0)
        self.create_arrow_button(frame=self.arrowFrame, arrowText='>>>', leftOrRight='Right', column=3, row=0)

        self.create_custom_button('shuffle', column=0, row=0)
        self.create_custom_button('restart', column=1, row=0)

    def create_current_over_total_label(self, frame, column, row):
        self.currentOverTotalLabel = ctk.CTkLabel(frame, text=f"{self.flashcardsIndex+1} / {len(self.flashcards)}")
        self.currentOverTotalLabel.grid(column=column, row=row, padx=6, pady=5, sticky='news')

    def create_arrow_button(self, frame, arrowText, leftOrRight, column, row):
        ArrowButton.ArrowButton(frame, controller=self, arrowText=arrowText, lefOrRight=leftOrRight).grid(column=column, columnspan=2, row=row, padx=5, pady=5, sticky='news')

    def create_custom_button(self, text, column, row):
        if text == 'shuffle':
            return CustomButton.ShuffleButton(self.buttonFrame, controller=self, text=text).grid(column=column, row=row, rowspan=2, padx=5, pady=5, sticky='news')
        elif text == 'restart':
            return CustomButton.RestartButton(self.buttonFrame, controller=self, text=text).grid(column=column, row=row, rowspan=2, padx=5, pady=5, sticky='news')

    def update_flashcards(self):
        for index in range(len(self.flashcards)):
            self.flashcards[index].label.configure(text=self.flashcards[index].key)
            self.flashcards[index].update()
            self.flashcards[index].switchVar = True

        try:
            self.flashcards[self.flashcardsIndex].tkraise()
        except IndexError:
            self.flashcards[0].tkraise()
            self.flashcardsIndex = 0

        if self.flashcardsIndex < 0:
            self.flashcardsIndex = len(self.flashcards)-1

        self.currentOverTotalLabel.configure(text=f"{self.flashcardsIndex+1 if self.flashcardsIndex < len(self.flashcards) else self.flashcardsIndex} / {len(self.flashcards)}")
        self.currentOverTotalLabel.update()

if __name__ == '__main__':
    Play()