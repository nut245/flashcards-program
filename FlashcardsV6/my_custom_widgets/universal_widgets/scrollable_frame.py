import tkinter as tk
from tkinter import ttk
from tkinter.constants import *

from my_settings_lib import settingsObj as stg

class VerticalScrolledFrame(ttk.Frame):
    def __init__(self, parent, column=0, row=0, columnspan=1, rowspan=1):
        """A pure Tkinter scrollable frame that actually works!
        * Use the 'interior' attribute to place widgets inside the scrollable frame.
        * Construct and pack/place/grid normally.
        * This frame only allows vertical scrolling.
        """
        ttk.Frame.__init__(self, parent)

        # Create a canvas object and a vertical scrollbar for scrolling it.
        self.vscrollbar = ttk.Scrollbar(self, orient=VERTICAL)
        self.vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        self.canvas = tk.Canvas(self, bd=0, highlightthickness=0,
                           yscrollcommand=self.vscrollbar.set)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        self.vscrollbar.config(command=self.canvas.yview)

        # Reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # Create a frame inside the canvas which will be scrolled with it.
        self.interior = interior = tk.Frame(self.canvas)
        self.interior_id = self.canvas.create_window(0, 0, window=interior,
                                           anchor=NW)
        
        self.grid(
            row=row, 
            column=column, 
            rowspan=rowspan, 
            columnspan=columnspan,
            padx=stg.PADX, pady=stg.PADY, sticky='news'
        )

        self.interior.configure(background=stg.BACKGROUND_COLOUR)
        self.canvas.configure(background=stg.BACKGROUND_COLOUR)

        interior.bind('<Configure>', self._configure_interior)
        self.canvas.bind('<Configure>',self._configure_canvas)

    # Track changes to the canvas and frame width and sync them,
    # also updating the scrollbar.
    def _configure_interior(self, event):
        # Update the scrollbars to match the size of the inner frame.
        size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
        self.canvas.config(scrollregion="0 0 %s %s" % size)
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # Update the self.canvas's width to fit the inner frame.
            self.canvas.config(width=self.interior.winfo_reqwidth())

    def _configure_canvas(self, event):
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # Update the inner frame's width to fill the canvas.
            self.canvas.itemconfigure(self.interior_id, width=self.canvas.winfo_width())