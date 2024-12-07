from rewriter.rewriter import Rewriter
from utils.astnode import *

# Quantum Branch Rewrite class
class QBranchRewriter(Rewriter):
    def __init__(self, get_tempvar_name, default_proc_name='#_'):
        super().__init__(get_tempvar_name, None)
        self.default_proc_name = default_proc_name
        self.default_proc = False

    def rewrite(self, ast):
        ast._procs += self.visit(ast)
        if self.default_proc:
            ast._procs.append(ProcNode(IDNode(self.default_proc_name), [], BlockNode([SkipStmtNode()])))
            
    def visit_QifStmtNode(self, qifstmt):
        new_procs = []
        new_branches = []
        for _, body in qifstmt._branches:
            new_procs += self.visit(body)
            new_proc, new_call = self.construct_proc(body)
            new_branches.append((_, new_call))
            if new_proc and new_proc._id._id != self.default_proc_name: new_procs.append(new_proc)

        qifstmt._branches = new_branches
        return new_procs
    
    def construct_proc(self, block): 
        if len(block._statements) == 1 and isinstance(block._statements[0], SkipStmtNode):
            self.default_proc = True
            return ProcNode(IDNode(self.default_proc_name), [], block), CallNode(IDNode(self.default_proc_name), [])
        elif len(block._statements) == 1 and isinstance(block._statements[0], CallNode):
            ## No need to rewrite. 
            return None, block._statements[0]
        else: 
            proc_name = self.get_tempvar_name()

            id = IDNode(proc_name)
            proc_params, call_params = [], []
            for _, symbol in block._symbols.free_vars().items():
                var = IDNode(symbol.name)
                proc_params.append(var)
                call_params.append(SingletonNode(var))
            return ProcNode(id, proc_params, block), CallNode(id, call_params)