from utils.memorytable import MemoryTable
from utils.mid_level.variable import Variable, Immediate
from utils.mid_level.label import Label
from rqcoptimizer import RQCOptimizer

# Code Generator class
class RQCGenerator:
    def __init__(self):
        self.optimizer = RQCOptimizer()

    def generate(self, ast):
        ## High-level to mid-level translation
        mid_code = self.high2mid_trans(ast)

        ## Mid-level optimization
        mid_code = self.optimizer.midlevel_optimize(mid_code)

        ## Memory allocation
        mem_table = self.mem_allocate(ast, mid_code)

        ## Mid-level to Low-level translation
        low_code = self.mid2low_trans(mid_code, mem_table)

        ## Low-level optimization
        low_code = self.optimizer.lowlevel_optimize(low_code)

        ## Label to immediate translation
        self.link(low_code)

        return low_code, mid_code, mem_table

    def high2mid_trans(self, ast):
        from translator.high2mid_translator import High2MidTransLator
        translator = High2MidTransLator()
        return translator.translate(ast)

    def mid2low_trans(self, code, mem_table):
        from translator.mid2low_translator import Mid2LowTransLator
        translator = Mid2LowTransLator(mem_table)
        return translator.translate(code)
    
    def mem_allocate(self, ast, mid_code):
        mem_table = MemoryTable()
        mem_table.alloc_arrays(ast._symbols)
        for _, inst in mid_code.code():
            for child in inst.__dict__.values():
                if isinstance(child, Variable) and not child.is_immediate():
                    mem_table.allocate(child.name)
        return mem_table
    
    def link(self, low_code):
        label2line = {}
        i = 0
        for label, _ in low_code.list:
            if label: label2line[label.to_string()] = i
            if not _.is_unhandled(): i += 1
        i = 0
        for _, inst in low_code.list:
            for item in inst.__dict__.values():
                if isinstance(item, Label):
                    inst.imm = Immediate(label2line[item.to_string()] - i)
            if not inst.is_unhandled(): i += 1