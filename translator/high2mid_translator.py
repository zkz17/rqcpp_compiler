from utils.astnode import *
from utils.instruction_mid import *
from utils.instruction_low import SwapBr, Negation
from utils.code_emitter import CodeEmitter
from basic_gates import basic_gates

# High-Level to Mid-Level Translation class
class High2MidTransLator:
    def __init__(self):
        self.emitter = CodeEmitter()

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
                self.emit(MidBranchEqZ(cond.name(), label_cond_backward), label_cond_forward)

                self.uncomp(body)

                label_skip_forward, label_skip_backward = self.get_label_pair()
                self.emit(MidBranchControl(cond.name(), label_skip_backward), label_skip_forward)
                branch_back.append((MidBranchControl(cond.name(), label_skip_forward), label_skip_backward, pre))

                self.emit(MidBranchControl(cond.name(), label_cond_forward), label_cond_backward)
            else:
                self.uncomp(body)
        
        for inst, label, pre in reversed(branch_back):
            self.emit(inst, label)
            self.uncomp(pre)

    def uncomp_WhileStmtNode(self, whilestmt):
        label_counter_forward, label_counter_backward = self.get_label_pair()
        counter_var = self.emitter.get_tempvar_name()
        self.emit(Pop(counter_var))
        
        label_cond_forward, label_cond_backward = self.get_label_pair()
        self.emit(MidBranchNeqZ(whilestmt._cond.name(), label_cond_backward), label_cond_forward)

        self.uncomp(whilestmt._body)
        self.emit(MidSub(counter_var, 1))

        self.emit(MidBranchControl(whilestmt._cond.name(), label_cond_forward), label_cond_backward)
        self.emit(MidBranchControl(counter_var, label_counter_forward), label_counter_backward)

    def uncomp_AssignNode(self, assign):
        tempvar = self.emitter.get_tempvar_name()
        if isinstance(assign._right, UnaOpNode):
            self.emit(Pop(tempvar))
            self.emit(MidSwap(tempvar, assign._left.name()))
            self.emit(MidArithmetic(assign._right._op.value, tempvar, assign._right.name()))
        elif isinstance(assign._right, BinOpNode):
            self.emit(Pop(tempvar))
            self.emit(MidSwap(tempvar, assign._left.name()))
            self.emit(MidArithmeticB(assign._right._op.value, tempvar, assign._right._left.name(), assign._right._right.name()))
        elif isinstance(assign._right, SingletonNode) and isinstance(assign._right._value, NumNode):
            self.emit(MidXori(assign._left.name(), assign._right.value()))
            self.emit(Pop(assign._left.name()))
        elif isinstance(assign._right, SingletonNode) and isinstance(assign._right._value, IDNode):
            self.emit(MidXor(assign._left.name(), assign._right.name()))
            self.emit(Pop(assign._left.name()))
        else: raise Exception(f'Unhandled classical assignment of type {type(assign._right).__name__} for variable {assign._left.name()}')

    def visit_TopNode(self, topnode):
        self.emit(MidStart())
        ## optional: push inputs to procedure main
        self.emit(MidBranch(self.emitter.get_procbegin_label(topnode._entry)))
        ## optional: pop inputs to procedure main
        self.emit(MidFinish())

        self.visit(topnode._entry)
        for proc in topnode._procs:
            self.visit(proc)

    def visit_ProcNode(self, proc):
        proc_begin, proc_end, proc_entry = self.get_proc_labels(proc)
        self.emit(MidBranch(proc_end), proc_begin)
        self.emit(SwapBr('ro'), proc_entry)
        self.emit(Negation('ro'))

        self.init_params(proc)
        self.emit(Push('ro'))
        self.visit(proc._body)

        self.uncomp(proc._body)
        self.emit(Pop('ro'))
        self.init_params(proc)

        self.emit(MidBranch(proc_begin), proc_end)

    def init_params(self, proc):
        tempvars = []
        for param in reversed(proc._params):
            tempvar = self.emitter.get_tempvar_name()
            self.emit(Pop(tempvar))
            self.emit(MidSwap(tempvar, param.name()))
            tempvars.append(tempvar)
        for tempvar in reversed(tempvars):
            self.emit(Push(tempvar))

    def visit_IfStmtNode(self, ifstmt):
        branch_back = []
        for cond, body, pre in ifstmt._branches:
            if cond:
                self.visit(pre)
                label_cond_forward, label_cond_backward = self.get_label_pair()
                self.emit(MidBranchEqZ(cond.name(), label_cond_backward), label_cond_forward)

                self.visit(body)

                label_skip_forward, label_skip_backward = self.get_label_pair()
                self.emit(MidBranchControl(cond.name(), label_skip_backward), label_skip_forward)
                branch_back.append((MidBranchControl(cond.name(), label_skip_forward), label_skip_backward, pre))

                self.emit(MidBranchControl(cond.name(), label_cond_forward), label_cond_backward)
            else:
                self.visit(body)
        
        for inst, label, pre in reversed(branch_back):
            self.emit(inst, label)
            self.uncomp(pre)

    def visit_WhileStmtNode(self, whilestmt):
        label_counter_forward, label_counter_backward = self.get_label_pair()
        counter_var = self.emitter.get_tempvar_name()
        self.emit(MidBranchNeqZ(counter_var, label_counter_backward), label_counter_forward)

        self.visit(whilestmt._pre)
        label_cond_forward, label_cond_backward = self.get_label_pair()
        self.emit(MidBranchEqZ(whilestmt._cond.name(), label_cond_backward), label_cond_forward)

        self.emit(MidAdd(counter_var, 1))
        self.visit(whilestmt._body)

        self.emit(MidBranchControl(counter_var, label_counter_forward), label_counter_backward)
        self.emit(MidBranchControl(whilestmt._cond.name(), label_cond_forward), label_cond_backward)
        self.emit(Push(counter_var))

    def visit_QifStmtNode(self, qifstmt):
        self.emit(MidQif(qifstmt._qbits.name(), qifstmt._qbits._range._index.name()))

        label_skip_zero_forward, label_skip_zero_backward = self.get_label_pair()
        label_skip_one_forward, label_skip_one_backward = self.get_label_pair()
        self.emit(MidBranchNeqZ(qifstmt._qbits.name(), label_skip_zero_backward, qifstmt._qbits._range._index.name()), label_skip_zero_forward)
        #self.visit(qifstmt)
        self.emit(MidBranchControl(qifstmt._qbits.name(), label_skip_one_backward, qifstmt._qbits._range._index.name()), label_skip_one_forward)
        self.emit(MidBranchControl(qifstmt._qbits.name(), label_skip_zero_forward, qifstmt._qbits._range._index.name()), label_skip_zero_backward)
        #self.visit
        self.emit(MidBranchEqZ(qifstmt._qbits.name(), label_skip_one_forward, qifstmt._qbits._range._index.name()), label_skip_one_backward)

        self.emit(MidFiq(qifstmt._qbits.name(), qifstmt._qbits._range._index.name()))

    def visit_CallNode(self, call):
        for param in call._params:
            self.emit(Push(param.name()))

        self.emit(MidBranch(self.emitter.get_procentry_label(call)))

        for param in reversed(call._params):
            self.emit(Pop(param.name()))

    def visit_AssignNode(self, assign):
        tempvar = self.emitter.get_tempvar_name()
        if isinstance(assign._right, UnaOpNode):
            self.emit(MidArithmetic(assign._right._op.value, tempvar, assign._right.name()))
            self.emit(MidSwap(tempvar, assign._left.name()))
            self.emit(Push(tempvar))
        elif isinstance(assign._right, BinOpNode):
            self.emit(MidArithmeticB(assign._right._op.value, tempvar, assign._right._left.name(), assign._right._right.name()))
            self.emit(MidSwap(tempvar, assign._left.name()))
            self.emit(Push(tempvar))
        elif isinstance(assign._right, SingletonNode) and isinstance(assign._right._value, NumNode):
            self.emit(Push(assign._left.name()))
            self.emit(MidXori(assign._left.name(), assign._right.value()))
        elif isinstance(assign._right, SingletonNode) and isinstance(assign._right._value, IDNode):
            self.emit(Push(assign._left.name()))
            self.emit(MidXor(assign._left.name(), assign._right.name()))
        else: raise Exception(f'Unhandled classical assignment of type {type(assign._right).__name__} for variable {assign._left.name()}')

    def visit_UnitaryNode(self, unitary):
        gate = basic_gates[unitary.name()]
        if gate['qvar'] == 1:
            qreg = unitary._qbits[0].name()
            offset = unitary._qbits[0]._range._index
            if isinstance(offset, SingletonNode):
                self.emit(MidUnitary(unitary.name(), qreg, offset.name()))
            else:
                raise Exception(f'Unrecognized index for qubit register {qreg}')
        elif gate['qvar'] == 2:
            qreg1 = unitary._qbits[0].name()
            offset1 = unitary._qbits[0]._range._index
            qreg2 = unitary._qbits[1].name()
            offset2 = unitary._qbits[1]._range._index
            if isinstance(offset1, SingletonNode) and isinstance(offset2, SingletonNode):
                self.emit(MidUnitaryB(unitary.name(), qreg1, offset1.name(), qreg2, offset2.name()))
            else:
                raise Exception(f'Unrecognized index for qubit register {qreg}')
        else:
            raise Exception(f'Unhandled unitary type {unitary.name()}')

    def get_proc_labels(self, proc):
        return self.emitter.get_procbegin_label(proc), self.emitter.get_procend_label(proc), self.emitter.get_procentry_label(proc)
        
    def get_label_pair(self):
        return self.emitter.get_new_label(), self.emitter.get_new_label()
        
    def emit(self, inst, label=None):
        self.emitter.emit(inst, label)

    