class SyntacticalError:
    def __init__(self, error_token, line, column, expected_token):
        self.__error_token = error_token
        self.__line = line
        self.__column = column
        self.__expected_token = expected_token

    @property
    def error_token(self):
        return self.__error_token

    @property
    def line(self):
        return self.__line

    @property
    def column(self):
        return self.__column

    @property
    def expected_token(self):
        return self.__expected_token

    def __str__(self):
        return f'Syntax Error: {self.error_token}, ({self.line}, {self.column}), Expected Token: {self.expected_token}'
