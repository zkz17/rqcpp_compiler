# Symbol class
class Symbol:
    # name: str
    # type: Type
    def __init__(self, name, type):
        self.name = name
        self.type = type

# Symbol Table class
class SymbolTable:
    def __init__(self, parent=None):
        self.parent = parent
        self.table = {}
        self.free_var = {}

    def define(self, name, type):
        if name in self.table: raise Exception(f'Conflict definition of variable \'{name}\'')
        else: self.table[name] = Symbol(name, type)

    def assign(self, name, type):
        self.table[name] = Symbol(name, type)

    def resolve(self, name): 
        if name in self.table: 
            return self.table[name]
        elif self.parent:
            symbol = self.parent.resolve(name)
            if symbol and (symbol.type.is_classical() or symbol.type.is_array()):
                self.free_var[symbol.name] = symbol
            return symbol
        else: 
            return None
        
    def free_vars(self):
        return self.free_var