class Token:
    def __init__(self, token, lexeme, line, column, tk_type):
        self.__token = token
        self.__lexeme = lexeme
        self.__line = line
        self.__column = column
        self.__tk_type = tk_type

    @property
    def token(self):
        return self.__token

    @property
    def lexeme(self):
        return self.__lexeme

    @property
    def line(self):
        return self.__line

    @property
    def column(self):
        return self.__column

    @property
    def tk_type(self):
        return self.__tk_type

    def __str__(self):
        return (f'TOKEN: token {self.token}, lexeme {self.lexeme}, line {self.line}'
                f', column {self.column}, type {self.tk_type}')
