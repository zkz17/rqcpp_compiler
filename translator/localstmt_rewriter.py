from utils.astnode import *

# Local Statement Rewrite class
class LocalStmtRewriter:
    def __init__(self):
        pass

    def rewrite(self, ast):
        self.visit(ast)

    def visit(self, node):
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name, self.generic_visit)
        return method(node)

    def generic_visit(self, node):
        ## Default method for unhandled nodes
        if not node: return
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
        return []
    
    def visit_BlockNode(self, block):
        statements = []
        for stmt in block._statements:
            new_statements = self.visit(stmt)
            if len(new_statements): statements += new_statements
            else: statements.append(stmt)
        block._statements = statements
        return []
    
    def visit_LocalStmtNode(self, localstmt):
        statements = []
        ## TODO
        return statements