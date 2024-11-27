from symboltable import SymbolTable

# AST Node classes
class ASTNode:
    def __init__(self):
        pass

    def add_symbol(self, symbol, type):
        pass

    def print(self):
        pass

    def equal_to(self, node):
        return False
    
class TopNode(ASTNode):
    # entry: ProcNode
    # procs: [ ProcNode ]
    # qregs: [ QRegNode ]
    def __init__(self, entry, procs, qregs):
        self._entry = entry
        self._procs = procs
        self._qregs = qregs
        self._symbols = SymbolTable()
        for proc in self._procs:
            # TODO
            pass
        for qreg in self._qregs:
            # TODO
            pass

    def add_symbol(self, symbol, type):
        # TODO
        pass
        for proc in self._procs:
            # TODO
            pass

    def print(self):
        # TODO
        print('Top')
        for qreg in self._qregs:
            qreg.print()
        print()
        for proc in self._procs:
            proc.print()
            print()

class ProcNode(ASTNode):
    # id: IDNode
    # params: [ IDNode ]
    # body: BlockNode
    def __init__(self, id, params, body):
        self._id = id
        self._params = params
        self._body = body
        self._symbols = SymbolTable()

    def add_symbol(self, symbol, type):
        # TODO
        pass

    def print(self):
        # TODO
        pass

class BlockNode(ASTNode):
    # statements: TODO
    def __init__(self, statements):
        self._statements = statements
        self._symbols = SymbolTable()

    def add_symbol(self, symbol, type):
        # TODO
        pass

    def print(self):
        # TODO
        pass

class IfStmtNode(ASTNode):
    # branches: [ (CValueNode: BlockNode) ]
    def __init__(self, branches):
        self._branches = branches

    def add_symbol(self, symbol, type):
        # TODO
        pass

    def print(self):
        # TODO
        pass

class QifStmtNode(ASTNode):
    # qbit: QBitNode
    # branches: [ (CValueNode: BlockNode) ]
    def __init__(self, qbit, branches):
        self._qbit = qbit
        self._branches = branches

    def add_symbol(self, symbol, type):
        # TODO
        pass

    def print(self):
        # TODO
        pass

class AssignNode(ASTNode):
    # left: IDNode
    # right: CValueNode
    def __init__(self, left, right):
        self._left = left
        self._right = right

    def add_symbol(self, symbol, type):
        # TODO
        pass

    def print(self):
        # TODO
        pass

class CallNode(ASTNode):
    # callee: IDNode
    # params: [ CValueNode ]
    def __init__(self, id, params):
        self._id = id
        self._params = params

    def add_symbol(self, symbol, type):
        # TODO
        pass

    def print(self):
        # TODO
        pass

class UnitaryNode(ASTNode):
    # unitary: IDNode
    # qbits: [ QBitNode ]
    def __init__(self, unitary, qbits):
        self._unitary = unitary
        self._qbits = qbits

    def add_symbol(self, symbol, type):
        # TODO
        pass

    def print(self):
        # TODO
        pass

class RangeNode(ASTNode):
    # low: CValueNode
    # up: CValueNode
    def __init__(self, low, up):
        self._low = low
        self._up = up

    def add_symbol(self, symbol, type):
        # TODO
        pass

    def print(self):
        # TODO
        pass

class QBitNode(ASTNode):
    # qreg: IDNode
    # range: RangeNode
    def __init__(self, qreg, range):
        self._qreg = qreg
        self._range = range

    def add_symbol(self, symbol, type):
        # TODO
        pass

    def print(self):
        # TODO
        pass

class QRegNode(ASTNode):
    # name: IDNode
    # length: CValueNode
    def __init__(self, name, length):
        self._name = name
        self._length = length

    def add_symbol(self, symbol, type):
        # TODO
        pass

    def print(self):
        # TODO
        pass

class NumNode(ASTNode):
    # value: int
    def __init__(self, value):
        self._value = value

    def print(self):
        print('(NumNode: ' + str(self._value) + ')', end='')

    def equal_to(self, node):
        return isinstance(node, NumNode) and self._value == node._value

class IDNode(ASTNode):
    # id: str
    def __init__(self, id):
        self._id = id

    def print(self):
        print('[IDNode: ' + str(self._id) + ']', end='')

    def equal_to(self, node):
        return isinstance(node, IDNode) and self._id == node._id

class SkipNode(ASTNode):
    def __init__(self):
        pass

    def print(self):
        print('[SkipNode]', end='')

    def equal_to(self, node):
        return isinstance(node, SkipNode)

class CValueNode(ASTNode):
    # abstract node of classical value
    def __init__(self):
        pass

    def value(self):
        pass

    def add_symbol(self, symbol, type):
        pass

    def print(self):
        pass

    def equal_to(self, node):
        return isinstance(node, CValueNode) and self.value() == node.value()

class BinOpNode(CValueNode):
    # left, right: CValueNode
    # op: Token
    def __init__(self, left, op, right):
        self._left = left
        self._op = op
        self._right = right
        self._symbols = SymbolTable()

    def value(self):
        if self._op.type == 'PLUS':
            return self._left.value() + self._right.value()
        elif self._op.type == 'MINUS':
            return self._left.value() - self._right.value()
        elif self._op.type == 'MULTIPLY':
            return self._left.value() * self._right.value()
        elif self._op.type == 'GREATEREQ':
            return self._left.value() >= self._right.value()
        elif self._op.type == 'GREATERTHAN':
            return self._left.value() > self._right.value()
        elif self._op.type == 'LESSEQ':
            return self._left.value() <= self._right.value()
        elif self._op.type == 'LESSTHAN':
            return self._left.value() < self._right.value()
        elif self._op.type == 'EQUALTO':
            return self._left.value() == self._right.value()
        else:
            raise Exception('Unexpected oprand:', self._op.value)

    def add_symbol(self, symbol, type):
        # TODO
        pass

    def print(self):
        # TODO
        pass
    
class SingletonNode(CValueNode):
    # value: IDNode or NumNode
    def __init__(self, value):
        self._value = value

    def value(self):
        if isinstance(self._value, IDNode):
            # TODO
            return 0
        elif isinstance(self._value, NumNode):
            return self._value._value
        else:
            raise Exception('Empty oprand')

    def print(self):
        if isinstance(self._value, IDNode):
            print('[IDNode: ' + str(self._value._id) + ']', end='')
        elif isinstance(self._value, NumNode): 
            print('(NumNode: ' + str(self._value._value) + ')', end='')
        else:
            raise Exception('Empty oprand')
