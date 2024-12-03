from utils.astnode import *

# AST Rewriter abstract class
class Rewriter: 
    def __init__(self, prefix):
        self.temp_var_prefix = prefix
        self.temp_var_counter = 0
        self.available_temp_name = []

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
    
    def get_tempvar_name(self):
        if len(self.available_temp_name):
            return self.available_temp_name.pop()
        name = self.temp_var_prefix + str(self.temp_var_counter)
        self.temp_var_counter += 1
        return name
    
    def free_tempvar_name(self, names):
        if isinstance(names, list): self.available_temp_name += names
        else: self.available_temp_name.append(names)