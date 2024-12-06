from rewriter.rewriter import Rewriter
from utils.astnode import *

# Expression Split Rewrite class
class ExprSplitRewriter(Rewriter):
    def __init__(self, prefix='&'):
        super().__init__(prefix)

    def rewrite(self, ast):
        self.visit(ast)

    def visit_BlockNode(self, block):
        new_statements = []
        for stmt in block._statements:
            stmt_list = self.visit(stmt)
            if len(stmt_list): new_statements += stmt_list
            else: new_statements.append(stmt)
        
        block._statements = new_statements
        return []
    
    def visit_AssignNode(self, assign):
        new_statements, _ = self.split_cvalue(assign._right)
        if len(new_statements): 
            self.free_tempvar_name(new_statements[-1]._left._id)
            new_statements[-1]._left = assign._left
        return new_statements
    
    def split_cvalue(self, cval):
        new_statements = []
        if isinstance(cval, SingletonNode): return [], cval
        elif isinstance(cval, UnaOpNode):
            stmt_list, right = self.split_cvalue(cval._right)
            new_statements += stmt_list
            
            tempvar_name = self.get_tempvar_name()
            tempvar = IDNode(tempvar_name)
            new_val = UnaOpNode(cval._op, right)
            new_statements.append(AssignNode(tempvar, new_val))
            return new_statements, SingletonNode(tempvar)
        elif isinstance(cval, BinOpNode):
            stmt_list, left = self.split_cvalue(cval._left)
            new_statements += stmt_list
            stmt_list, right = self.split_cvalue(cval._right)
            new_statements += stmt_list

            tempvar_name = self.get_tempvar_name()
            tempvar = IDNode(tempvar_name)
            new_val = BinOpNode(left, cval._op, right)
            new_statements.append(AssignNode(tempvar, new_val))
            return new_statements, SingletonNode(tempvar)
        elif isinstance(cval, ListNode):
            ## TODO
            return [], cval
        else:
            raise Exception(f'Undefined classical value type {type(cval).__name__}')