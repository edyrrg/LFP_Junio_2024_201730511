from src.models.error import Error
from src.models.token import Token


class Lexer:
    def __init__(self, input_sequence):
        self.input_sequence = input_sequence
        self.tokens = []
        self.errors = []

    def state_zero(self, character, line, column):
        if character.isalpha():
            return 1
        elif character == "-":
            return 2
        elif character == "'":
            return 3
        elif character in [';', '[', ']', ':', ',', '{', '}', '>']:
            return 4
        elif character == ".":
            return 5
        elif ord(character) in {32, 10, 9}:
            return 0
        else:
            self.errors.append(Error("N/A", "N/A", line, column, character))
            return 0

    def analyze(self):
        line, column = 1, 1
        state, prev_state = 0, 0
        lexeme = ""

        for character in self.input_sequence:
            if state == 0:
                state = self.state_zero(character, line, column)
                if state == 0:
                    lexeme = ""
                else:
                    lexeme += character

            elif state == 1:
                if character.isalpha():
                    lexeme += character
                else:
                    if lexeme in ["nombre", "nodos", "conexiones"]:
                        self.tokens.append(Token("PALABRA RESERVADA", lexeme, line, column - len(lexeme)))
                    else:
                        self.errors.append(Error("PALABRA RESERVADA", lexeme, line, column, "N/A"))

                    lexeme = ""

                    state = self.state_zero(character, line, column)
                    if state != 0:
                        lexeme += character

            elif state == 2:
                if character == ">":
                    lexeme += character
                    self.tokens.append(Token("ASIGNACIÓN", lexeme, line, column - len(lexeme) - 1))
                    lexeme = ""
                    state = 0
                else:
                    self.errors.append(Error("ASIGNACIÓN", lexeme, line, column, character))
                    state = 0
                    lexeme = ""

            elif state == 3:
                if character == "'":
                    lexeme += character
                    self.tokens.append(Token("STRING", lexeme, line, column - len(lexeme)))
                    lexeme = ""
                    state = 0
                elif character == "\n":
                    self.errors.append(Error("STRING", lexeme, line, column, character))
                    state = 0
                    lexeme = ""
                else:
                    state = 3
                    lexeme += character

            elif state == 4:
                self.tokens.append(Token("SIGNO", lexeme, line, column - len(lexeme)))
                lexeme = ""
                state = self.state_zero(character, line, column)
                if state != 0:
                    lexeme += character

            elif state == 5:
                lexeme += character
                if lexeme == "...":
                    self.tokens.append(Token("SEPARADOR", lexeme, line, column - len(lexeme)))
                    lexeme = ""
                    state = 0
                elif len(lexeme) > 3:
                    self.errors.append(Error("SEPARADOR", lexeme, line, column, character))
                    state = 0
                    lexeme = ""

            if ord(character) == 10:
                line += 1
                column = 1
            elif ord(character) == 9:
                column += 4
            else:
                column += 1
