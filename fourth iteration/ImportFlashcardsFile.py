from tkinter import filedialog
import Flashcard

class ImportFlashcards():
    def __init__(self):
        self.dictionary = {}
        self.flashcards = []
        self.create_dictionary()
        self.create_flashcards()
        self.flashcardsSaved = self.flashcards.copy()

    def create_flashcards(self):
        flashcards_count = 0
        for key, value in self.dictionary.items():
            self.flashcards.append(Flashcard.Flashcard(key=key, value=value))
            flashcards_count += 1
        self.flashcardsSaved = self.flashcards.copy()

    def create_dictionary(self):
        line_count = 0
        try:
            with open(self.open_file()) as file:
                for line in file:
                    try:
                        (key, val) = line.split(' : ')
                    except ValueError:
                        print(f"was unable to unpack line {line_count+1} : '{line[:-1]}'", end='\n\n')
                    self.dictionary[key] = val[:-1]
                    line_count += 1
        except:
            print("The file you have chosen could not be read\n")
            self.create_dictionary()

    def open_file(self):
        return filedialog.askopenfilename().replace('/', '//')