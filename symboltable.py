# Symbol class
class Symbol:
    def __init__(self, name, type):
        self.name = name
        self.type = type

# Symbol Table class
class SymbolTable:
    def __init__(self):
        self.table = []

    def add_symbol(self, name, type):
        self.table.append(Symbol(name, type))