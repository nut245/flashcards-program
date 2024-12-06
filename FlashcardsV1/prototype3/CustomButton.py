import customtkinter as ctk
import random


class RestartButton(ctk.CTkButton):
    def __init__(self, parent, controller, text):

        super().__init__(master=parent,
                         text=text, 
                         command=self.restart)
        
        self.controller = controller

        self.flashcardsSaved = self.controller.flashcards.copy()
        
    def restart(self):
        self.controller.flashcards = self.flashcardsSaved
        self.controller.flashcards[0].tkraise()
        self.controller.flashcardsIndex = 0
        self.controller.update_flashcards()


class ShuffleButton(ctk.CTkButton):
    def __init__(self, parent, controller, text):

        super().__init__(master=parent,
                         text=text, 
                         command=self.shuffle)
        
        self.controller = controller
        
    def shuffle(self):
        self.controller.flashcards = sorted(self.controller.flashcards, key=lambda x: random.random())
        self.controller.update_flashcards()


class AccuracyButton(ctk.CTkButton):
    def __init__(self, parent, controller, text):

        super().__init__(master=parent,
                         text=text, 
                         command=self.accuracy)
        
        self.controller = controller
        self.text = text

    def accuracy(self):
        if self.text == 'correct':
            self.controller.correctDict[self.controller.flashcards[self.controller.flashcardsIndex].key] = self.controller.flashcards[self.controller.flashcardsIndex].value
            #print(f"good dict: {self.controller.correctDict}")

        elif self.text == 'wrong':
            self.controller.wrongDict[self.controller.flashcards[self.controller.flashcardsIndex].key] = self.controller.flashcards[self.controller.flashcardsIndex].value
            #print(f"bad dict: {self.controller.wrongDict}")

        else:
            print("My Own Error (AccuracyButton): invalid argument passed")