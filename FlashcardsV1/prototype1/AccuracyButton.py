import customtkinter as ctk

class AccuracyButton(ctk.CTkButton):
    def __init__(self, parent, controller, text):

        super().__init__(master=parent,
                         text=text, 
                         command=self.accuracy)
        
    def accuracy(self):
        pass