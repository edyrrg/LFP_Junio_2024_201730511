from src.models.error import Error
from src.models.token import Token


class Lexer:
    def __init__(self, input_sequence):
        self.input_sequence = input_sequence
        self.tokens = []
        self.errors = []

    def is_character_valid(self, character):
        return character in [';', '[', ']', ':', ',', '{', '}', '>']

    def state_zero(self, character, line, column):
        if character.isalpha():
            return 1
        if character == "-":
            return 2
        if character == "'":
            return 3
        if self.is_character_valid(character):
            return 4
        if ord(character) != 32 or ord(character) != 10 or ord(character) == 9:
            pass
        else:
            self.errors.append(Error("N/A", "N/A", line, column, character))
        return 0

    def analyze(self):
        line = 1
        column = 1
        lexeme = ""
        state = 0
        previous_state = 0

        for character in self.input_sequence:
            if state == 0:
                state = self.state_zero(character, line, column)
                lexeme += "" if state == 0 else character
                # if state == 0:
                #     lexeme = ""
                # else:
                #     lexeme += character

            elif state == 1:
                if character.isalpha():
                    lexeme += character
                else:
                    if lexeme in ["nombre", "nodos", "conexiones"]:
                        self.tokens.append(Token("Palabra reservada", lexeme, line, column - len(lexeme)))
                    else:
                        self.errors.append(Error("Palabra reservada", lexeme, line, column, "N/A"))

                    lexeme = ""

                    state = self.state_zero(character, line, column)
                    if state != 0:
                        lexeme += character

            elif state == 2:
                if character == ">":
                    lexeme += character
                    state = 20
                    previous_state = 2
                else:
                    self.errors.append(Error("Asignación", lexeme, line, column, character))
                    state = 0
                    lexeme = ""

            elif state == 3:
                if character == "'":
                    lexeme += character
                    state = 20
                    previous_state = 3
                elif character == "\n":
                    self.errors.append(Error("String", lexeme, line, column, character))
                    state = 0
                    lexeme = ""
                else:
                    state = 3
                    lexeme += character

            elif state == 4:
                self.tokens.append(Token("Signo", lexeme, line, column - len(lexeme)))

                lexeme = ""

                state = self.state_zero(character, line, column)
                if state != 0:
                    lexeme += character

            elif state == 20:
                if previous_state == 2:
                    self.tokens.append(Token("Asignación", lexeme, line, column - len(lexeme)))
                elif previous_state == 3:
                    self.tokens.append(Token("String", lexeme, line, column - len(lexeme)))
                previous_state = 0

                lexeme = ""

                state = self.state_zero(character, line, column)
                if state != 0:
                    lexeme += character

            if ord(character) == 10:
                line += 1
                column = 1
            elif ord(character) == 9:
                column += 4
            else:
                column += 1
