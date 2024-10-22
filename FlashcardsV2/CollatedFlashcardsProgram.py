import customtkinter as ctk
from tkinter import filedialog
import random
import SettingsFile

try:
    from ctypes import windll, byref, sizeof, c_int
except:
    pass

class Flashcards(ctk.CTkFrame):
    def __init__(self, dictionary: dict, parent=None):

        # flashcard setup
        self.dictionary = {}
        for key, val in dictionary.items():
            self.dictionary[key] = val
        self.index = 0
        self.key, self.value = list(self.dictionary.items())[self.index]
        super().__init__(master=parent, fg_color="#504c54")

        self.switchVar = True

        # widgets
        font = ctk.CTkFont(family='calibri', size=SettingsFile.FLASHCARD_FONT_SIZE)
        self.label = ctk.CTkLabel(self, text=self.key, wraplength=900, justify='left', font=font)
        self.label.pack(expand=True, fill='both')

        self.label.bind("<Button-1>", self.switch_label)

    def update(self):
        self.key, self.value = list(self.dictionary.items())[self.index]

        if self.switchVar == True:
            self.label.configure(text=self.key)
            self.label.update()
        else:
            self.label.configure(text=self.value)
            self.label.update()

    def switch_label(self, *args, **kwargs):
        self.switchVar = not self.switchVar
        self.update()

    def next(self):
        self.index += 1
        if self.index > len(self.dictionary)-1:
                self.index = 0
        self.switchVar = True
        self.update()

    def previous(self):
        self.index -= 1
        if self.index < 0:
            self.index = len(self.dictionary)-1
        self.switchVar = True
        self.update()

    def restart(self):
        self.index = 0
        self.switchVar = True
        self.update()

class ImportFlashcards():
    def __init__(self):
        self.dictionary = {}
        self.create_dictionary()

    def create_dictionary(self, newFile=True):
        self.dictionary.clear()
        line_count = 0
        if newFile:
            self.file = self.open_file()
        with open(self.file, encoding='utf8') as file:
            for line in file:
                try:
                    (key, val) = line.split(' : ')
                except ValueError:
                    if '\n' in line:
                        val += line[2:]

                    elif line != '\n':
                        print(f"was unable to unpack line {line_count+1} : '{line[:-1]}'", end='\n\n')

                self.dictionary[key] = val[:-1]
                line_count += 1

    def open_file(self):
        return filedialog.askopenfilename().replace('/', '//')
    


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
        self.parent.show_frame(Menu)



class Menu(ctk.CTkFrame):
    def __init__(self, parent):

        # window setup
        self.parent = parent
        super().__init__(master=self.parent, fg_color=SettingsFile.WINDOW_COLOR)

        # layout
        self.rowconfigure((0, 1, 2, 3, 4, 5), weight=1, uniform='a')
        self.columnconfigure((0,1,2,4), weight=1, uniform='a')

        # widgets
        self.playButton = self.create_menu_button(text="Play", file=Play, row=1)
        self.importButton = self.create_menu_button(text="Import", row=4)

    def create_menu_button(self, text, row, file=None):
        def configure_command():
            if text != "Import":
                self.parent.backButton.grid(column=0, row=0, sticky='news')
                self.parent.show_frame(file)

                self.parent.recreate_flashcards(flashcardsParent=self.parent.frames[file].flashcardFrame)
                self.parent.flashcards.pack(expand=True, fill='both')

            # when 'Import' passed as text
            else:
                self.parent.importedFlashcards.create_dictionary()

            if text == "Play":
                self.parent.frames[file].update_current_over_total_label()

        button = ctk.CTkButton(self, text=text, 
                                        width=250,
                                        height=50,
                                        command=configure_command)
        button.grid(row=row, column=1, pady=10, columnspan=2, sticky='news')
        return button



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
        self.backButton = BackButton(parent=self)

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