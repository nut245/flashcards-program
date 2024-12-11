import tkinter as tk

from MyCustomWidgets import VerticalScrolledFrame

from MySettings import SettingsObj as stg

class ThemesPage(VerticalScrolledFrame):
    """
    write new documentation here

    ### Parameter
    - more documentation here too

    ### Properties
    - EVEN MORE DOCUMENTATION
    """
    def __init__(self, master):
        super().__init__(parent=master)

        self.interior.configure(background='#EEEEEE')

        self.themeDisplayWidgets: list[ThemeDisplayWidget] = []

        self.index=0
        while self.index < len(stg.THEMES):
            currentTheme = stg.THEMES[self.index]
            self.themeDisplayWidgets.append(
                ThemeDisplayWidget(
                    master=self.interior,
                    controller=self,
                    index=self.index,
                    mode=currentTheme['mode'],
                    background=currentTheme['background'],
                    frame=currentTheme['frame'],
                    accent=currentTheme['accent'],
                    button=currentTheme['button'],
                    keyword=currentTheme['keyword'],
                    definition=currentTheme['definition'],
                    wrong=currentTheme['wrong'],
                    correct=currentTheme['correct']
                )
            )
            self.themeDisplayWidgets[self.index].pack(expand=True, fill='both', padx=stg.PADX, pady=stg.PADY)

            self.index += 1

    def retrieve_chosen_theme_index(self):
        for theme in self.themeDisplayWidgets:
            if theme.chosen:
                return theme.index
        return stg.INDEX

class ThemeDisplayWidget(tk.Frame):
    def __init__(self, master, controller: ThemesPage, index, mode, background, frame, accent, button, keyword, definition, wrong, correct):
        self.controller: ThemesPage = controller
        super().__init__(master=master, background=background)

        self.index = index
        self.chosen = False

        self.frame = tk.Frame(
            master=self,
            background=frame
        )
        self.frame.pack(expand=True, fill='both', padx=stg.PADX, pady=stg.PADY)

        self.frame.grid_rowconfigure((0,1,2), weight=1)
        self.frame.grid_columnconfigure((0,1), weight=1)

        self.title = tk.Label(
            master=self.frame,
            text="title",
            background=accent,
            font=(stg.TITLE_FONT[0], stg.TITLE_FONT[1]-25, stg.TITLE_FONT[2]),
            relief='ridge',
            borderwidth=6
        )
        self.title.grid(column=0, row=0, rowspan=2, sticky='news', padx=stg.PADX, pady=stg.PADY)

        self.label = tk.Label(
            master=self.frame,
            text='label',
            background=accent,
            font=stg.COMMON_FONT
        )
        self.label.grid(column=1, row=0, sticky='news', padx=stg.PADX, pady=stg.PADY)

        self.button = tk.Button(
            master=self.frame,
            text='button',
            background=button,
            font=stg.COMMON_FONT
        )
        self.button.grid(column=1, row=1, sticky='news', padx=stg.PADX, pady=stg.PADY)

        self.wrong = tk.Label(
            master=self.frame,
            text="wrong",
            background=accent,
            foreground=wrong,
            font=(stg.COMMON_FONT[0], stg.COMMON_FONT[1], 'bold')
        )
        self.wrong.grid(column=0, row=2, sticky='news', padx=stg.PADX, pady=stg.PADY)

        self.correct = tk.Label(
            master=self.frame,
            text="correct",
            background=accent,
            foreground=correct,
            font=(stg.COMMON_FONT[0], stg.COMMON_FONT[1], 'bold')
        )
        self.correct.grid(column=1, row=2, sticky='news', padx=stg.PADX, pady=stg.PADY)

        for frame in self.winfo_children():
            frame.bind("<Button-1>", lambda _ : self.select_theme())
            for child in frame.winfo_children():
                child.bind("<Button-1>", lambda _ : self.select_theme())

        if mode == 'dark':
            self.title.configure(foreground=stg.DARK_TEXT_COLOUR)
            self.label.configure(foreground=stg.DARK_TEXT_COLOUR)
            self.button.configure(foreground=stg.DARK_TEXT_COLOUR)

    def select_theme(self):
        for themeDisplayWidget in self.controller.themeDisplayWidgets:
            themeDisplayWidget.chosen = False
            themeDisplayWidget.configure(highlightthickness=0, highlightbackground='#EEEEEE')

        self.chosen = True
        self.configure(highlightthickness=5, highlightbackground='red')