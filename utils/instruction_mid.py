

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
    
    def to_string(self):
        return f'Unhandled instruction type {type(self).__name__}'
    
# Mid-Level Instruction classes
class MidIns(Instruction):
    def __init__(self):
        pass

    def is_mid_level(self):
        return True
    
class MidStart(MidIns):
    def __init__(self):
        self.opcode = 16

    def to_string(self):
        return 'start'
    
class MidFinish(MidIns):
    def __init__(self):
        self.opcode = 17

    def to_string(self):
        return 'finish'
    
class Push(MidIns):
    def __init__(self, var):
        self.var = var

    def to_string(self):
        return f'push({self.var})'
    
class Pop(MidIns):
    def __init__(self, var):
        self.var = var

    def to_string(self):
        return f'pop({self.var})'

class MidBranchEqZ(MidIns):
    def __init__(self, var, label):
        self.var = var
        self.label = label

    def to_string(self):
        return f'bez({self.var}, {self.label})'

class MidBranchNeqZ(MidIns):
    def __init__(self, var, label):
        self.var = var
        self.label = label

    def to_string(self):
        return f'bnz({self.var}, {self.label})'

class MidBranch(MidIns):
    def __init__(self, label):
        self.label = label

    def to_string(self):
        return f'bra({self.label})'
    
class MidBranchControl(MidIns):
    def __init__(self, var, label):
        self.var = var
        self.label = label

    def to_string(self):
        return f'brc({self.var}, {self.label})'
    
class MidUnitary(MidIns):
    def __init__(self, gate, qreg, offset):
        self.opcode = 18
        self.gate = gate
        self.qreg = qreg
        self.offset = offset

    def to_string(self):
        return f'uni({self.gate}, {self.qreg}[{self.offset}])'
    
class MidUnitaryB(MidIns):
    def __init__(self, gate, qreg1, offset1, qreg2, offset2):
        self.opcode = 19
        self.gate = gate
        self.qreg1 = qreg1
        self.offset1 = offset1
        self.qreg2 = qreg2
        self.offset2 = offset2

    def to_string(self):
        return f'unib({self.gate}, {self.qreg1}[{self.offset1}], {self.qreg2}[{self.offset2}])'
    
class MidAdd(MidIns):
    def __init__(self, var, incr):
        self.var = var
        self.incr = incr

    def to_string(self):
        return f'add({self.var}, {self.incr})'