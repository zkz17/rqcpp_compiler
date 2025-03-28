import re

# Define token types
TOKEN_TYPES = [
    ('INTEGER', r'\d+'),
    ('KET', r'\|\d+>'),
    ('RARROW', r'\->'),
    ('PLUS', r'\+'),
    ('MINUS', r'\-'),
    ('MULTIPLY', r'\*'),
    ('GREATEREQ', r'>='),
    ('GREATERTHAN', r'>'),
    ('LESSEQ', r'<='),
    ('LESSTHAN', r'<'),
    ('EQUALTO', r'=='),
    ('NOTEQUAL', r'!='),
    ('AND', r'and\b'),
    ('OR', r'or\b'),
    ('NOT', r'not\b'),
    ('SKIP', r'skip\b'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('LBRACKET', r'\['),
    ('RBRACKET', r'\]'),
    ('ASSIGN', r'='),
    ('QBITS', r'qbits\b'),
    ('ARRAY', r'array\b'),
    ('PROCEDURE', r'procedure\b'),
    ('MAIN', r'main\b'),
    ('QIF', r'qif\b'),
    ('FIQ', r'fiq\b'),
    ('IF', r'if\b'),
    ('THEN', r'then\b'),
    ('ELIF', r'elif\b'),
    ('ELSE', r'else\b'),
    ('FI', r'fi\b'),
    ('WHILE', r'while\b'),
    ('DO', r'do\b'),
    ('OD', r'od\b'),
    ('BEGIN', r'begin\b'),
    ('LOCAL', r'local\b'),
    ('END', r'end\b'),
    ('ID', r'[\_A-Za-z][\_A-Za-z0-9]*'),
    ('COLON', r':'),
    ('SEMICOLON', r';'),
    ('COMMA', r','),
    ('WHITESPACE', r'\s+')
]

# Token class
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f'Token({self.type}, {self.value})'
    
# Lexer class
class RQCLexer:
    def __init__(self, text):
        self.text = text
        self._tokens = []
        self.current_indent = 0
        self.line_start = True

    def tokens(self):
        return self._tokens

    def tokenize(self):
        lines = self.text.splitlines()
        for line in lines:
            stripped_line = line.lstrip()
            if not stripped_line:
                continue  # Skip empty lines

            indent = len(line) - len(stripped_line)
            if indent > self.current_indent:
                self._tokens.append(Token('INDENT', None))
            elif indent < self.current_indent:
                while indent < self.current_indent:
                    self._tokens.append(Token('DEDENT', None))
                    self.current_indent -= 4  # Assuming 4 spaces per indent

            self.current_indent = indent

            # Tokenize the actual content
            self.line_start = True
            self._tokenize_line(stripped_line)

        # Handle remaining DEDENT tokens at the end
        while self.current_indent > 0:
            self._tokens.append(Token('DEDENT', None))
            self.current_indent -= 4

    def _tokenize_line(self, line): 
        if self.line_start: 
            self._tokens.append(Token('NEWLINE', None))
            self.line_start = False
        pos = 0
        while pos < len(line):
            for token_type, pattern in TOKEN_TYPES:
                regex = re.compile(pattern)
                match = regex.match(line, pos)
                if match:
                    value = match.group(0)
                    if token_type != 'WHITESPACE':
                        self._tokens.append(Token(token_type, value))
                    pos = match.end()
                    break
            else:
                raise Exception(f'Invalid character: {line[pos]}')