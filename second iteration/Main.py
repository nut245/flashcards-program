import customtkinter as ctk
try:
    from ctypes import windll, byref, sizeof, c_int
except:
    pass

import TextToDict
import Flashcard
import ArrowButton
import CustomButton

TITLE_HEX_COLOR = 0x000
WINDOW_COLOR = "#000"

class Main(ctk.CTk):
    def __init__(self, *args, **kwargs):

        # window setup
        super().__init__(fg_color=WINDOW_COLOR)
        self.title('Flashcards Program')
        self.geometry('600x400')
        #self.resizable(False,False)

        # data
        self.correctDict = {}
        self.wrongDict = {}

        # layout
        self.columnconfigure((0), weight=1, uniform='a')
        self.rowconfigure((0,1,2,3,4,5,6,7,8), weight=1, uniform='a')

        self.arrowFrame = ctk.CTkFrame(self, fg_color=WINDOW_COLOR)
        self.arrowFrame.grid(column=0, row=6, padx=5, sticky='news')
        self.arrowFrame.columnconfigure((0,1,2,3,4), weight=1, uniform='a')
        self.arrowFrame.rowconfigure((0), weight=1, uniform='a')

        self.buttonFrame = ctk.CTkFrame(self)
        self.buttonFrame.grid(column=0, row=7, rowspan=2, padx=5, pady=5, sticky='news')
        self.buttonFrame.columnconfigure((0,1), weight=1, uniform='a')
        self.buttonFrame.rowconfigure((0,1), weight=1, uniform='a')

        # widgets
        self.flashcards = []
        count = 0
        for key, value in TextToDict.dictionary.items():
            self.flashcards.append(Flashcard.Flashcard(self, controller=self, key=key, value=value))
            self.flashcards[count].grid(column=0,row=0, rowspan=6, padx=5, pady=5, sticky='news')
            count += 1
        self.flashcards[0].tkraise()

        self.flashcardsIndex = 0

        self.create_current_over_total_label(frame=self.arrowFrame, column=2, row=0)
        self.create_arrow_button(frame=self.arrowFrame, arrowText='<<<', leftOrRight='Left', column=0, row=0)
        self.create_arrow_button(frame=self.arrowFrame, arrowText='>>>', leftOrRight='Right', column=3, row=0)

        self.create_custom_button('shuffle', column=0, row=0)
        self.create_custom_button('restart', column=1, row=0)

        # run
        self.change_title_bar_color()
        self.mainloop()

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