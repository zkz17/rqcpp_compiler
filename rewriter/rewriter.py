from utils.astnode import *

# AST Rewriter abstract class
class Rewriter: 
    def __init__(self, get_tempvar_name, free_tempvar_name):
        self.get_tempvar_name = get_tempvar_name
        self.free_tempvar_name = free_tempvar_name

    def rewrite(self, ast):
        pass

    def visit(self, node):
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name, self.generic_visit)
        return method(node)
    
    def generic_visit(self, node):
        ## Default method for unhandled nodes
        return_list = []
        if not isinstance(node, ASTNode): return return_list
        for child in node.__dict__.values():
            if isinstance(child, list):
                for item in child:
                    if isinstance(item, ASTNode): 
                        return_list += self.visit(item)
                    elif isinstance(item, tuple): 
                        for element in item:
                            return_list += self.visit(element)
            elif isinstance(child, ASTNode): 
                return_list += self.visit(child)
        return return_list