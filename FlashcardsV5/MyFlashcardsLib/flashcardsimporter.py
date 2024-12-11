from tkinter import filedialog

class ImportFlashcards():
    """
    Handles the importing of (currently only) text files.

    ### Attributes
    - self.file: str | None
        - requested file directory from user
    
    - self.dictionary: dict[str, str]
        - parsed text file information, into flashcards format
    """
    def __init__(self):
        self.file = None
        self.dictionary = {}
        self.create_dictionary()

    def create_dictionary(self, newFile=True):
        """
        parses given text/markdown file for key and value pairs (terms and definitions)

        ### Parameter
        - newFile: bool (automatically True)
            - proceeds to parse new file, unless specified otherwise
        """
        if newFile:
            self.file = self.open_file()

        if self.file == '' or self.file == None:
            self.file = None
            return
        
        self.dictionary.clear()
        line_count = 0
    
        with open(self.file, encoding='utf8') as file:
            for line in file:
                try:
                    (key, val) = line.split(' : ')
                except ValueError:
                    if line[:2] == r'\n' or line == '\n':
                        val += line[2:]

                    else:
                        print(f"In [{self.file.replace('//', '/')}]\n\twas unable to unpack line {line_count+1}: '{line[:-1]}'", end='\n\n')

                self.dictionary[key] = val[:-1]
                line_count += 1

    def open_file(self):
        return filedialog.askopenfilename().replace('/', '//')