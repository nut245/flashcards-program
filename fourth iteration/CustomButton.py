import customtkinter as ctk
import random
import Main

class RestartButton(ctk.CTkButton):
    def __init__(self, parent, controller, main, text=None):

        super().__init__(master=parent,
                         text=text, 
                         command=self.restart)
        
        self.controller = controller
        self.main = main
        
    def restart(self):
        self.controller.flashcards = self.main.importedFlashcards.flashcardsSaved
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
        self.complete = False

    def accuracy(self):
        try:
            if self.text == 'correct':
                self.controller.correctDict[self.controller.flashcards[self.controller.flashcardsIndex].key] = self.controller.flashcards[self.controller.flashcardsIndex].value
                #print(f"good dict: {self.controller.correctDict}")

            elif self.text == 'wrong':
                self.controller.wrongDict[self.controller.flashcards[self.controller.flashcardsIndex].key] = self.controller.flashcards[self.controller.flashcardsIndex].value
                #print(f"bad dict: {self.controller.wrongDict}")

            else:
                print("MyOwnError (AccuracyButton): invalid argument passed")

            if self.controller.flashcardsIndex == len(self.controller.flashcards)-1:
                raise IndexError
            self.controller.flashcardsIndex += 1

        except IndexError:
            self.complete = True

        self.controller.update_flashcards()

class CurrentOverTotal(ctk.CTkLabel):
    def __init__(self, parent, controller, text):

        super().__init__(master=parent,
                         text=text)
        
        self.controller = controller