from tkinter import ttk, messagebox, filedialog
import tkinter as tk

from src.scanner.lexer import Lexer


class OperationMenuFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, height=10, width=40, padx=10, pady=10)
        self.parent = parent
        title_label = ttk.Label(self, text="Archivos")
        title_label.grid(column=0, row=0, padx=10, pady=10)
        upload_file_button = ttk.Button(self, text="Cargar Archivo", command=lambda: self.file_handler())
        upload_file_button.grid(column=0, row=1, padx=10, pady=10, ipadx=10, ipady=10)
        exec_file_button = ttk.Button(self, text="Ejecutar Archivo", command=lambda: self.exec_analyze_file())
        exec_file_button.grid(column=0, row=2, padx=10, pady=10, ipadx=10, ipady=10)

        title_label = ttk.Label(self, text="Reportes")
        title_label.grid(column=1, row=0, padx=10, pady=10)
        upload_file_button = ttk.Button(self, text="Reporte de Tokens", command=lambda: self.show_info())
        upload_file_button.grid(column=1, row=1, padx=10, pady=10, ipadx=10, ipady=10)
        exec_file_button = ttk.Button(self, text="Reporte de Errores", command=lambda: self.show_info())
        exec_file_button.grid(column=1, row=2, padx=10, pady=10, ipadx=10, ipady=10)

    def file_handler(self):
        path = filedialog.askopenfilename(
            title="Seleccione un archivo",
            initialdir="C:/",
            filetypes=[
                ("Archivos", "*.txt"),
            ]
        )

        if path != "" and path is not None:
            self.parent.path_file = path
            # messagebox.showinfo("Ruta de archivo de seleccionado", self.parent.path_file)
        else:
            messagebox.showerror("Error", "No se selecciono ningun archivo")

    def exec_analyze_file(self):
        path = self.parent.path_file
        if path != "" and path is not None:
            file = open(self.parent.path_file, "r", encoding="utf-8")
            input_text = file.read()
            lexer = Lexer(input_text)
            lexer.analyze()
            for token in lexer.tokens:
                print(token)
            for error in lexer.errors:
                print(error)
        else:
            messagebox.showerror("Error", "No se ha selecciono un archivo aun")


    def show_info(self):
        messagebox.showinfo(title="Info", message="Archivos disponibles")
