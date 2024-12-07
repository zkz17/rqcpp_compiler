# High-Level Transformer class
class RQCTransformer:
    def __init__(self):
        self.proc_prefix = '#'
        self.proc_counter = 0
        self.var_prefix = '&'
        self.var_counter = 0
        self.available_tempvar_name = []

    def transform(self, ast):
        self.quantum_branch_rewrite(ast)
        self.local_statement_rewrite(ast)
        self.expr_extract_rewrite(ast)
        self.index_extract_rewrite(ast)
        self.expr_split_rewrite(ast)

    def expr_split_rewrite(self, ast):
        from rewriter.exprsplit_rewriter import ExprSplitRewriter
        rewriter = ExprSplitRewriter(self.get_tempvar_name, self.free_tempvar_name)
        rewriter.rewrite(ast)

    def index_extract_rewrite(self, ast):
        from rewriter.indexextract_rewriter import IndexExtractRewriter
        rewriter = IndexExtractRewriter(self.get_tempvar_name, self.free_tempvar_name)
        rewriter.rewrite(ast)

    def expr_extract_rewrite(self, ast):
        from rewriter.exprextract_rewriter import ExprExtractRewriter
        rewriter = ExprExtractRewriter(self.get_tempvar_name, self.free_tempvar_name)
        rewriter.rewrite(ast)

    def quantum_branch_rewrite(self, ast):
        from rewriter.qbranch_rewriter import QBranchRewriter
        rewriter = QBranchRewriter(self.get_tempproc_name, self.proc_prefix + '_')
        rewriter.rewrite(ast)

    def local_statement_rewrite(self, ast):
        from rewriter.localstmt_rewriter import LocalStmtRewriter
        rewriter = LocalStmtRewriter(self.get_tempvar_name, self.free_tempvar_name)
        rewriter.rewrite(ast)

    def get_tempvar_name(self):
        if len(self.available_tempvar_name):
            return self.available_tempvar_name.pop()
        name = self.var_prefix + str(self.var_counter)
        self.var_counter += 1
        return name
    
    def free_tempvar_name(self, name):
        if isinstance(name, list):
            self.available_tempvar_name += name
        self.available_tempvar_name.append(name)
    
    def get_tempproc_name(self):
        name = self.proc_prefix + str(self.proc_counter)
        self.proc_counter += 1
        return name