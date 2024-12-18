# Symbol class
class Symbol:
    # name: str
    # type: Type
    # size: int
    def __init__(self, name, type, size=1):
        self.name = name
        self.type = type
        self.size = size
        self.array = {} # { int: TODO }

    def defined(self, index):
        return index in self.array

    def assign_element(self, index, value=0):
        self.array[index] = value

    def get_element(self, index):
        if not self.defined(index): return None
        return self.array[index]

# Symbol Table class
class SymbolTable:
    def __init__(self, parent=None):
        self.parent = parent
        if parent: parent.children.append(self)
        self.children = []
        self.table = {}
        self.free_var = {}

    def allocate(self, name, type, size):
        self.table[name] = Symbol(name, type, size)

    def define(self, name, type, index=None):
        if name in self.table: 
            if index: 
                if index._value >= self.table[name].size: 
                    raise Exception(f'Procedure array index out of range, max: {self.table[name].size - 1}, given: {index}')
                if self.table[name].defined(index._value):
                    raise Exception(f'Conflict definition of array element \'{name}[{index._value}]\'')
                self.table[name].assign_element(index._value)
            else: raise Exception(f'Conflict definition of variable \'{name}\'')
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