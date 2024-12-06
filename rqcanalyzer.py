# Semantic Analyzer class
class RQCAnalyzer:
    def __init__(self):
        pass

    def analyze(self, ast):
        self.scope_analyze(ast)
        self.typecheck_analyze(ast)

    def scope_analyze(self, ast):
        from analyzer.scope_analyzer import ScopeAnalyzer
        analyzer = ScopeAnalyzer()
        analyzer.analyze(ast)

    def typecheck_analyze(self, ast):
        from analyzer.typecheck_analyzer import TypeCheckAnalyzer
        analyzer = TypeCheckAnalyzer()
        analyzer.analyze(ast)