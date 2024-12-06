import customtkinter as ctk
import PlayFile

WINDOW_COLOR = "#000"

class Menu(ctk.CTkFrame):
    def __init__(self, parent, controller, *args, **kwargs):

        # window setup
        self.controller = controller

        super().__init__(master=parent, fg_color=WINDOW_COLOR)

        self.rowconfigure((0, 1, 2, 3, 4, 5), weight=1, uniform='a')
        self.columnconfigure((0,1,2,4), weight=1, uniform='a')

        self.playButton = self.create_menu_button("Play", row=1)

        self.testButton = self.create_menu_button("Test", row=2)

        self.editButton = self.create_menu_button("Edit", row=3)
        
        self.importButton = self.create_menu_button("Import", row=4)

    def create_menu_button(self, text, row):
        def configure_command():
            self.controller.backButton.grid(column=0, row=0, sticky='news')

            if text == "Play":
                self.controller.show_frame(PlayFile.Play)

            elif text == "Test":
                print("you have pressed test")

            elif text == "Edit":
                print("you have pressed edit")

            elif text == "Import":
                print("you have pressed import")

            else:
                print("MyOwnError (Menu): that was not a valid input")

        button = ctk.CTkButton(self, text=text, 
                                        width=250,
                                        height=50,
                                        command=configure_command)
        button.grid(row=row, column=1, pady=10, columnspan=2, sticky='news')
        return button