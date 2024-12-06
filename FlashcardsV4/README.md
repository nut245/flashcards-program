## Release Notes

### Completed features
- Importable text files for conversion into flashcards
- Fully-functional usage for flashcards
- Reloadable flashcards and information on-the-fly (whilst program is open)
- Implementation of procedurally generated 'Jeoprody'-esque questions/quiz
  - Results of quiz on completion
- Immediate output of results with feedback after completion of quiz
- 

- Original green theme and design (as well as easy implementation of new themes)
- keybinds for mouse-independant shortcuts (not yet customisable)

- Implementation of MySettings library
  - handles all appearences of library
  - to be used to store keybinds

- Abstraction of widget appearence attributes
  - stored within 'custom...' files

- Bug Fixes & Error Handling
  - in case flashcards are not supplied
  - null or non-integer values past into 'TestConfigurer' entry widgets
  - implentation of type hinting, leveraged in IntelliSense

### Future Endeavors
- Exportation of flashcards to desired file fomarts
- Preserved 'decks' of flashcards, without need for file access
  - insertable images
  - control over options within "Test Your Knowledge" quiz

- Repeating of wrong answers within "Test Your Knowledge" quiz

- Leverging active recall techniques
  - "I remember", "I somewhat remember", "I don't remember" options within flashcards
  - saving different versions of flashcards to cater to active recall

- diagram flashcards (notoriously pay-walled)

- Future proofing
  - further code documentation for use cases of each class/functions
  - creation of naming standards within program
  - renaming of polymorphic or ambiguous function and variable names
