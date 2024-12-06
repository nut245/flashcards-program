import customtkinter as ctk

class ArrowButton(ctk.CTkButton):
    def __init__(self, parent, controller, arrowText: int, lefOrRight):
        
        self.leftOrRight = lefOrRight

        super().__init__(master=parent,
                         text=arrowText, 
                         command=self.clicked)

        self.controller = controller

    def clicked(self):
        def left_or_right_clicked(leftOrRight):
            if leftOrRight == "Right":
                self.controller.flashcardsIndex += 1
            else:
                self.controller.flashcardsIndex -= 1

        left_or_right_clicked(self.leftOrRight)

        self.controller.update_flashcards()