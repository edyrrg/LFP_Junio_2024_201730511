import tkinter as tk
from tkinter import ttk

class AppGui:
    def __init__(self, root):
        self.root = root
        self.root.title('Grafos Guatemala')
        self.center_window(1200, 800)
        self.root.resizable(False, False)
        self.label = None
        self.boton = None
        self.create_widgets()

    def center_window(self, _width, _height):
        width_screen = self.root.winfo_screenwidth()
        height_screen = self.root.winfo_screenheight()

        # x = (with_screen / 2) - (20 / 2)
        # y = (height_screen / 2) - (20 / 2)
        x = (width_screen - _width) // 2
        y = (height_screen - _height) // 2

        self.root.geometry(f"{_width}x{_height}+{x}+{y}")

    def create_widgets(self):
        # Crear un label
        self.label = ttk.Label(self.root, text="¡Hola, mundo!")
        self.label.pack(pady=10)

        # Crear un botón
        self.boton = ttk.Button(self.root, text="Haz clic aquí")
        self.boton.pack(pady=10)
