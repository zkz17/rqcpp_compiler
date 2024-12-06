from utils.astnode import *
from utils.symboltable import SymbolTable

# Semantic Analyzer abstract class
class Analyzer:
    def __init__(self):
        self.global_scope = SymbolTable()
        self.current_scope = self.global_scope

    def analyze(self):
        pass

    def visit(self, node):
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name, self.generic_visit)
        method(node)

    def generic_visit(self, node):
        ## Default method for unhandled nodes
        if not isinstance(node, ASTNode): return
        for child in node.__dict__.values():
            if isinstance(child, list):
                for item in child:
                    if isinstance(item, ASTNode): 
                        self.visit(item)
                    elif isinstance(item, tuple): 
                        for element in item:
                            self.visit(element)
            elif isinstance(child, ASTNode): 
                self.visit(child)

    def get_symbol(self, varname):
        symbol = self.current_scope.resolve(varname)
        if not symbol: raise Exception(f'Undefined reference to \'{varname}\'')
        return symbol

    def enter_scope(self, block):
        self.current_scope = block._symbols

    def exit_scope(self):
        self.current_scope = self.current_scope.parent