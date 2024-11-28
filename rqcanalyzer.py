# Semantic Analyzer class
class RQCAnalyzer:
    def __init__(self, ast):
        self.ast = ast

    def analyze(self):
        self.scope_analyze()

    def scope_analyze(self):
        from analyzer.scope_analyzer import ScopeAnalyzer
        analyzer = ScopeAnalyzer()
        analyzer.analyze(self.ast)