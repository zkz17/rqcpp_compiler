from analyzer.analyzer import Analyzer
from utils.symboltable import SymbolTable
from utils.astnode import *
from utils.type import *

# Type Check Analyzer class
class TypeCheckAnalyzer(Analyzer):
    def __init__(self):
        self.current_scope = SymbolTable()

    def analyze(self, ast):
        self.current_scope = ast._symbols
        self.visit(ast)

    def visit_QRegNode(self, qreg):
        length = qreg._length.value()
        if not length:
            raise Exception(f'Non-determined legnth for quantum register {qreg._id._id}')
        if length <= 0:
            raise Exception(f'Quantum register {qreg._id._id} must have a positive length')
        qreg._length = SingletonNode(NumNode(length))

    def visit_ArrayDeclNode(self, array):
        for dimension in array._dimensions:
            if not dimension.value():
                raise Exception(f'Non-determined length for classical array {array._id._id}')
            if dimension.value() <= 0:
                raise Exception(f'Classical array {array._id._id} must have a positive length')

    def visit_BlockNode(self, block):
        self.enter_scope(block)
        for stmt in block._statements:
            self.visit(stmt)
        self.exit_scope()

    def visit_AssignNode(self, assign):
        if isinstance(assign._left, IDNode):
            self.visit(assign._right)
        elif isinstance(assign._left, ArrayElementNode):
            symbol = self.get_symbol(assign._left._id._id)
            arraytype = symbol.type
            array = assign._left
            while isinstance(array, ArrayElementNode):
                if not arraytype.is_array():
                    raise Exception(f'Insufficient dimensions for {type(symbol.type).__name__} variable \'{symbol.name}\'')
                array = array._array
                arraytype = arraytype.element_type

            if arraytype.is_classical():
                if isinstance(assign._right, ListNode):
                    raise Exception(f'Unmatched dimensions for assignment of variable {symbol.name}')
                self.visit(assign._right)
            elif arraytype.is_array():
                if not arraytype.element_type.is_classical():
                    raise Exception(f'Assignment of more-than-two-dimensional array {symbol.name} is prohibited')
                if not isinstance(assign._right, ListNode):
                    raise Exception(f'Unmatched dimensions for assignment of variable {symbol.name}')
                if arraytype.length != len(assign._right._cvals):
                    raise Exception(f'Unmatched number of elements for assignment of variable {symbol.name}')
                self.visit(assign._right)

    def visit_CallNode(self, call):
        proc_name = call._id._id
        symbol = self.get_symbol(proc_name)
        if not symbol.type.is_procedure(): 
            raise Exception(f'{type(symbol.type).__name__} variable \'{proc_name}\' is not callable') 
        if len(call._params) != symbol.type.num_param: 
            raise Exception(f'Unmatched number of params for procedure call \'{proc_name}\', required: {symbol.type.num_param}, given: {len(call._params)}')

        for param in call._params:
            self.visit(param)

    def visit_QBitNode(self, qbit):
        symbol = self.get_symbol(qbit._qreg._id)
        if not symbol.type.is_quantum():
            raise Exception(f'{type(symbol.type).__name__} variable \'{symbol.name}\' is not quantum')
        self.visit(qbit._range)

    def visit_SingletonNode(self, singleton):
        if isinstance(singleton._value, IDNode):
            symbol = self.get_symbol(singleton._value._id)
            if not symbol.type.is_classical():
                raise Exception(f'{type(symbol.type).__name__} variable \'{symbol.name}\' is not a non-array classical variable')
        elif isinstance(singleton._value, ArrayElementNode):
            array = singleton._value
            symbol = self.get_symbol(array._id._id)
            arraytype = symbol.type
            while isinstance(array, ArrayElementNode):
                if not arraytype.is_array():
                    raise Exception(f'Insufficient dimensions for {type(symbol.type).__name__} variable \'{symbol.name}\'')
                array = array._array
                arraytype = arraytype.element_type
            if not arraytype.is_classical():
                raise Exception(f'Unable to convert variable {symbol.name} into a non-array classical value')
