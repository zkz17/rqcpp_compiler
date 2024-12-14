# Code Generator class
class RQCGenerator:
    def __init__(self):
        pass

    def generate(self, ast):
        mid_code = self.high2midTrans(ast)
        low_code = self.mid2lowTrans(mid_code)
        return low_code

    def high2midTrans(self, ast):
        from translator.high2mid_translator import High2MidTransLator
        translator = High2MidTransLator()
        return translator.translate(ast)

    def mid2lowTrans(self, code):
        from translator.mid2low_translator import Mid2LowTransLator
        translator = Mid2LowTransLator()
        return translator.translate(code)