import customtkinter as ctk
import SettingsFile
from ImportFlashcardsFile import ImportFlashcards
from FlashcardsFile import Flashcards
import CustomWidgetsFile
from MenuFile import Menu
from PlayFile import Play

try:
    from ctypes import windll, byref, sizeof, c_int
except:
    pass

class Main(ctk.CTk):
    def __init__(self):

        # window setup
        super().__init__(fg_color=SettingsFile.WINDOW_COLOR)
        self.title('Flashcards Program')
        self.geometry('600x400')

        self.importedFlashcards = ImportFlashcards()

        self.flashcards = Flashcards(dictionary=self.importedFlashcards.dictionary)

        # main/window layout
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=100)

        # 'instantiates' back button
        self.backButton = CustomWidgetsFile.BackButton(parent=self)

        # frame setup
        self.frames = {} 

        for F in (Menu, Play):
            frame = F(parent=self)
            self.frames[F] = frame
            frame.grid(column=0, row=1, sticky='news')

        self.show_frame(Menu)

        self.change_title_bar_color()
        self.mainloop()

    def show_frame(self, cont):
            frame = self.frames[cont]
            frame.tkraise()

    def recreate_flashcards(self, flashcardsParent):
        try:
            self.flashcards.destroy()
        except: pass
        self.flashcards = Flashcards(dictionary=self.importedFlashcards.dictionary, parent=flashcardsParent)

    def change_title_bar_color(self):
        try:
            HWND = windll.user32.GetParent(self.winfo_id())
            DWMWA_ATTRIBUTE = 35
            COLOR = SettingsFile.TITLE_HEX_COLOR
            windll.dwmapi.DwmSetWindowAttribute(HWND, DWMWA_ATTRIBUTE, byref(c_int(COLOR)), sizeof(c_int))
        except:
            pass

if __name__ == '__main__':
    Main()