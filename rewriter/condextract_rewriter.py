from rewriter.rewriter import Rewriter
from utils.astnode import *

# Expression Extraction Rewrite class
class CondExtractRewriter(Rewriter):
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
    
    def visit_IfStmtNode(self, ifstmt):
        #used_tempvar_name = []
        new_branches = []

        for cond, body, _ in ifstmt._branches:
            if cond and not isinstance(cond, SingletonNode):
                tempvar_name = self.get_tempvar_name()
                #used_tempvar_name.append(tempvar_name)

                tempvar = IDNode(tempvar_name)
                self.visit(body)
                new_branches.append((SingletonNode(tempvar), body, BlockNode([AssignNode(tempvar, cond)])))
            else: 
                self.visit(body)
                new_branches.append((cond, body, None))

        ifstmt._branches = new_branches
        #self.free_tempvar_name(used_tempvar_name)
        return [ifstmt]
    
    def visit_WhileStmtNode(self, whilestmt):
        #used_tempvar_name = []

        if whilestmt._cond and not isinstance(whilestmt._cond, SingletonNode):
            tempvar_name = self.get_tempvar_name()
            #used_tempvar_name.append(tempvar_name)

            tempvar = IDNode(tempvar_name)
            whilestmt._pre = BlockNode([AssignNode(tempvar, whilestmt._cond)])
            whilestmt._cond = SingletonNode(tempvar)

        self.visit(whilestmt._body)
        #self.free_tempvar_name(used_tempvar_name)
        return [whilestmt]
    
    def visit_QifStmtNode(self, qifstmt):
        #used_tempvar_name = []
        new_statements = []

        for _, call in qifstmt._branches:
            if not isinstance(call, CallNode): raise Exception(f'Unexpected Qif branch type {type(call).__name__}')

            new_params = []
            for param in call._params:
                if not isinstance(param, SingletonNode):
                    tempvar_name = self.get_tempvar_name()
                    #used_tempvar_name.append(tempvar_name)

                    tempvar = IDNode(tempvar_name)
                    new_statements.append(AssignNode(tempvar, param))
                    new_params.append(SingletonNode(tempvar))
                else:
                    new_params.append(param)
            call._params = new_params

        new_statements.append(qifstmt)
        #self.free_tempvar_name(used_tempvar_name)
        return new_statements
    
    def visit_CallNode(self, call):
        #used_tempvar_name = []
        new_statements = []
        new_params = []

        for param in call._params:
            if not isinstance(param, SingletonNode):
                tempvar_name = self.get_tempvar_name()
                #used_tempvar_name.append(tempvar_name)

                tempvar = IDNode(tempvar_name)
                new_statements.append(AssignNode(tempvar, param))
                new_params.append(SingletonNode(tempvar))
            else:
                new_params.append(param)
        call._params = new_params
        new_statements.append(call)
        #self.free_tempvar_name(used_tempvar_name)
        return new_statements