class Token:
    def __init__(self, token, tk_type, lexeme, line, column):
        self.__token = token
        self.__type = tk_type
        self.__lexeme = lexeme
        self.__line = line
        self.__column = column

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
    def type(self):
        return self.__type

    def __str__(self):
        return (f'token: {self.token}, type: {self.type}, lexeme: {self.lexeme}, line: {self.line}'
                f', column: {self.column}')
