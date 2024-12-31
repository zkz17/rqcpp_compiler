from utils.astnode import *
from utils.mid_level.instruction import *
from utils.mid_level.variable import *
from utils.instruction import SwapBr, Negation, Start, Finish
from utils.register import SystemReg
from utils.code_emitter import CodeEmitter
from basic_gates import basic_gates

# High-Level to Mid-Level Translation class
class High2MidTransLator:
    def __init__(self):
        self.emitter = CodeEmitter()
        self.ro = SystemReg('ro')

    def translate(self, ast):
        self.visit(ast)
        return self.emitter.code()

    def visit(self, node):
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name, self.generic_visit)
        method(node)

    def generic_visit(self, node):
        ## Default method for unhandled nodes
        if not isinstance(node, ASTNode): return
        for child in node.__dict__.values():
            if isinstance(child, list):
                for item in child:
                    if isinstance(item, ASTNode): 
                        self.visit(item)
                    elif isinstance(item, tuple): 
                        for element in item:
                            self.visit(element)
            elif isinstance(child, ASTNode): 
                self.visit(child)

    def uncomp(self, node):
        method_name = f"uncomp_{type(node).__name__}"
        method = getattr(self, method_name, self.generic_uncomp)
        method(node)

    def generic_uncomp(self, node):
        ## Default method for unhandled nodes
        if not isinstance(node, ASTNode): return
        for child in node.__dict__.values():
            if isinstance(child, list):
                for item in child:
                    if isinstance(item, ASTNode): 
                        self.uncomp(item)
                    elif isinstance(item, tuple): 
                        for element in item:
                            self.uncomp(element)
            elif isinstance(child, ASTNode): 
                self.uncomp(child)

    def uncomp_BlockNode(self, block):
        for stmt in reversed(block._statements):
            self.uncomp(stmt)

    def uncomp_IfStmtNode(self, ifstmt):
        branch_back = []
        for cond, body, pre in ifstmt._branches:
            if cond:
                self.visit(pre)
                label_cond_forward, label_cond_backward = self.get_label_pair()
                self.emit(MidBranchEqZ(self.get_var(cond.name(), cond.index()), label_cond_backward), label_cond_forward)

                self.uncomp(body)

                label_skip_forward, label_skip_backward = self.get_label_pair()
                self.emit(MidBranchControl(self.get_var(cond.name(), cond.index()), label_skip_backward), label_skip_forward)
                branch_back.append((MidBranchControl(self.get_var(cond.name(), cond.index()), label_skip_forward), label_skip_backward, pre))

                self.emit(MidBranchControl(self.get_var(cond.name(), cond.index()), label_cond_forward), label_cond_backward)
            else:
                self.uncomp(body)
        
        for inst, label, pre in reversed(branch_back):
            self.emit(inst, label)
            self.uncomp(pre)

    def uncomp_WhileStmtNode(self, whilestmt):
        label_counter_forward, label_counter_backward = self.get_label_pair()
        counter_var = self.get_var(self.emitter.get_tempvar_name())
        self.emit(Pop(counter_var))
        
        label_cond_forward, label_cond_backward = self.get_label_pair()
        self.emit(MidBranchNeqZ(self.get_var(whilestmt._cond.name(), whilestmt._cond.index()), label_cond_backward), label_cond_forward)

        self.uncomp(whilestmt._body)
        self.emit(MidSubi(counter_var, self.get_var(1)))

        self.emit(MidBranchControl(self.get_var(whilestmt._cond.name(), whilestmt._cond.index()), label_cond_forward), label_cond_backward)
        self.emit(MidBranchControl(counter_var, label_counter_forward), label_counter_backward)

    def uncomp_AssignNode(self, assign):
        tempvar = self.get_var(self.emitter.get_tempvar_name())
        left = self.get_var(assign._left.name(), assign._left.index())
        if isinstance(assign._right, UnaOpNode):
            self.emit(Pop(tempvar))
            self.emit(MidSwap(tempvar, left))
            self.emit(MidArithmetic(assign._right._op.value, tempvar, self.get_var(assign._right._right.name(), assign._right._right.index())))
        elif isinstance(assign._right, BinOpNode):
            self.emit(Pop(tempvar))
            self.emit(MidSwap(tempvar, left))
            self.emit(MidArithmeticB(assign._right._op.value, tempvar, self.get_var(assign._right._left.name(), assign._right._left.index()), self.get_var(assign._right._right.name(), assign._right._right.index())))
        elif isinstance(assign._right, SingletonNode) and isinstance(assign._right._value, NumNode):
            self.emit(MidXori(left, self.get_var(assign._right.value())))
            self.emit(Pop(left))
        elif isinstance(assign._right, SingletonNode) and isinstance(assign._right._value, IDNode):
            self.emit(MidXor(left, self.get_var(assign._right.name(), assign._right.index())))
            self.emit(Pop(left))
        else: raise Exception(f'Unhandled classical assignment of type {type(assign._right).__name__} for variable {assign._left.name()}')

    def visit_TopNode(self, topnode):
        self.emit(Start())
        ## optional: push inputs to procedure main
        self.emit(MidBranch(self.emitter.get_procbegin_label(topnode._entry)))
        ## optional: pop inputs to procedure main
        self.emit(Finish())

        self.visit(topnode._entry)
        for proc in topnode._procs:
            self.visit(proc)

    def visit_ProcNode(self, proc):
        proc_begin, proc_end, proc_entry = self.get_proc_labels(proc)
        self.emit(MidBranch(proc_end), proc_begin)
        self.emit(SwapBr(self.ro), proc_entry)
        self.emit(Negation(self.ro))

        self.init_params(proc)
        self.emit(Push(self.ro))
        self.visit(proc._body)

        self.uncomp(proc._body)
        self.emit(Pop(self.ro))
        self.init_params(proc)

        self.emit(MidBranch(proc_begin), proc_end)

    def init_params(self, proc):
        tempvars = []
        for param in reversed(proc._params):
            tempvar = self.get_var(self.emitter.get_tempvar_name())
            self.emit(Pop(tempvar))
            self.emit(MidSwap(tempvar, self.get_var(param.name())))
            tempvars.append(tempvar)
        for tempvar in reversed(tempvars):
            self.emit(Push(tempvar))

    def visit_IfStmtNode(self, ifstmt):
        branch_back = []
        for cond, body, pre in ifstmt._branches:
            if cond:
                self.visit(pre)
                label_cond_forward, label_cond_backward = self.get_label_pair()
                self.emit(MidBranchEqZ(self.get_var(cond.name(), cond.index()), label_cond_backward), label_cond_forward)

                self.visit(body)

                label_skip_forward, label_skip_backward = self.get_label_pair()
                self.emit(MidBranchControl(self.get_var(cond.name(), cond.index()), label_skip_backward), label_skip_forward)
                branch_back.append((MidBranchControl(self.get_var(cond.name(), cond.index()), label_skip_forward), label_skip_backward, pre))

                self.emit(MidBranchControl(self.get_var(cond.name(), cond.index()), label_cond_forward), label_cond_backward)
            else:
                self.visit(body)
        
        for inst, label, pre in reversed(branch_back):
            self.emit(inst, label)
            self.uncomp(pre)

    def visit_WhileStmtNode(self, whilestmt):
        label_counter_forward, label_counter_backward = self.get_label_pair()
        counter_var = self.get_var(self.emitter.get_tempvar_name())
        self.emit(MidBranchNeqZ(counter_var, label_counter_backward), label_counter_forward)

        self.visit(whilestmt._pre)
        label_cond_forward, label_cond_backward = self.get_label_pair()
        self.emit(MidBranchEqZ(self.get_var(whilestmt._cond.name(), whilestmt._cond.index()), label_cond_backward), label_cond_forward)

        self.emit(MidAddi(counter_var, self.get_var(1)))
        self.visit(whilestmt._body)

        self.emit(MidBranchControl(counter_var, label_counter_forward), label_counter_backward)
        self.emit(MidBranchControl(self.get_var(whilestmt._cond.name(), whilestmt._cond.index()), label_cond_forward), label_cond_backward)
        self.emit(Push(counter_var))

    def visit_QifStmtNode(self, qifstmt):
        qbit = self.get_var(qifstmt._qbits.name(), qifstmt._qbits._index._index.name())
        self.emit(MidQif(qbit))

        label_skip_zero_forward, label_skip_zero_backward = self.get_label_pair()
        label_skip_one_forward, label_skip_one_backward = self.get_label_pair()
        self.emit(MidBranchNeqZ(qbit, label_skip_zero_backward), label_skip_zero_forward)
        #self.visit(qifstmt)
        self.emit(MidBranchControl(qbit, label_skip_one_backward), label_skip_one_forward)
        self.emit(MidBranchControl(qbit, label_skip_zero_forward), label_skip_zero_backward)
        #self.visit
        self.emit(MidBranchEqZ(qbit, label_skip_one_forward), label_skip_one_backward)

        self.emit(MidFiq(qbit))

    def visit_CallNode(self, call):
        for param in call._params:
            self.emit(Push(self.get_var(param.name())))

        self.emit(MidBranch(self.emitter.get_procentry_label(call._callee)))

        for param in reversed(call._params):
            self.emit(Pop(self.get_var(param.name())))

    def visit_AssignNode(self, assign):
        tempvar = self.get_var(self.emitter.get_tempvar_name())
        left = self.get_var(assign._left.name(), assign._left.index())
        if isinstance(assign._right, UnaOpNode):
            self.emit(MidArithmetic(assign._right._op.value, tempvar, self.get_var(assign._right._right.name(), assign._right._right.index())))
            self.emit(MidSwap(tempvar, left))
            self.emit(Push(tempvar))
        elif isinstance(assign._right, BinOpNode):
            self.emit(MidArithmeticB(assign._right._op.value, tempvar, self.get_var(assign._right._left.name(), assign._right._left.index()), self.get_var(assign._right._right.name(), assign._right._right.index())))
            self.emit(MidSwap(tempvar, left))
            self.emit(Push(tempvar))
        elif isinstance(assign._right, SingletonNode) and isinstance(assign._right._value, NumNode):
            self.emit(Push(left))
            self.emit(MidXori(left, self.get_var(assign._right.value())))
        elif isinstance(assign._right, SingletonNode) and isinstance(assign._right._value, IDNode):
            self.emit(Push(left))
            self.emit(MidXor(left, self.get_var(assign._right.name(), assign._right.index())))
        else: raise Exception(f'Unhandled classical assignment of type {type(assign._right).__name__} for variable {assign._left.name()}')

    def visit_UnitaryNode(self, unitary):
        gate = basic_gates[unitary.name()]
        if gate['qvar'] == 1:
            qreg = unitary._qbits[0].name()
            offset = unitary._qbits[0]._index._index
            if isinstance(offset, SingletonNode):
                self.emit(MidUnitary(unitary.name(), self.get_var(qreg, offset.name())))
            else:
                raise Exception(f'Unrecognized index for qubit register {qreg}')
        elif gate['qvar'] == 2:
            qreg1 = unitary._qbits[0].name()
            offset1 = unitary._qbits[0]._index._index
            qreg2 = unitary._qbits[1].name()
            offset2 = unitary._qbits[1]._index._index
            if isinstance(offset1, SingletonNode) and isinstance(offset2, SingletonNode):
                self.emit(MidUnitaryB(unitary.name(), self.get_var(qreg1, offset1.name()), self.get_var(qreg2, offset2.name())))
            else:
                raise Exception(f'Unrecognized index for qubit register {qreg}')
        else:
            raise Exception(f'Unhandled unitary type {unitary.name()}')

    def get_proc_labels(self, proc):
        return self.emitter.get_procbegin_label(proc), self.emitter.get_procend_label(proc), self.emitter.get_procentry_label(proc)
        
    def get_label_pair(self):
        return self.emitter.get_new_label(), self.emitter.get_new_label()
    
    def get_var(self, name, index=None):
        try:
            return Immediate(int(name))
        except:
            return Variable(name, index)
        
    def emit(self, inst, label=None):
        self.emitter.emit(inst, label)

    