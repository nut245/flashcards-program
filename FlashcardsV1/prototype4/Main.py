import customtkinter as ctk
import tkinter as tk
try:
    from ctypes import windll, byref, sizeof, c_int
except:
    pass

import MenuFile
import PlayFile
import TestFile
import ImportFlashcardsFile

TITLE_HEX_COLOR = 0x000
WINDOW_COLOR = "#000"

class Main(ctk.CTk):
    def __init__(self, *args, **kwargs):

        # window setup
        super().__init__(fg_color=WINDOW_COLOR)
        self.title('Flashcards Program')
        self.geometry('600x400')

        self.importedFlashcards = ImportFlashcardsFile.ImportFlashcards()

        self.create_menubar()

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=100)

        self.container = ctk.CTkFrame(self) 
        self.container.grid(column=0, row=1, sticky='news')
        self.container.columnconfigure(0, weight=1)
        self.container.rowconfigure(0, weight=1)

        self.frames = {} 

        for F in (MenuFile.Menu, PlayFile.Play, TestFile.Test):
            frame = F(parent=self.container, controller=self)
            self.frames[F] = frame
            frame.grid(column=0, row=0, sticky='news')

        self.show_frame(MenuFile.Menu)

        # run
        self.change_title_bar_color()
        self.mainloop()

    def create_menubar(self):
        def back_button_clicked():
            self.show_frame(MenuFile.Menu)
            self.backButton.grid_forget()

        self.backButton = ctk.CTkButton(self, text='<<< back to main menu <<<', 
                                        fg_color=WINDOW_COLOR,
                                        hover_color="#111",
                                        corner_radius=1,
                                        command = back_button_clicked)

    def show_frame(self, cont):
            frame = self.frames[cont]
            frame.tkraise()

    def change_title_bar_color(self):
        try:
            HWND = windll.user32.GetParent(self.winfo_id())
            DWMWA_ATTRIBUTE = 35
            COLOR = TITLE_HEX_COLOR
            windll.dwmapi.DwmSetWindowAttribute(HWND, DWMWA_ATTRIBUTE, byref(c_int(COLOR)), sizeof(c_int))
        except:
            pass

if __name__ == '__main__':
    Main()