import tkinter as tk
from tkinter import ttk


class AppGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('LF - Proyecto 2')
        self.resizable(False, False)
        self.center_window(1000, 600)
        self.menu = ttk.Menu(self, tearoff=0)

    def center_window(self, _width, _height):
        width_screen = self.winfo_screenwidth()
        height_screen = self.winfo_screenheight()
        x = (width_screen - _width) // 2
        y = (height_screen - _height) // 2
        self.geometry(f"{_width}x{_height}+{x}+{y}")
