import os
import threading
from tkinter import ttk, messagebox, filedialog
import tkinter as tk
import graphviz
import time
from jinja2 import Environment, FileSystemLoader

from src.scanner.lexer import Lexer


class OperationMenuFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, height=10, width=40, padx=10, pady=10)
        self.parent = parent
        self.lexer: Lexer = None
        title_label = ttk.Label(self, text="Archivos")
        title_label.grid(column=0, row=0, padx=10, pady=10)
        upload_file_button = ttk.Button(self, text="Cargar Archivo", command=lambda: self.file_handler())
        upload_file_button.grid(column=0, row=1, padx=10, pady=10, ipadx=10, ipady=10)
        exec_file_button = ttk.Button(self, text="Ejecutar Archivo", command=lambda: self.exec_analyze_file())
        exec_file_button.grid(column=0, row=2, padx=10, pady=10, ipadx=10, ipady=10)

        title_label = ttk.Label(self, text="Reportes")
        title_label.grid(column=1, row=0, padx=10, pady=10)
        upload_file_button = ttk.Button(self, text="Reporte de Tokens", command=lambda: self.create_token_report())
        upload_file_button.grid(column=1, row=1, padx=10, pady=10, ipadx=10, ipady=10)
        exec_file_button = ttk.Button(self, text="Reporte de Errores", command=lambda: self.create_errors_report())
        exec_file_button.grid(column=1, row=2, padx=10, pady=10, ipadx=10, ipady=10)
        self.progress_bar = ttk.Progressbar(self, orient="horizontal", length=300)

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
            self.lexer = Lexer(input_text)
            self.lexer.analyze()
            self.start()
            list_images = self.create_digraphs(self.lexer.tokens)
            self.parent.send_list_images(list_images)
        else:
            messagebox.showerror("Error", "No se ha selecciono un archivo aun")

    def show_info(self):
        messagebox.showinfo(title="Info", message="Archivos disponibles")

    def start(self):
        self.progress_bar['value'] = 0
        self.progress_bar['maximum'] = 100
        self.progress_bar.grid(column=0, row=3, columnspan=2, pady=10)
        threading.Thread(target=self.process).start()

    def process(self):
        for i in range(100):
            time.sleep(0.008)
            self.progress_bar['value'] = i + 1
            self.update_idletasks()
        self.progress_bar.grid_forget()
        tk.messagebox.showinfo("Completado", "Análisis lexico terminado.")

    def create_digraphs(self, tokens):
        titulo = ""
        nodos, conexiones = [], []
        es_titulo, son_nodos, son_conexiones = False, False, False

        list_images = {}

        directory = "../assets/img/"

        if not os.path.exists(directory):
            os.makedirs(directory)

        for i, token in enumerate(tokens):
            if token.lexeme == "nombre":
                es_titulo = True
            elif es_titulo and token.name == "STRING":
                titulo = token.lexeme.replace("'", "")
                es_titulo = False

            if token.lexeme == "nodos":
                son_nodos = True
            elif son_nodos and token.name == "STRING":
                nodos.append(token.lexeme.replace("'", ""))
            elif son_nodos and token.lexeme == ";":
                son_nodos = False

            if token.lexeme == "conexiones":
                son_conexiones = True
            elif son_conexiones and token.name == "STRING":
                conexiones.append(token.lexeme.replace("'", ""))
            elif son_conexiones and token.lexeme == ";":
                son_conexiones = False

            if token.name == "SEPARADOR" or (i == (len(tokens) - 1) and (token.lexeme == ";" or token.lexeme == "]")):
                filepath = os.path.join(directory, titulo)
                graph = graphviz.Digraph(name=titulo, filename=filepath, format="png")
                for index in range(0, len(nodos), 2):
                    if index + 1 < len(nodos):
                        graph.node(nodos[index], nodos[index + 1])

                for index in range(0, len(conexiones), 2):
                    if index + 1 < len(conexiones):
                        graph.edge(conexiones[index], conexiones[index + 1])

                graph.attr(label=titulo)
                graph.render()
                list_images[titulo] = filepath
                titulo, nodos, conexiones = "", [], []

        return list_images

    def create_token_report(self):
        path = filedialog.askdirectory(title="Seleccione una ubicación donde guardar el reporte", initialdir="C:/")

        if path == "" and path is None:
            messagebox.showerror("Error", "Seleccione primero una ubicacion para guardar reporte")
            return

        elif self.lexer is None:
            messagebox.showerror("Error", "Primero ejecute el archivo antes de generar el repote")
            return

        env = Environment(loader=FileSystemLoader('templates'))

        template = env.get_template('template_tokens.html')

        html_output = template.render(tokens=self.lexer.tokens)

        save_file_path = os.path.join(path, "reporte_tokens.html")

        with open(save_file_path, 'w') as f:
            f.write(html_output)
            f.close()

        messagebox.showinfo("Completado", "Reporte de Tokens creado")

    def create_errors_report(self):
        path = filedialog.askdirectory(title="Seleccione una ubicación donde guardar el reporte", initialdir="C:/")

        if path == "" and path is None:
            messagebox.showerror("Error", "Seleccione primero una ubicacion para guardar reporte")
            return

        elif self.lexer is None:
            messagebox.showerror("Error", "Primero ejecute el archivo antes de generar el repote")
            return

        env = Environment(loader=FileSystemLoader('templates'))

        template = env.get_template('template_errors.html')

        html_output = template.render(errors=self.lexer.errors)

        save_file_path = os.path.join(path, "reporte_errores.html")

        with open(save_file_path, 'w') as f:
            f.write(html_output)
            f.close()

        messagebox.showinfo("Completado", "Reporte de Errores creado")
