from utils.astnode import *
from utils.instruction_mid import *
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

    def visit_TopNode(self, topnode):
        self.emitter.emit(MidStart())
        ## optional: push inputs to procedure main
        self.emitter.emit(MidBranch(self.emitter.get_procbegin_label(topnode._entry)))
        ## optional: pop inputs to procedure main
        self.emitter.emit(MidFinish())

        self.visit(topnode._entry)
        for proc in topnode._procs:
            self.visit(proc)

    def visit_IfStmtNode(self, ifstmt):
        pass

    def visit_WhileStmtNode(self, whilestmt):
        label0, label1 = self.emitter.get_new_label(), self.emitter.get_new_label()
        counter_var = self.emitter.get_tempvar_name()
        self.emitter.emit(MidBranchNeqZ(counter_var, label1), label0)

        label2, label3 = self.emitter.get_new_label(), self.emitter.get_new_label()
        self.emitter.emit(MidBranchEqZ(whilestmt._cond.name(), label3), label2)

        self.emitter.emit(MidAdd(counter_var, 1))
        self.visit(whilestmt._body)

        self.emitter.emit(MidBranchControl(counter_var, label0), label1)
        self.emitter.emit(MidBranchControl(whilestmt._cond.name(), label2), label3)

    def visit_CallNode(self, call):
        for param in call._params:
            self.emitter.emit(Push(param.name()))

        self.emitter.emit(MidBranch(self.emitter.get_procentry_label(call)))

        for param in reversed(call._params):
            self.emitter.emit(Pop(param.name()))

    def visit_UnitaryNode(self, unitary):
        gate = basic_gates[unitary.name()]
        if gate['qvar'] == 1:
            qreg = unitary._qbits[0].name()
            offset = unitary._qbits[0]._range._index
            if isinstance(offset, SingletonNode):
                self.emitter.emit(MidUnitary(unitary.name(), qreg, offset.name()))
            else:
                raise Exception(f'Unrecognized index for qubit register {qreg}')
        elif gate['qvar'] == 2:
            qreg1 = unitary._qbits[0].name()
            offset1 = unitary._qbits[0]._range._index
            qreg2 = unitary._qbits[1].name()
            offset2 = unitary._qbits[1]._range._index
            if isinstance(offset1, SingletonNode) and isinstance(offset2, SingletonNode):
                self.emitter.emit(MidUnitaryB(unitary.name(), qreg1, offset1.name(), qreg2, offset2.name()))
            else:
                raise Exception(f'Unrecognized index for qubit register {qreg}')
        else:
            raise Exception(f'Unhandled unitary type {unitary.name()}')

    