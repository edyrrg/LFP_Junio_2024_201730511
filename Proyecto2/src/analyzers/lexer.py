from src.models.lexer_error import LexerError
from src.models.token import Token


class Lexer:
    key_words = ["Array", "new", "asc"]
    key_words_name = {"Array": "tk_array",
                      "new": "tk_new",
                      "asc": "tk_asc"}
    SORT = "sort"
    SAVE = "save"
    booleans = ["TRUE", "FALSE"]
    booleans_name = {"TRUE": "tk_boolean_true",
                     "FALSE": "tk_boolean_false"}
    symbols = [";", "(", ")", "[", "]", ",", "."]
    symbols_name = {";": "tk_punto_y_coma",
                    "(": "tk_parentesis_apertura",
                    ")": "tk_parentesis_cierre",
                    "[": "tk_corchete_apertura",
                    "]": "tk_corchete_cierre",
                    ",": "tk_coma",
                    ".": "tk_punto"}

    def __init__(self, input_text):
        self.input_text = input_text
        self.position = 0
        self.current_char = input_text[self.position] if input_text else None
        self.line, self.column = None, None
        self.tokens, self.errors = [], []

    def next_char(self):
        self.position += 1
        if self.position < len(self.input_text):
            self.current_char = self.input_text[self.position]
        else:
            self.current_char = None

    def tokenize(self):
        self.line, self.column = 1, 0
        while self.current_char is not None:
            if self.current_char.isalpha() and self.current_char in {"A", "n", "a", "T", "F", "s"}:
                self._keyword()
            elif self.current_char.isalpha() and self.current_char.islower():
                self._identifier()
            elif self.current_char in self.symbols:
                self._symbol()
            elif self.current_char == "=":
                self._assign()
            elif self.current_char.isdigit():
                self._number()
            elif self.current_char == "/":
                self._comment()
            elif ord(self.current_char) == 34:
                self._string()
            elif ord(self.current_char) == 32:
                self.next_char()
            else:
                self.count_line_or_column()
                if ord(self.current_char) != 10:
                    self.errors.append(LexerError("UNKOWN", self.current_char, self.line, self.column, self.current_char))
                self.next_char()

        return self.tokens, self.errors

    def _identifier(self, sending=None):
        result = self.current_char if sending is None else sending + self.current_char
        self.next_char()
        while ((self.current_char is not None and not self.current_char.isspace()
                and not (self.current_char in self.symbols)) and self.current_char != "="
               and self.current_char.isalnum()) or (self.current_char == "_" or self.current_char == "-"):
            result += self.current_char
            self.next_char()
        self.count_line_or_column()
        tmp_token = Token("tk_identifier", "ID", result, self.line, self.column)
        self.tokens.append(tmp_token)

    def _keyword(self):
        result = ""
        while self.current_char is not None and ord(self.current_char) != 32 and self.current_char.isalpha():
            result += self.current_char
            self.next_char()
        self.count_line_or_column()
        if result in self.key_words:
            tmp_token = Token(self.key_words_name[result], "KEYWORD", result, self.line, self.column)
            self.tokens.append(tmp_token)
        elif result in self.booleans:
            tmp_token = Token(self.booleans_name[f"{result}"], "BOOLEAN", result, self.line, self.column)
            self.tokens.append(tmp_token)
        elif result == self.SORT:
            tmp_token = Token("tk_sort", "SORT", result, self.line, self.column)
            self.tokens.append(tmp_token)
        elif result == self.SAVE:
            tmp_token = Token("tk_save", "SAVE", result, self.line, self.column)
            self.tokens.append(tmp_token)
        elif result.isalpha() and result.islower() and (self.current_char.isalnum() or self.current_char == "_"):
            self._identifier(result)
        else:
            tmp_error = LexerError("KEYWORD", result, self.line, self.column, self.current_char)
            self.errors.append(tmp_error)

    def _symbol(self):
        result = self.current_char
        self.count_line_or_column()
        self.next_char()
        tmp_token = Token(self.symbols_name[result], "SYMBOL", result, self.line, self.column)
        self.tokens.append(tmp_token)

    def _assign(self):
        result = self.current_char
        self.count_line_or_column()
        self.next_char()
        tmp_token = Token("tk_assign", "ASSIGN", result, self.line, self.column)
        self.tokens.append(tmp_token)

    def _number(self):
        result = ""
        while self.current_char.isdigit():
            result += self.current_char
            self.next_char()
        if self.current_char == ".":
            self._decimal_number(result)
        elif not self.current_char.isalpha():
            self.count_line_or_column()
            tmp_token = Token("tk_number", "NUMBER", result, self.line, self.column)
            self.tokens.append(tmp_token)
        else:
            tmp_error = LexerError("NUMBER", result, self.line, self.column, self.current_char)
            self.errors.append(tmp_error)

    def _decimal_number(self, result):
        result = result
        while self.current_char == "." or self.current_char.isdigit():
            result += self.current_char
            self.next_char()
        self.count_line_or_column()
        tmp_token = Token("tk_decimal_number", "DECIMAL_NUMBER", result, self.line, self.column)
        self.tokens.append(tmp_token)

    def _comment(self):
        self.next_char()
        if self.current_char == "/":
            self.next_char()
            while self.current_char != "\n":
                self.next_char()
        elif self.current_char == "*":
            self.next_char()
            while self.current_char != "*" and self.input_text[self.position + 1] != "/":
                self.next_char()
            if self.current_char == "*":
                self.next_char()
                if self.current_char == "/":
                    self.next_char()

    def _string(self):
        result = self.current_char
        self.next_char()
        while (self.current_char is not None and ord(self.current_char) != 34 and self.current_char != "\n"
                and not (self.current_char in {";", ",", "(", ")", "[", "]"})):
            result += self.current_char
            self.next_char()
        self.count_line_or_column()
        if self.current_char is not None and self.current_char != "\n" and ord(self.current_char) == 34:
            result += self.current_char
            tmp_token = Token("tk_string", "STRING", result, self.line, self.column)
            self.tokens.append(tmp_token)
            self.next_char()
        else:
            tmp_error = LexerError("STRING", result, self.line, self.column, self.current_char)
            self.errors.append(tmp_error)

    def count_line_or_column(self):
        if self.current_char is not None and self.current_char == "\n":
            self.line += 1
            self.column = 0
        elif self.current_char is not None and ord(self.current_char) == 9:
            self.column += 4
        elif self.current_char is not None:
            self.column += 1


if __name__ == '__main__':
    lexer = Lexer(
        f'Array 5mi_Array = ne*w @Array ["hola", "numero",68,55,48, 99.123];\nmiArray.sort(asc=FALSE);\nmiArray.save("ruta/del/archivo.csv");')
    tokens, errors = lexer.tokenize()
    for token in tokens:
        print(token)
    for error in errors:
        print(error)
