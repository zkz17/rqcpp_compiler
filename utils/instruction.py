# QINS Instruction base class
class Instruction:
    def __init__(self):
        pass

    def is_immediate_type(self):
        return False
    
    def is_register_type(self):
        return False
    
    def is_other_type(self):
        return False
    
    def is_mid_level(self):
        return False
    
    def is_unhandled(self):
        return False
    
    def is_branch(self):
        return False
    
    def is_conditional_branch(self):
        return False
    
    def is_head(self):
        return False
    
    def to_string(self):
        return f'Unhandled output type {type(self).__name__}'

class UnhandledIns(Instruction):
    def __init__(self, name):
        self.name = name
    
    def is_unhandled(self):
        return True

    def to_string(self):
        return self.name
    
class Iins(Instruction):
    def __init__(self, reg, imm):
        self.reg = reg
        self.imm = imm

    def is_immediate_type(self):
        return True
    
    def to_string(self):
        return f'{self.op}({self.reg.to_string() + ', ' if self.reg else ''}{self.imm.to_string()})'
    
class Rins(Instruction):
    def __init__(self, reg1, reg2):
        self.reg1 = reg1
        self.reg2 = reg2

    def is_register_type(self):
        return True
    
    def to_string(self):
        return f'{self.op}({self.reg1.to_string()}{', ' + self.reg2.to_string() if self.reg2 else ''})'
    
class Oins(Instruction):
    def __init__(self, para, reg1, reg2, reg3):
        self.para = para
        self.reg1 = reg1
        self.reg2 = reg2
        self.reg3 = reg3

    def is_other_type(self):
        return True
    
    def to_string(self):
        return f'{self.op}({self.para}, {self.reg1.to_string()}{', ' + self.reg2.to_string() if self.reg2 else ''}{', ' + self.reg3.to_string() if self.reg3 else ''})'
    
class Load(Iins):
    def __init__(self, r, imm):
        self.op = 'ld'
        self.opcode = 0
        super().__init__(r, imm)
    
class XORI(Iins):
    def __init__(self, r, imm):
        self.op = 'xori'
        self.opcode = 1
        super().__init__(r, imm)
    
class AddI(Iins):
    def __init__(self, r, imm):
        self.op = 'addi'
        self.opcode = 2
        super().__init__(r, imm)
    
class SubI(Iins):
    def __init__(self, r, imm):
        self.op = 'subi'
        self.opcode = 3
        super().__init__(r, imm)
    
class Branch(Iins):
    def __init__(self, imm):
        self.opcode = 4
        self.imm = imm

    def to_string(self):
        return f'bra({self.imm.to_string()})'
    
class BranchEqZ(Iins):
    def __init__(self, r, br, imm):
        self.opcode = 5
        self.r = r
        self.br = br
        self.imm = imm

    def to_string(self):
        return f'bez({self.r.to_string()}, {self.imm.to_string()})'
    
class BranchNeqZ(Iins):
    def __init__(self, r, br, imm):
        self.opcode = 6
        self.r = r
        self.br = br
        self.imm = imm

    def to_string(self):
        return f'bnz({self.r.to_string()}, {self.imm.to_string()})'
    
class LoadR(Rins):
    def __init__(self, r1, r2):
        self.op = 'ldr'
        self.opcode = 7
        super().__init__(r1, r2)
    
class FetchR(Rins):
    def __init__(self, r1, r2):
        self.op = 'fetr'
        self.opcode = 8
        super().__init__(r1, r2)
    
class Swap(Rins):
    def __init__(self, r1, r2):
        self.op = 'swap'
        self.opcode = 9
        super().__init__(r1, r2)
    
class Add(Rins):
    def __init__(self, r1, r2):
        self.op = 'add'
        self.opcode = 10
        super().__init__(r1, r2)
    
class Sub(Rins):
    def __init__(self, r1, r2):
        self.op = 'sub'
        self.opcode = 11
        super().__init__(r1, r2)
    
class Negation(Rins):
    def __init__(self, reg):
        self.op = 'neg'
        self.opcode = 12
        self.reg= reg
        super().__init__(reg, None)
    
class SwapBr(Rins):
    def __init__(self, reg):
        self.op = 'swbr'
        self.opcode = 13
        super().__init__(reg, None)
    
class Qif(Rins):
    def __init__(self, r1):
        self.op = 'qif'
        self.opcode = 14
        super().__init__(r1, None)
    
class Fiq(Rins):
    def __init__(self, r1):
        self.op = 'fiq'
        self.opcode = 15
        super().__init__(r1, None)
    
class Start(Rins):
    def __init__(self):
        self.opcode = 16
        super().__init__(None, None)

    def to_string(self):
        return 'start'
    
class Finish(Rins):
    def __init__(self):
        self.opcode = 17
        super().__init__(None, None)

    def to_string(self):
        return 'finish'
    
class Unitary(Oins):
    def __init__(self, G, r1):
        self.op = 'uni'
        self.opcode = 18
        super().__init__(G, r1, None, None)
    
class UnitaryB(Oins):
    def __init__(self, G, r1, r2):
        self.op = 'unib'
        self.opcode = 19
        super().__init__(G, r1, r2, None)
    
class Arithmetic(Oins):
    def __init__(self, operator, r1, r2):
        self.op = 'ari'
        self.opcode = 20
        super().__init__(operator, r1, r2, None)
    
class ArithmeticB(Oins):
    def __init__(self, operator, r1, r2, r3):
        self.op = 'arib'
        self.opcode = 21
        super().__init__(operator, r1, r2, r3)
