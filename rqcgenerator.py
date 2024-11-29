# Code Generator class
class RQCGenerator:
    def __init__(self):
        pass

    def generate(self, ast):
        self.highLvlTrans(ast)
        self.high2midTrans(ast)
        self.mid2lowTrans(ast)

    def highLvlTrans(self, ast):
        from translator.highlvl_translator import HighLvlTransformer
        transformer = HighLvlTransformer()
        transformer.transform(ast)

    def high2midTrans(self, ast):
        from translator.high2mid_translator import High2MidTransLator
        translator = High2MidTransLator()
        translator.translate(ast)

    def mid2lowTrans(self, ast):
        from translator.mid2low_translator import Mid2LowTransLator
        translator = Mid2LowTransLator()
        translator.translate(ast)