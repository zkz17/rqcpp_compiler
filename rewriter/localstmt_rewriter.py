from rewriter.rewriter import Rewriter
from utils.astnode import *

# Local Statement Rewrite class
class LocalStmtRewriter(Rewriter):
    def __init__(self, prefix='%'):
        super().__init__(prefix)

    def rewrite(self, ast):
        self.visit(ast)
    
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
        for assign in localstmt._localvars:
            temp_var = IDNode(self.get_tempvar_name)
            ## TODO
        return statements