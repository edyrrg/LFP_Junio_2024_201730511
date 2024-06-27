import os
import time

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QAction, QMainWindow, QTextEdit, QLabel, QPushButton, QFileDialog, QMessageBox
from jinja2 import Environment, FileSystemLoader

from src.analyzers.lexer import Lexer
from src.analyzers.parser import Parser


class PyQt5GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('LFP - Proyecto 2')

        self.resize(1100, 700)

        self.path_file = ""

        self.create_menu_bar()

        self.text_edit = None

        self.create_text_editor()

        self.create_ui()

        self.lexer = None

        self.parser = None

        self.lexer_errors = None

        self.parser_errors = None

        self.tokens = None

    def create_menu_bar(self):
        font = QFont("Arial", 11)

        menubar = self.menuBar()
        menubar.setFont(font)
        file_menu = menubar.addMenu('Archivos')

        open_action = QAction('Abrir', self)
        save_action = QAction('Guardar', self)
        save_as_action = QAction('Guardar como...', self)
        open_action.setFont(font)
        save_action.setFont(font)
        save_as_action.setFont(font)

        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(save_as_action)

        reports_menu = menubar.addMenu('Reportes')

        tokens_action = QAction('Tokens', self)
        errors_action = QAction('Errores', self)
        parse_tree_action = QAction('Árbol de derivación', self)
        tokens_action.setFont(font)
        errors_action.setFont(font)
        parse_tree_action.setFont(font)

        reports_menu.addAction(tokens_action)
        reports_menu.addAction(errors_action)
        reports_menu.addAction(parse_tree_action)

        open_action.triggered.connect(self.open_file)
        save_action.triggered.connect(self.save_file)
        save_as_action.triggered.connect(self.save_as_file)
        tokens_action.triggered.connect(self.create_report_tokens)
        errors_action.triggered.connect(self.create_report_errors)
        parse_tree_action.triggered.connect(self.show_parse_tree)

    def create_text_editor(self):
        self.text_edit = QTextEdit(self)
        self.text_edit.setGeometry(110, 100, 900, 475)
        self.text_edit.setPlaceholderText("Editor de código fuente")
        font = QFont("Arial", 12)
        self.text_edit.setFont(font)
        self.text_edit.setStyleSheet("background-color: lightyellow; color: blue;")

    def create_ui(self):
        label = QLabel("Editor del listado", self)
        label.move(480, 50)
        font_label = QFont("Arial", 15, QFont.DemiBold)
        label.setFont(font_label)
        label.adjustSize()
        # label.setAlignment(Qt.AlignCenter)
        button = QPushButton('Ejecutar', self)
        font_button = QFont("Arial", 11)
        button.setFont(font_button)
        button.resize(100, 50)
        button.move(550, 600)
        button.clicked.connect(self.exec_code)

    def open_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar Archivo a Cargar", "C:/",
                                                   "Archivos de texto (*.lfp)",
                                                   options=options)
        if file_path != "" and file_path is not None:
            self.path_file = file_path
            file = open(self.path_file, "r", encoding="utf-8")
            input_text = file.read()
            self.text_edit.setText(input_text)
        else:
            self.show_alert("Advertencia", "No se ha seleccionado ningún archivo")

    def show_alert(self, title, message):
        alert = QMessageBox()
        alert.setWindowTitle(title)
        alert.setText(message)
        alert.setIcon(QMessageBox.Warning)
        alert.setStandardButtons(QMessageBox.Ok)
        alert.exec_()

    def show_notification(self, title, message):
        notification = QMessageBox()
        notification.setWindowTitle(title)
        notification.setText(message)
        notification.setIcon(QMessageBox.Information)
        notification.setStandardButtons(QMessageBox.Ok)
        notification.exec_()

    def save_file(self):
        print("Guardar archivo")

    def save_as_file(self):
        print("Guardar archivo como...")

    def create_report_tokens(self):
        options = QFileDialog.Options()
        folder_path = QFileDialog.getExistingDirectory(self, 'Seleccionar Carpeta', 'C:/', options=options)
        if folder_path is None or folder_path == "":
            self.show_alert('Error', 'Por favor, selecciona una carpeta primero para guardar el reporte.')
            return

        if self.lexer is None or self.parser is None:
            self.show_alert('Error', 'Por favor, primero ejecute las instrucciones antes de generar el reporte de tokens.')
            return

        current_time = int(time.time())

        env = Environment(loader=FileSystemLoader("src/template/"))

        template = env.get_template('template_tokens.html')

        html_output = template.render(tokens=self.tokens)

        save_file_path = os.path.join(folder_path, f"reporte_tokens_{current_time}.html")

        with open(save_file_path, 'w') as f:
            f.write(html_output)
            f.close()

        self.show_notification("Completado", f"Reporte de tokens creado y guardado en\n{save_file_path}")

    def create_report_errors(self):
        options = QFileDialog.Options()
        folder_path = QFileDialog.getExistingDirectory(self, 'Seleccionar Carpeta', 'C:/', options=options)
        if folder_path is None or folder_path == "":
            self.show_alert('Error', 'Por favor, selecciona una carpeta primero para guardar el reporte.')
            return

        if self.lexer is None or self.parser is None:
            self.show_alert('Error', 'Por favor, primero ejecute las instrucciones antes de generar el reporte de errores.')
            return

        current_time = int(time.time())

        env = Environment(loader=FileSystemLoader("src/template/"))

        template = env.get_template('template_errors.html')

        html_output = template.render(lexer_errors=self.lexer_errors, syntactical_errors=self.parser_errors)

        save_file_path = os.path.join(folder_path, f"reporte_errores_{current_time}.html")

        with open(save_file_path, 'w') as f:
            f.write(html_output)
            f.close()

        self.show_notification("Completado", f"Reporte de errores creado y guardado en\n{save_file_path}")

    def show_parse_tree(self):
        print("Mostrar árbol de derivación")

    def exec_code(self):
        input_text = self.text_edit.toPlainText()
        self.lexer = Lexer(input_text)
        tokens, self.lexer_errors = self.lexer.tokenize()
        self.tokens = tokens.copy()
        for token in tokens:
            print(token)
        for error in self.lexer_errors:
            print(error)

        self.parser = Parser(tokens)
        self.parser_errors = self.parser.parse()
        for syntactical_error in self.parser_errors:
            print(syntactical_error)
