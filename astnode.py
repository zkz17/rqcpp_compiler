from symboltable import SymbolTable

# AST Node classes
class ASTNode:
    def __init__(self):
        pass

    def add_symbol(self, symbol, type):
        pass

    def print(self):
        pass

    def equal_to(self, node):
        return False
    
class TopNode(ASTNode):
    # funcs: a list of FuncNode
    def __init__(self, funcs, qregisters):
        self.funcs = funcs
        self.qregisters = qregisters
        self.symbols = SymbolTable()
        for func in self.funcs:
            # TODO
            pass
        for qregister in self.qregisters:
            # TODO
            pass

    def add_symbol(self, symbol, type):
        # TODO
        pass
        for func in self.funcs:
            # TODO
            pass

    def print(self):
        # TODO
        print('Top')
        for qregister in self.qregisters:
            qregister.print()
        print()
        for func in self.funcs:
            func.print()
            print()

class FuncNode(ASTNode):
    # func: IDNode
    # params: a list of IDNode
    # body: BlockNode
    def __init__(self, func, params, body):
        self.func = func
        self.params = params
        self.body = body
        self.symbols = SymbolTable()

    def add_symbol(self, symbol, type):
        # TODO
        pass

    def print(self):
        # TODO
        pass

class QRegisterNode(ASTNode):
    # name: IDNode
    # length: TODO
    def __init__(self, name, length):
        self.name = name
        self.length = length

    def add_symbol(self, symbol, type):
        # TODO
        pass

    def print(self):
        # TODO
        pass