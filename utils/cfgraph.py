
class BasicBlock:
    def __init__(self, start=1):
        self.start = start
        self.end = None
        self.instructions = []
        self.pred = []
        self.succ = []

    def append(self, inst):
        self.instructions.append(inst)

    def add_pred(self, pred):
        self.pred.append(pred)

    def add_succ(self, succ):
        self.succ.append(succ)

class CFGraph:
    def __init__(self, code):
        self.start_to_block = {}
        self.label_to_line = {}
        self.build(code)

    def build(self, code):
        current_block = BasicBlock(1)
        for line, (label, inst) in enumerate(code.code(), start=1):
            if label: self.label_to_line[label.to_string()] = line
            if not inst.is_mid_level(): # SwapBr, Negation, Start, Finish
                current_block.append(inst)
                if inst.opcode == 13: # SwapBr
                    new_block = BasicBlock(line)
                    new_block.append(inst)

                    current_block.end = line
                    self.start_to_block[current_block.start] = current_block
                    current_block = new_block
            elif inst.is_conditional_branch():
                pass
            elif inst.is_branch():
                pass
