from utils.astnode import *

# Quantum Branch Rewrite class
class QBranchRewriter:
    def __init__(self):
        self.new_proc_prefix = '#'
        self.new_proc_counter = 1
        self.zero_proc = False

    def rewrite(self, ast):
        ast._procs += self.visit(ast)
        if self.zero_proc:
            ast._procs.append(ProcNode(IDNode(self.new_proc_prefix + '0'), [], BlockNode([SkipStmtNode()])))

    def visit(self, node):
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name, self.generic_visit)
        return method(node)
    
    def generic_visit(self, node):
        ## Default method for unhandled nodes
        new_procs = []
        if not node: return new_procs
        for child in node.__dict__.values():
            if isinstance(child, list):
                for item in child:
                    if isinstance(item, ASTNode): 
                        new_procs += self.visit(item)
                    elif isinstance(item, tuple): 
                        for element in item:
                            new_procs += self.visit(element)
            elif isinstance(child, ASTNode): 
                new_procs += self.visit(child)
        return new_procs
            
    def visit_QifStmtNode(self, qifstmt):
        new_procs = []
        new_branches = []
        for _, body in qifstmt._branches:
            new_procs += self.visit(body)
            new_proc, new_call = self.construct_proc(body)
            new_branches.append((_, new_call))
            if new_proc and new_proc._id._id != self.new_proc_prefix + '0': new_procs.append(new_proc)

        qifstmt._branches = new_branches
        return new_procs
    
    def construct_proc(self, block): 
        proc_name = self.new_proc_prefix
        if len(block._statements) == 1 and isinstance(block._statements[0], SkipStmtNode):
            proc_name += '0'
            self.zero_proc = True
            return ProcNode(IDNode(proc_name), [], block), CallNode(IDNode(proc_name), [])
        elif len(block._statements) == 1 and isinstance(block._statements[0], CallNode):
            ## No need to rewrite. 
            return None, block._statements[0]
        else: 
            proc_name += str(self.new_proc_counter)
            self.new_proc_counter += 1

            id = IDNode(proc_name)
            proc_params, call_params = [], []
            for _, symbol in block._symbols.free_vars():
                proc_params.append(IDNode(symbol.name))
                call_params.append(symbol.value)
            return ProcNode(id, proc_params, block), CallNode(id, call_params)