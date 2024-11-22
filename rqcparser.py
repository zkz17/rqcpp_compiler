from astnode import *

# Parser class
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def parse(self):
        return self.program()
    
    def program():
        