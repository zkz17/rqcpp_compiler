# Symbol class
class Symbol:
    def __init__(self, name, type, value):
        self.name = name
        self.type = type
        self.value = value

# Symbol Table class
class SymbolTable:
    def __init__(self, parent=None):
        self.parent = parent
        self.table = {}

    def define(self, name, type, value=None):
        if name in self.table: raise Exception(f'Conflict definition of variable \'{name}\'')
        else: self.table[name] = Symbol(name, type, value)

    def assign(self, name, type, value=None):
        if name in self.table and self.table[name].type != 'c': type = self.table[name].type
        if type != 'c': raise Exception(f'Variable {name} of type {type} is not assignable')
        self.table[name] = Symbol(name, type, value)

    def resolve(self, name): 
        if name in self.table: 
            return self.table[name]
        elif self.parent:
            return self.parent.resolve(name)
        else: 
            return None