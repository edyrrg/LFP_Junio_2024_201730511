import os
from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageTk


class ProcessFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.name_images = None
        self.list_images = None
        self.combobox = ttk.Combobox(self, state='disabled')
        self.combobox.set("...")
        self.combobox.bind("<<ComboboxSelected>>", self.update_image)
        self.combobox.pack(pady=20)
        self.image_label = tk.Label(self, bd="1", relief="solid")
        self.image_label.pack_forget()
        self.current_path_image = None

    def update_image(self, event):
        self.current_path_image = self.list_images[self.combobox.get()] + ".png"

        if os.path.exists(self.current_path_image):
            imagen = Image.open(self.current_path_image)
            imagen_tk = ImageTk.PhotoImage(imagen)
            self.image_label.config(image=imagen_tk)
            self.image_label.image = imagen_tk
            self.image_label.pack(pady=10)
        else:
            print(f'Imagen no encontrada: {self.current_path_image}')

    def set_images(self, list_images):
        self.list_images = list_images
        self.name_images = list(list_images.keys())
        self.combobox.set("Seleccione una imagen")
        self.combobox['values'] = self.name_images
        self.combobox.state(["!disabled", "readonly"])
