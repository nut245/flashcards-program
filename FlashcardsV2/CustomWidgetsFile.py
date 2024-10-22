import customtkinter as ctk
import SettingsFile
import MenuFile

class BackButton(ctk.CTkButton):
    def __init__(self, parent):

        self.parent = parent
        super().__init__(master=self.parent,
                         text='<<< back to main menu <<<', 
                         fg_color=SettingsFile.WINDOW_COLOR,
                         hover_color="#111",
                         corner_radius=1,
                         command=self.back_button_clicked)

    def back_button_clicked(self):
        self.grid_forget()
        self.parent.show_frame(MenuFile.Menu)