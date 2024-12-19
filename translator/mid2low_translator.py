from utils.code_emitter import CodeEmitter
from utils.register import RegisterHandler
from utils.instruction_low import *

# Mid-Level to Low-Level Translation class
class Mid2LowTransLator:
    def __init__(self, mem_table):
        self.emitter = CodeEmitter()
        self.mem_table = mem_table
        self.reg_handler = RegisterHandler()

    def translate(self, code):
        for label, inst in code.code():
            if inst.is_mid_level():
                method_name = f"translate_{type(inst).__name__}"
                method = getattr(self, method_name, self.generic_translate)
                method(inst, label)
            else: self.emit(inst, label)
        return self.emitter.code()
    
    def generic_translate(self, inst, label):
        self.emit(UnhandledIns(f'Unhandled instruction type {type(inst).__name__}'), label)

    def translate_MidBranchEqZ(self, bez, label):
        r, regs = self.load_var(bez.var)
        self.emit(BranchEqZ(r, self.reg_handler.br, bez.label), label)
        self.unload_var(bez.var, r, regs)

    def translate_MidBranchNeqZ(self, bnz, label):
        r, regs = self.load_var(bnz.var)
        self.emit(BranchNeqZ(r, self.reg_handler.br, bnz.label), label)
        self.unload_var(bnz.var, r, regs)

    def translate_MidBranchControl(self, brc, label):
        r, regs = self.load_var(brc.var)
        self.emit(Branch(brc.label), label)
        self.unload_var(brc.var, r, regs)

    def translate_MidSwap(self, swap, label):
        r1, regs1 = self.load_var(swap.var1)
        r2, regs2 = self.load_var(swap.var2)
        self.emit(Swap(r1, r2), label)
        self.unload_var(swap.var2, r2, regs2)
        self.unload_var(swap.var1, r1, regs1)

    def translate_MidArithmetic(self, ari, label):
        r1, regs1 = self.load_var(ari.var1)
        r2, regs2 = self.load_var(ari.var2)
        self.emit(Arithmetic(ari.op, r1, r2), label)
        self.unload_var(ari.var2, r2, regs2)
        self.unload_var(ari.var1, r1, regs1)

    def translate_MidArithmeticB(self, arib, label):
        r1, regs1 = self.load_var(arib.var1)
        r2, regs2 = self.load_var(arib.var2)
        r3, regs3 = self.load_var(arib.var3)
        self.emit(ArithmeticB(arib.op, r1, r2, r3), label)
        self.unload_var(arib.var3, r3, regs3)
        self.unload_var(arib.var2, r2, regs2)
        self.unload_var(arib.var1, r1, regs1)

    def translate_MidXor(self, xor, label):
        r1, regs1 = self.load_var(xor.var1)
        r2 = self.load_imm(self.mem_table.offset(xor.var2.name))
        self.emit(FetchR(r1, r2), label)
        self.unload_imm(self.mem_table.offset(xor.var2.name), r2)
        self.unload_var(xor.var1, r1, regs1)

    def translate_MidAdd(self, add, label):
        r1, regs1 = self.load_var(add.var1)
        r2, regs2 = self.load_var(add.var2)
        self.emit(Add(r1, r2), label)
        self.unload_var(add.var2, r2, regs2)
        self.unload_var(add.var1, r1, regs1)

    def translate_MidSub(self, sub, label):
        r1, regs1 = self.load_var(sub.var1)
        r2, regs2 = self.load_var(sub.var2)
        self.emit(Sub(r1, r2), label)
        self.unload_var(sub.var2, r2, regs2)
        self.unload_var(sub.var1, r1, regs1)

    def translate_MidXori(self, xori, label):
        r1, regs1 = self.load_var(xori.var)
        self.emit(XORI(r1, xori.imm), label)
        self.unload_var(xori.var, r1, regs1)

    def translate_MidAddi(self, addi, label):
        r1, regs1 = self.load_var(addi.var)
        self.emit(AddI(r1, addi.imm), label)
        self.unload_var(addi.var, r1, regs1)

    def translate_MidSubi(self, subi, label):
        r1, regs1 = self.load_var(subi.var)
        self.emit(AddI(r1, subi.imm), label)
        self.unload_var(subi.var, r1, regs1)

    def translate_MidUnitary(self, uni, label):
        r, regs = self.load_var(uni.qreg)
        self.emit(Unitary(uni.gate, r), label)
        self.unload_var(uni.qreg, r, regs)

    def translate_MidUnitaryB(self, unib, label):
        r1, regs1 = self.load_var(unib.qreg1)
        r2, regs2 = self.load_var(unib.qreg2)
        self.emit(UnitaryB(unib.gate, r1, r2), label)
        self.unload_var(unib.qreg2, r2, regs2)
        self.unload_var(unib.qreg1, r1, regs1)

    def unload_var(self, var, r, regs):
        if var.is_number:
            ## Unload value
            self.unload_imm(int(var.name), r)
        elif var.index:
            ## Unload value into address
            r2 = regs.pop()
            self.emit(LoadR(r, r2))
            self.clear_reg(r)

            ## Unload address
            r1 = regs.pop()
            self.emit(Sub(r2, r1))
            self.emit(Load(r2, self.mem_table.offset(var.name)))
            self.clear_reg(r2)

            ## Unload index value
            self.unload_var(var.index, r1, regs)
        else:
            ## Unload value into address
            r1 = regs.pop()
            self.emit(LoadR(r, r1))
            self.clear_reg(r)

            ## Unload address
            self.emit(Load(r1, self.mem_table.offset(var.name)))
            self.clear_reg(r1)

    def load_var(self, var):
        regs = []
        if var.is_number:
            ## Load value
            r1 = self.load_imm(int(var.name))
            return r1, regs
        elif var.index:
            ## Load index value
            r1, regs_index = self.load_var(var.index)
            regs += regs_index

            ## Load address
            r2 = self.get_reg()
            self.emit(Load(r2, self.mem_table.offset(var.name)))
            self.emit(Add(r2, r1))

            ## Load value from address
            r3 = self.get_reg()
            self.emit(LoadR(r3, r2))

            regs.append(r1)
            regs.append(r2)
            return r3, regs
        else:
            ## Load address
            r1 = self.get_reg()
            self.emit(Load(r1, self.mem_table.offset(var.name)))

            ## Load value from address
            r2 = self.get_reg()
            self.emit(LoadR(r2, r1))

            regs.append(r1)
            return r2, regs
        
    def unload_imm(self, imm, r):
        self.emit(XORI(r, imm))
        self.clear_reg(r)
        
    def load_imm(self, imm):
        r1 = self.get_reg()
        self.emit(XORI(r1, imm))
        return r1

    def clear_reg(self, reg):
        self.reg_handler.clear_user_reg(reg)

    def get_reg(self):
        return self.reg_handler.get_user_reg()
        
    def emit(self, inst, label=None):
        self.emitter.emit(inst, label)