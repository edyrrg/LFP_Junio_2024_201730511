class Lexer:
    def __init__(self, input_text):
        self.tokens = None
        self.input_text = input_text
        self.position = 0
        self.current_char = input_text[self.position] if input_text else None

    def next_char(self):
        self.position += 1
        if self.position < len(self.input_text):
            self.current_char = self.input_text[self.position]
        else:
            self.current_char = None
