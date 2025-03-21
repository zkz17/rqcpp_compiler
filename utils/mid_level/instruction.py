from utils.instruction import Instruction

# Mid-Level Instruction classes
class MidIns(Instruction):
    def __init__(self):
        pass

    def is_mid_level(self):
        return True
    
class Push(MidIns):
    def __init__(self, var):
        self.var = var

    def to_string(self):
        return f'push({self.var.to_string()})'
    
class Pop(MidIns):
    def __init__(self, var):
        self.var = var

    def to_string(self):
        return f'pop({self.var.to_string()})'

class MidBranchEqZ(MidIns):
    def __init__(self, var, label, ishead=False):
        self.var = var
        self.label = label
        self.ishead = ishead

    def to_string(self):
        return f'bez({self.var.to_string()}, {self.label.to_string()})'
    
    def is_branch(self):
        return True
    
    def is_conditional_branch(self):
        return True
    
    def is_head(self):
        return self.ishead

class MidBranchNeqZ(MidIns):
    def __init__(self, var, label, ishead=False):
        self.var = var
        self.label = label
        self.ishead = ishead

    def to_string(self):
        return f'bnz({self.var.to_string()}, {self.label.to_string()})'
    
    def is_branch(self):
        return True
    
    def is_conditional_branch(self):
        return True
    
    def is_head(self):
        return self.ishead

class MidBranch(MidIns):
    def __init__(self, label, ishead=False):
        self.label = label
        self.ishead = ishead

    def to_string(self):
        return f'bra({self.label.to_string()})'
    
    def is_branch(self):
        return True
    
    def is_conditional_branch(self):
        return False
    
    def is_head(self):
        return self.ishead
    
class MidBranchControl(MidIns):
    def __init__(self, var, label, ishead=False):
        self.var = var
        self.label = label
        self.ishead = ishead

    def to_string(self):
        return f'brc({self.var.to_string()}, {self.label.to_string()})'
    
    def is_branch(self):
        return True
    
    def is_conditional_branch(self):
        return False
    
    def is_head(self):
        return self.ishead
    
class MidUnitary(MidIns):
    def __init__(self, gate, qreg):
        self.opcode = 18
        self.gate = gate
        self.qreg = qreg

    def to_string(self):
        return f'uni({self.gate}, {self.qreg.to_string()})'
    
class MidUnitaryB(MidIns):
    def __init__(self, gate, qreg1, qreg2):
        self.opcode = 19
        self.gate = gate
        self.qreg1 = qreg1
        self.qreg2 = qreg2

    def to_string(self):
        return f'unib({self.gate}, {self.qreg1.to_string()}, {self.qreg2.to_string()})'
    
class MidSwap(MidIns):
    def __init__(self, var1, var2):
        self.var1 = var1
        self.var2 = var2

    def to_string(self):
        return f'swap({self.var1.to_string()}, {self.var2.to_string()})'
    
class MidAdd(MidIns):
    def __init__(self, var1, var2):
        self.var1 = var1
        self.var2 = var2

    def to_string(self):
        return f'add({self.var1.to_string()}, {self.var2.to_string()})'
    
class MidSub(MidIns):
    def __init__(self, var1, var2):
        self.var1 = var1
        self.var2 = var2

    def to_string(self):
        return f'sub({self.var1.to_string()}, {self.var2.to_string()})'
    
class MidXor(MidIns):
    def __init__(self, var1, var2):
        self.var1 = var1
        self.var2 = var2

    def to_string(self):
        return f'xor({self.var1.to_string()}, {self.var2.to_string()})'
    
class MidAddi(MidIns):
    def __init__(self, var, imm):
        self.var = var
        self.imm = imm

    def to_string(self):
        return f'addi({self.var.to_string()}, {self.imm.to_string()})'
    
class MidSubi(MidIns):
    def __init__(self, var, imm):
        self.var = var
        self.imm = imm

    def to_string(self):
        return f'sub({self.var.to_string()}, {self.imm.to_string()})'
    
class MidXori(MidIns):
    def __init__(self, var, imm):
        self.var = var
        self.imm = imm

    def to_string(self):
        return f'xori({self.var.to_string()}, {self.imm.to_string()})'
    
class MidQif(MidIns):
    def __init__(self, reg):
        self.reg = reg

    def to_string(self):
        return f'qif({self.reg.to_string()})'
    
class MidFiq(MidIns):
    def __init__(self, reg):
        self.reg = reg

    def to_string(self):
        return f'fiq({self.reg.to_string()})'
    
class MidArithmetic(MidIns):
    def __init__(self, op, var1, var2):
        self.op = op
        self.var1 = var1
        self.var2 = var2

    def to_string(self):
        return f'ari({self.op}, {self.var1.to_string()}, {self.var2.to_string()})'
    
class MidArithmeticB(MidIns):
    def __init__(self, op, var1, var2, var3):
        self.op = op
        self.var1 = var1
        self.var2 = var2
        self.var3 = var3

    def to_string(self):
        return f'arib({self.op}, {self.var1.to_string()}, {self.var2.to_string()}, {self.var3.to_string()})'