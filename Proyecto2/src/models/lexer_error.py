class LexerError:
    def __init__(self, token, lexeme, line, column, character):
        self.token = token
        self.lexeme = lexeme
        self.line = line
        self.column = column
        self.character = character

        if character == " ":
            self.character = "blank space"
        else:
            self.character = character

    def __str__(self):
        return f'Error: {self.token} {self.lexeme} (line: {self.line}, column: {self.column}), {self.character}'
