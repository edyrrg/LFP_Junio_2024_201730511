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
        self.__path_file = None
        self.list_images = None
        self.process_frame = None
        self.create_menu()

    def center_window(self, _width, _height):
        width_screen = self.winfo_screenwidth()
        height_screen = self.winfo_screenheight()
        x = (width_screen - _width) // 2
        y = (height_screen - _height) // 2
        self.geometry(f"{_width}x{_height}+{x}+{y}")

    def create_menu(self):
        operation_menu_frame = OperationMenuFrame(self)
        operation_menu_frame.pack(side=tk.TOP, expand=False)
        self.process_frame = ProcessFrame(self)
        self.process_frame.pack(side=tk.TOP, expand=False)

    def send_list_images(self, list_images):
        self.process_frame.set_images(list_images)

    @property
    def path_file(self):
        return self.__path_file

    @path_file.setter
    def path_file(self, value):
        self.__path_file = value
