import customtkinter as ctk
import SettingsFile
import random

class Play(ctk.CTkFrame):
    def __init__(self, parent):

        # window setup
        self.parent = parent
        #self.grid(column=0, row=1, sticky='news')
        super().__init__(master=self.parent, fg_color=SettingsFile.WINDOW_COLOR)
        self.flashcardsIndex = self.parent.flashcards.index

        # layout
        self.columnconfigure((0), weight=1)
        self.rowconfigure((0,1,2,3,4,5,6,7), weight=1)

        self.flashcardFrame = ctk.CTkFrame(self)

        self.arrowFrame = ctk.CTkFrame(self, fg_color='transparent')
        self.arrowFrame.columnconfigure((0,1,2,3,4), weight=1)
        self.arrowFrame.rowconfigure((0), weight=1)

        self.buttonFrame = ctk.CTkFrame(self, fg_color='transparent')
        self.buttonFrame.columnconfigure((0,1), weight=1)
        self.buttonFrame.rowconfigure((0,1,2), weight=1)

        self.flashcardFrame.grid(column=0, row=0, rowspan=6, sticky='news')
        self.arrowFrame.grid(column=0, row=6, padx=5, sticky='news')
        self.buttonFrame.grid(column=0, row=7, rowspan=2, sticky='news')

        # widgets
        self.next_button = ctk.CTkButton(master=self.arrowFrame, text='>>>', command= lambda : self.button_pressed('>>>'))
        self.next_button.grid(column=3, columnspan=2, row=0, pady=5, sticky='news')

        self.prev_button = ctk.CTkButton(master=self.arrowFrame, text='<<<', command= lambda : self.button_pressed('<<<'))
        self.prev_button.grid(column=0, columnspan=2, row=0, pady=5, sticky='news')

        self.create_current_over_total_label()

        self.shuffle_button = ctk.CTkButton(master=self.buttonFrame, text='Shuffle', command=self.shuffle)
        self.shuffle_button.grid(column=0, row=0, rowspan=2, padx=5, pady=5, sticky='news')

        self.restart_button = ctk.CTkButton(master=self.buttonFrame, text='Restart', command=self.restart)
        self.restart_button.grid(column=1, row=0, rowspan=2, padx=5, pady=5, sticky='news')

        self.refresh_button = ctk.CTkButton(master=self.buttonFrame, text='Refresh', command=self.refresh_flashcards)
        self.refresh_button.grid(column=0, row=2, columnspan=2, padx=5, pady=5, sticky='news')

    def button_pressed(self, button):
        if button == '>>>':
            self.parent.flashcards.next()
        else:
            self.parent.flashcards.previous()
        self.flashcardsIndex = self.parent.flashcards.index
        self.update_current_over_total_label()

    def create_current_over_total_label(self):
        self.currentOverTotalLabel = ctk.CTkLabel(self.arrowFrame, text=f"{self.flashcardsIndex+1 if self.flashcardsIndex < len(self.parent.importedFlashcards.dictionary) else self.flashcardsIndex} / {len(self.parent.importedFlashcards.dictionary)}\n"+
                                                  f"{round((self.flashcardsIndex+1)/len(self.parent.importedFlashcards.dictionary)*100)}%")
        self.currentOverTotalLabel.grid(column=2, row=0, padx=5, pady=5, sticky='news')

    def update_current_over_total_label(self):
        self.currentOverTotalLabel.configure(text=f"{self.flashcardsIndex+1 if self.flashcardsIndex < len(self.parent.importedFlashcards.dictionary) else self.flashcardsIndex} / {len(self.parent.importedFlashcards.dictionary)}\n"+
                                                  f"{round((self.flashcardsIndex+1)/len(self.parent.importedFlashcards.dictionary)*100)}%")

    def shuffle(self):
        temporary_flashcards_list = list(self.parent.flashcards.dictionary.items())
        random.shuffle(temporary_flashcards_list)
        self.parent.flashcards.dictionary = dict(temporary_flashcards_list)

    def restart(self):
        self.parent.flashcards.dictionary = self.parent.importedFlashcards.dictionary
        self.flashcardsIndex = 0
        self.parent.flashcards.restart()
        self.update_current_over_total_label()

    def refresh_flashcards(self):
        self.parent.importedFlashcards.create_dictionary(newFile=False)
        self.restart()