import os
import tkinter as tk
from tkinter import ttk, messagebox, font, filedialog

from src.gui.process_frame import ProcessFrame


class AppGui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Grafos Guatemala')
        global_font = font.Font(family="Helvetica", size=10)
        self.option_add("*Font", global_font)
        self.center_window(1200, 800)
        self.resizable(False, False)
        self.file_paths = {}
        self.frames = {}
        self.current_frame = None
        self.create_menu()
        self.create_frames()

    def center_window(self, _width, _height):
        width_screen = self.winfo_screenwidth()
        height_screen = self.winfo_screenheight()

        # x = (with_screen / 2) - (20 / 2)
        # y = (height_screen / 2) - (20 / 2)
        x = (width_screen - _width) // 2
        y = (height_screen - _height) // 2

        self.geometry(f"{_width}x{_height}+{x}+{y}")

    def create_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        report_menu = tk.Menu(menubar, tearoff=0)

        menubar.add_cascade(label="Archivo", menu=file_menu)
        menubar.add_cascade(label="Reportes", menu=report_menu)

        file_menu.add_command(label="Cargar Archivo", command=lambda: self.file_handler())
        file_menu.add_command(label="Ejecutar Archivo", command=lambda: self.show_info())

        report_menu.add_command(label="Reporte de Tokens", command=lambda: self.show_info())
        report_menu.add_command(label="Reporte de Errores", command=lambda: self.show_info())

    def show_info(self):
        messagebox.showinfo("Estado", "Funciona :D")

    def create_frames(self):
        self.frames["ShowProcessFrame"] = ProcessFrame(self)
        self.frames["ExecFileFrame"] = ttk.Frame(self)
        self.frames["ReportTokensFrame"] = ttk.Frame(self)
        self.frames["ReportErrorsFrame"] = ttk.Frame(self)

        self.show_frame("ShowProcessFrame")

    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.pack(fill=tk.BOTH, expand=True)

        if hasattr(self, 'current_frame') and self.current_frame is not None:
            self.current_frame.pack_forget()

        self.current_frame = frame

    def file_handler(self):
        path = filedialog.askopenfilename(
            title="Seleccione un archivo",
            initialdir="C:/",
            filetypes=[
                ("Archivos", "*.txt"),
            ]
        )
        if path != "" and path is not None:
            # print(path)
            count_path_files = len(self.file_paths)
            count_path_files += 1
            self.file_paths[f"{count_path_files}"] = path
            print(self.file_paths)
        else:
            messagebox.showerror("Error", "No se selecciono un archivo")
