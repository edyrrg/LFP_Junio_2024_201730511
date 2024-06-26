from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QAction, QMainWindow, QTextEdit, QLabel, QPushButton, QFileDialog, QMessageBox

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
        tokens_action.triggered.connect(self.show_tokens)
        errors_action.triggered.connect(self.show_errors)
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
            self.show_alert()

    def show_alert(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Advertencia")
        msg.setText("No se ha seleccionado ningún archivo")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def save_file(self):
        print("Guardar archivo")

    def save_as_file(self):
        print("Guardar archivo como...")

    def show_tokens(self):
        print("Mostrar tokens")

    def show_errors(self):
        print("Mostrar errores")

    def show_parse_tree(self):
        print("Mostrar árbol de derivación")

    def exec_code(self):
        input_text = self.text_edit.toPlainText()
        lexer = Lexer(input_text)
        tokens, errors = lexer.tokenize()
        for token in tokens:
            print(token)

        for error in errors:
            print(error)
        parser = Parser(tokens)
        parser.parse()
