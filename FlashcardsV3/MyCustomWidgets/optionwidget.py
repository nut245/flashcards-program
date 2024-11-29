import tkinter as tk

class OptionWidget(tk.Frame):
    def __init__(self, parent, text):
        self.text = text
        self.parent = parent

        super().__init__(master=self.parent)

        tk.Label(master=self, text=self.text, width=20).pack(fill='both', expand=True, side='left', padx=5, pady=5)

        self.entry = tk.Entry(master=self, width=20)
        self.entry.pack(fill='both', expand=True, side='left', padx=5, pady=5)