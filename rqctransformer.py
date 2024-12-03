# High-Level Transformer class
class RQCTransformer:
    def __init__(self):
        pass

    def transform(self, ast):
        self.quantum_branch_rewrite(ast)
        #self.local_statement_rewrite(ast)
        self.expr_extract_rewrite(ast)

    def expr_extract_rewrite(self, ast):
        from rewriter.exprextract_rewriter import ExprExtractRewriter
        rewriter = ExprExtractRewriter()
        rewriter.rewrite(ast)

    def quantum_branch_rewrite(self, ast):
        from rewriter.qbranch_rewriter import QBranchRewriter
        rewriter = QBranchRewriter()
        rewriter.rewrite(ast)

    def local_statement_rewrite(self, ast):
        from rewriter.localstmt_rewriter import LocalStmtRewriter
        rewriter = LocalStmtRewriter()
        rewriter.rewrite(ast)