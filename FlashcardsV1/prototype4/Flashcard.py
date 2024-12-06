import customtkinter as ctk

class Flashcard(ctk.CTkFrame):
    def __init__(self, key, value, parent = None):

        # frame set up
        self.key = key
        self.value = value

        # data
        self.switchVar = True

        # widgets
        #font = ctk.CTkFont(family=HEADING_FONT, size=HEADING_FONT_SIZE)
        self.update_flashcard(parent=parent)

    def switch_label(self, event):
        self.switchVar = not self.switchVar
        if self.switchVar == True:
            self.label.configure(text=self.key)
            self.label.update()
        else:
            self.label.configure(text=self.value)
            self.label.update()
    
    def set_parent(self, parent):
        self.parent = parent
        self.update_flashcard(parent)
    
    def update_flashcard(self, parent):
        super().__init__(master=parent, fg_color="#504c54")

        self.label = ctk.CTkLabel(self, text=self.key)#, font=font)
        self.label.pack(expand=True, fill='both')

        self.label.bind("<Button-1>", self.switch_label)