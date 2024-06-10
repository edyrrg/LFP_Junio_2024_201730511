from tkinter import ttk, messagebox
import tkinter as tk


class ProcessFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.image_paths = [
            "ruta/a/tu/imagen1.jpg",
            "ruta/a/tu/imagen2.jpg",
            "ruta/a/tu/imagen3.jpg"
        ]

        self.combobox = ttk.Combobox(self, values=self.image_paths)
        self.combobox.bind("<<ComboboxSelected>>", self.update_image)
        self.combobox.pack(pady=20)

        self.image_label = tk.Label(self, text="Image here :D", width=50, height=25, bd="1", relief="solid")
        self.image_label.pack(pady=10)

        if self.image_paths:
            self.update_image()

    def update_image(self, event=None):
        pass
