import os
import tkinter as tk
from tkinter import ttk, messagebox, font, filedialog

from src.gui.process_frame import ProcessFrame
from src.gui.operation_menu_frame import OperationMenuFrame
from src.scanner.lexer import Lexer


class AppGui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Grafos Guatemala')
        global_font = font.Font(family="Arial", size=12)
        self.option_add("*Font", global_font)
        self.center_window(1000, 800)
        self.resizable(False, False)
        self.create_menu()
        self.__path_file = None


    def center_window(self, _width, _height):
        width_screen = self.winfo_screenwidth()
        height_screen = self.winfo_screenheight()

        # x = (with_screen / 2) - (20 / 2)
        # y = (height_screen / 2) - (20 / 2)
        x = (width_screen - _width) // 2
        y = (height_screen - _height) // 2

        self.geometry(f"{_width}x{_height}+{x}+{y}")

    def create_menu(self):
        report_operation_menu = OperationMenuFrame(self)
        report_operation_menu.pack(side=tk.TOP, expand=False)
        process_frame = ProcessFrame(self)
        process_frame.pack(side=tk.TOP, expand=False)

    @property
    def path_file(self):
        return self.__path_file

    @path_file.setter
    def path_file(self, value):
        self.__path_file = value
