from analyzer.analyzer import Analyzer
from utils.symboltable import SymbolTable
from utils.astnode import *
from utils.type import *

# Scope Analyzer class
class ScopeAnalyzer(Analyzer):
    def __init__(self):
        super().__init__()

    def analyze(self, ast):
        self.register_procs(ast)
        self.register_qregs(ast)
        self.register_arrays(ast)
        self.visit(ast)
        ast._symbols = self.global_scope

    def register_procs(self, topnode):
        for parray in topnode._proc_arrays:
            base_type = ProcedureType(len(parray._params))
            self.global_scope.allocate(parray.name(), ArrayType(base_type, parray.size()), parray.size())
        for proc in topnode._procs:
            self.global_scope.define(proc.name(), ProcedureType(len(proc._params)), proc._index)

    def register_qregs(self, topnode):
        for qreg in topnode._qregs:
            self.global_scope.allocate(qreg.name(), QuantumType(), qreg._length.value())

    def register_arrays(self, topnode):
        for array in topnode._arrays:
            etype = ClassicalType()
            for dimension in array._dimensions:
                etype = ArrayType(etype, dimension.value())
            self.global_scope.allocate(array.name(), etype, etype.length)

    def visit_BlockNode(self, block):
        for stmt in block._statements:
            self.visit(stmt)

        block._symbols = self.current_scope

    def visit_ProcNode(self, proc):
        self.enter_scope()
        for param in proc._params:
            self.current_scope.define(param._id, ProcParamType())
        self.visit(proc._body)
        self.exit_scope()

    def visit_IfStmtNode(self, ifstmt):
        for cond, body, _ in ifstmt._branches:
            if cond: self.visit(cond)
            self.enter_scope()
            self.visit(body)
            self.exit_scope()

    def visit_WhileStmtNode(self, whilestmt):
        self.visit(whilestmt._cond)
        self.enter_scope()
        self.visit(whilestmt._body)
        self.exit_scope()

    def visit_QifStmtNode(self, qifstmt):
        self.visit(qifstmt._qbits)
        for _, body in qifstmt._branches:
            self.enter_scope()
            self.visit(body)
            self.exit_scope()

    def visit_LocalStmtNode(self, localstmt):
        self.enter_scope()
        for assign in localstmt._localvars:
            self.visit(assign)
        self.visit(localstmt._body)
        self.exit_scope()

    def visit_AssignNode(self, assign):
        self.visit(assign._right)
        var = assign._left
        if isinstance(var, IDNode):
            self.current_scope.assign(var.name(), ClassicalType())
        elif isinstance(var, ArrayElementNode):
            self.get_symbol(var.name())

    def visit_CallNode(self, call):
        proc_name = call._callee.name()
        self.get_symbol(proc_name)

        for param in call._params:
            self.visit(param)
        
    def visit_UnitaryNode(self, unitary):
        for qbit in unitary._qbits:
            self.visit(qbit)

    def visit_QBitNode(self, qbit):
        self.get_symbol(qbit.name())
        self.visit(qbit._index)

    def visit_IndexNode(self, index):
        self.visit(index._index)

    def visit_RangeNode(self, range):
        if range._low: self.visit(range._low)
        if range._up: self.visit(range._up)

    def visit_BinOpNode(self, binop):
        self.visit(binop._left)
        self.visit(binop._right)

    def visit_SingletonNode(self, singleton):
        if isinstance(singleton._value, IDNode):
            self.get_symbol(singleton._value._id)
        elif isinstance(singleton._value, ArrayElementNode):
            self.get_symbol(singleton._value._id._id)

    def enter_scope(self):
        self.current_scope = SymbolTable(parent=self.current_scope)