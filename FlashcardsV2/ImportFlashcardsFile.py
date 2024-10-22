from tkinter import filedialog

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