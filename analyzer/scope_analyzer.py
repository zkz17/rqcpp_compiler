from utils.symboltable import SymbolTable
from utils.astnode import *

# Scope Analyzer class
class ScopeAnalyzer:
    def __init__(self):
        self.global_scope = SymbolTable()
        self.current_scope = self.global_scope

    def analyze(self, ast):
        self.register_procs(ast)
        self.register_qregs(ast)
        self.visit(ast)

    def register_procs(self, topnode):
        for proc in topnode._procs:
            self.global_scope.define(proc._id._id, 'p', proc)

    def register_qregs(self, topnode):
        for qreg in topnode._qregs:
            self.global_scope.define(qreg._id._id, 'q', qreg)

    def visit(self, node):
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name, self.generic_visit)
        method(node)

    def generic_visit(self, node):
        ## Default method for unhandled nodes
        if not node: return
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

    def visit_BlockNode(self, block):
        for stmt in block._statements:
            self.visit(stmt)

        block._symbols = self.current_scope

    def visit_QRegNode(self, qreg): 
        pass

    def visit_ProcNode(self, proc):
        self.enter_scope()
        for param in proc._params:
            self.current_scope.define(param._id, 'c', ProcParamNode(param))
        self.visit(proc._body)
        self.exit_scope()

    def visit_IfStmtNode(self, ifstmt):
        for cond, body in ifstmt._branches:
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
        self.current_scope.assign(assign._left._id, 'c', assign._right)

    def visit_CallNode(self, call):
        proc_name = call._id._id
        symbol = self.get_symbol(proc_name, 'p')
        if len(call._params) != len(symbol.value._params): raise Exception(f'Unmatched number of params for procedure call \'{proc_name}\'')

        for param in call._params:
            self.visit(param)
        
    def visit_UnitaryNode(self, unitary):
        # TODO
        # check unitary validity

        for qbit in unitary._qbits:
            self.visit(qbit)

    def visit_QBitNode(self, qbit):
        self.get_symbol(qbit._qreg._id, 'q')
        self.visit(qbit._range)

    def visit_RangeNode(self, range):
        if range._low: self.visit(range._low)
        if range._up: self.visit(range._up)

    def visit_BinOpNode(self, binop):
        self.visit(binop._left)
        self.visit(binop._right)

    def visit_SingletonNode(self, singleton):
        if isinstance(singleton._value, IDNode):
            self.get_symbol(singleton._value._id, 'c')

    def get_symbol(self, varname, type='c'):
        symbol = self.current_scope.resolve(varname)
        variable_type = {'c': 'classical variable', 'q': 'quantum variable', 'p': 'procedure'}

        if not symbol: raise Exception(f'Undefined reference to {variable_type[type]} \'{varname}\'')
        if symbol.type != type:
            if type == 'p': raise Exception(f'\'{varname}\' of type {variable_type[symbol.type]} is not callable')
            else: raise Exception(f'Unmatched variable type for {variable_type[symbol.type]} {varname}, expected: {variable_type[type]}')
        return symbol

    def enter_scope(self):
        self.current_scope = SymbolTable(parent=self.current_scope)

    def exit_scope(self):
        self.current_scope = self.current_scope.parent