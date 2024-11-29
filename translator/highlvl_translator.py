# High-Level Transformation class
class HighLvlTransformer:
    def __init__(self):
        pass

    def transform(self, ast):
        self.quantum_branch_rewrite(ast)
        #self.local_statement_rewrite(ast)

    def quantum_branch_rewrite(self, ast):
        from translator.qbranch_rewriter import QBranchRewriter
        rewriter = QBranchRewriter()
        rewriter.rewrite(ast)

    def local_statement_rewrite(self, ast):
        from translator.localstmt_rewriter import LocalStmtRewriter
        rewriter = LocalStmtRewriter()
        rewriter.rewrite(ast)