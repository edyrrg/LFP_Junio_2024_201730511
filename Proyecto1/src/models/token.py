class Token:
    def __init__(self, name, lexeme, line, column):
        self.name = name
        self.lexeme = lexeme
        self.line = line
        self.column = column

    def __str__(self):
        return f'Token - {self.name} {self.lexeme} (line: {self.line}, column: {self.column})'

