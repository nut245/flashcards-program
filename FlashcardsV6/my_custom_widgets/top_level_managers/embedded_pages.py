import tkinter as tk

class EmbeddedPages():
    """
    manages pages/frames that exist within a child object of SubPage()

    ### Properties
    - self.pages: list[tk.Frame]
        = the paramater passed on EmbeddedPages()'s instantiation to create self.frames 
    - self.frames: dict[str, tk.Frame]
        - the tk.Frame() objects to be displayed within the child object of SubPage()

    #### Methods
    - construct_frames(self, newFrame=None, frameName=None) -> None
        - creates the frames dictionary, done on instantiation with supplied pages
        - allows for insertion of new frames, with developer specified alias/key within frames dictionary
    """
    def __init__(self, controller, pages: list[tk.Frame], row=0, column=0, rowspan=1, columnspan=1):
        self.controller = controller

        self.frames: dict[str, tk.Frame] = {}

        self.pages: list[tk.Frame] = pages

        self.row, self.column = row, column
        self.rowspan, self.columnspan = rowspan, columnspan

        self.construct_frames()

    def clear_frames(self):
        self.frames.clear()
        self.pages.clear()
        self.frames: dict[str, tk.Frame] = {}
        self.pages: list[tk.Frame] = []

    def construct_frames(self, newFrame=None, frameName=None):
        """
        populates frames dictionary with tk.Frame child objects that within self.pages (supplied by user), to be displayed to user
        """
        if newFrame:
            self.pages.append(newFrame)
        
        if self.pages == None:
            self.pages: list[tk.Frame] = []
            return
        
        for F in (self.pages if isinstance(self.pages, list) else [self.pages, ]):
            page_name = F.__name__
            if frameName:
                page_name = frameName
            elif newFrame:
                page_name = newFrame
            frame = F(master=self.controller)
            self.frames[page_name] = frame
            self.frames[page_name].grid_forget() # because frame may potentially inherit from a my_custom_widget, that places itself automatically
        
        self.show_frame(page_name)

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        for frame in self.frames.values():
            frame.grid_forget()

        frame = self.frames[page_name]
        frame.grid(row=self.row, column=self.column, rowspan=self.rowspan, columnspan=self.columnspan, sticky="nsew")
        frame.focus_force()

    def next_page(self, page_name):
        """
        populates the desired page with widgets yet to be instantiated
        - such widgets require information to be gathered from preceding frames
        """
        try:
            self.frames[page_name].populate_page()
        except NameError:
            print(f"{__name__} file. (MyOwnError): child of {self.controller} does not have method populate_page()")

        self.show_frame(page_name)