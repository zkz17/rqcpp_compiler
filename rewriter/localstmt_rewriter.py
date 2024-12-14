from rewriter.rewriter import Rewriter
from utils.astnode import *

# Local Statement Rewrite class
class LocalStmtRewriter(Rewriter):
    def __init__(self, get_tempvar_name, free_tempvar_name):
        super().__init__(get_tempvar_name, free_tempvar_name)

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
    
    def visit_LocalStmtNode(self, localstmt):
        new_statements = []
        restore_statements = []
        for assign in localstmt._localvars:
            if localstmt._body._symbols.parent.resolve(assign._left.name()):
                tempvar = IDNode(self.get_tempvar_name())
                new_statements.append(AssignNode(tempvar, SingletonNode(assign._left)))
                restore_statements.append(AssignNode(assign._left, SingletonNode(tempvar)))
            new_statements.append(assign)
            
        self.visit(localstmt._body)
        new_statements += localstmt._body._statements
        new_statements += restore_statements
        return new_statements