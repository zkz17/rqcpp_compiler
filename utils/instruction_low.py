from utils.instruction_mid import Instruction
    
class Iins(Instruction):
    def __init__(self, reg, imm):
        self.reg = reg
        self.imm = imm

    def is_immediate_type(self):
        return True
    
class Rins(Instruction):
    def __init__(self, reg1, reg2):
        self.reg1 = reg1
        self.reg2 = reg2

    def is_register_type(self):
        return True
    
class Oins(Instruction):
    def __init__(self, para, reg1, reg2, reg3):
        self.para = para
        self.reg1 = reg1
        self.reg2 = reg2
        self.reg3 = reg3

    def is_other_type(self):
        return True
    
class Load(Iins):
    def __init__(self, r, imm):
        self.opcode = 0
        self.r = r
        self.imm = imm
    
class XORI(Iins):
    def __init__(self, r, imm):
        self.opcode = 1
        self.r = r
        self.imm = imm
    
class AddI(Iins):
    def __init__(self, r, imm):
        self.opcode = 2
        self.r = r
        self.imm = imm
    
class SubI(Iins):
    def __init__(self, r, imm):
        self.opcode = 3
        self.r = r
        self.imm = imm
    
class Branch(Iins):
    def __init__(self, imm):
        self.opcode = 4
        self.imm = imm

    def to_string(self):
        return f'bra({self.imm})'
    
class BranchEqZ(Iins):
    def __init__(self, r, br, imm):
        self.opcode = 5
        self.r = r
        self.br = br
        self.imm = imm
    
class BranchNeqZ(Iins):
    def __init__(self, r, br, imm):
        self.opcode = 6
        self.r = r
        self.br = br
        self.imm = imm
    
class LoadR(Rins):
    def __init__(self, r1, r2, mem):
        self.opcode = 7
        self.r1 = r1
        self.r2 = r2
        self.mem = mem
    
class FetchR(Rins):
    def __init__(self, r1, r2, mem):
        self.opcode = 8
        self.r1 = r1
        self.r2 = r2
        self.mem = mem
    
class Swap(Rins):
    def __init__(self, r1, r2):
        self.opcode = 9
        self.r1 = r1
        self.r2 = r2
    
class Add(Rins):
    def __init__(self, r1, r2):
        self.opcode = 10
        self.r1 = r1
        self.r2 = r2
    
class Sub(Rins):
    def __init__(self, r1, r2):
        self.opcode = 11
        self.r1 = r1
        self.r2 = r2
    
class Negation(Rins):
    def __init__(self, reg):
        self.opcode = 12
        self.reg= reg

    def to_string(self):
        return f'neg({self.reg})'
    
class SwapBr(Rins):
    def __init__(self, reg):
        self.opcode = 13
        self.reg = reg

    def to_string(self):
        return f'swbr({self.reg})'
    
class Qif(Rins):
    def __init__(self, r1):
        self.opcode = 14
        self.r1 = r1
    
class Fiq(Rins):
    def __init__(self, r1):
        self.opcode = 15
        self.r1 = r1
    
class Start(Rins):
    def __init__(self):
        self.opcode = 16

    def to_string(self):
        return 'start'
    
class Finish(Rins):
    def __init__(self):
        self.opcode = 17

    def to_string(self):
        return 'finish'
    
class Unitary(Oins):
    def __init__(self, G, r1, r2):
        self.opcode = 18
        self.G = G
        self.r1 = r1
    
class UnitaryB(Oins):
    def __init__(self, G, r1, r2):
        self.opcode = 19
        self.G = G
        self.r1 = r1
        self.r2 = r2
    
class Arithmetic(Oins):
    def __init__(self, op, r1, r2):
        self.opcode = 20
        self.op = op
        self.r1 = r1
        self.r2 = r2
    
class ArithmeticB(Oins):
    def __init__(self, op, r1, r2, r3):
        self.opcode = 21
        self.op = op
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
