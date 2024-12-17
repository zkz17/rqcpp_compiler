from rewriter.rewriter import Rewriter
from utils.astnode import *

# Expression Extraction Rewrite class
class IndexExtractRewriter(Rewriter):
    def __init__(self, get_tempvar_name, free_tempvar_name):
        super().__init__(get_tempvar_name, free_tempvar_name)

    def rewrite(self, ast):
        self.visit(ast)

    def visit_BlockNode(self, block):
        new_statements = []
        for stmt in block._statements:
            new_statements += self.visit(stmt)
            new_statements.append(stmt)
        
        block._statements = new_statements
        return []
    
    def visit_RangeNode(self, range):
        new_statements = []
        if range._index:
            if not isinstance(range._index, SingletonNode):
                tempvar_name = self.get_tempvar_name()
                tempvar = IDNode(tempvar_name)

                new_statements.append(AssignNode(tempvar, range._index))
                range._index = SingletonNode(tempvar)
        else:
            if range._low and not isinstance(range._low, SingletonNode):
                tempvar_name = self.get_tempvar_name()
                tempvar = IDNode(tempvar_name)

                new_statements.append(AssignNode(tempvar, range._low))
                range._low = SingletonNode(tempvar)
            if range._up and not isinstance(range._up, SingletonNode):
                tempvar_name = self.get_tempvar_name()
                tempvar = IDNode(tempvar_name)

                new_statements.append(AssignNode(tempvar, range._up))
                range._up = SingletonNode(tempvar)
        return new_statements