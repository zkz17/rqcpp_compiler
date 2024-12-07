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
        if parent: parent.children.append(self)
        self.children = []
        self.table = {}
        self.free_var = {}

    def define(self, name, type):
        if name in self.table: raise Exception(f'Conflict definition of variable \'{name}\'')
        else: self.table[name] = Symbol(name, type)

    def assign(self, name, type):
        if not name in self.table: self.table[name] = Symbol(name, type)

    def resolve(self, name): 
        if name in self.table: 
            return self.table[name]
        elif self.parent:
            symbol = self.parent.resolve(name)
            if symbol and symbol.type.is_classical():
                self.free_var[symbol.name] = symbol
            return symbol
        else: 
            return None
        
    def free_vars(self):
        return self.free_var
    
    def print_indent(self, level=0):
        print('    ' * level, end='')
    
    def print(self, level=0):
        if not len(self.table) and not len(self.children): return
        self.print_indent(level)
        print('{')
        for name, symbol in self.table.items():
            self.print_indent(level + 1)
            if not symbol.type.is_array(): print(f'{name}: {type(symbol.type).__name__}')
            else:
                vartype = symbol.type
                print(f'{name}: {type(symbol.type).__name__}', end='')
                dims = ''
                while vartype.is_array():
                    dims = f'[{vartype.length}]' + dims
                    vartype = vartype.element_type
                print(dims)

        for child in self.children:
            child.print(level + 1)

        self.print_indent(level)
        print('}')