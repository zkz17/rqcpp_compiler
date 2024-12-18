from utils.symboltable import SymbolTable

# AST Node classes
class ASTNode:
    def __init__(self):
        pass

    def print(self, level=0, end='\n'):
        pass

    def print_indent(self, level):
        print('    ' * level, end='')

    def equal_to(self, node):
        return False
    
    def name(self):
        return ''
    
class TopNode(ASTNode):
    # entry: ProcNode
    # procs: [ ProcNode ]
    # qregs: [ QRegNode ]
    # arrays: [ ArrayDeclNode ]
    # proc_arrays: [ ProcArrayNode ]
    def __init__(self, entry, procs, qregs, arrays, proc_arrays=[]):
        self._entry = entry
        self._procs = procs
        self._qregs = qregs
        self._arrays = arrays
        self._proc_arrays = proc_arrays
        self._symbols = SymbolTable()

    def print(self, level=0, end='\n'):
        self.print_indent(level)
        print('TopNode')

        ## print defined qregs
        self.print_indent(level)
        print('  qregs: ')
        for qreg in self._qregs:
            qreg.print(level + 1)

        ## print declared arrays
        self.print_indent(level)
        print('  arrays: ')
        for array in self._arrays:
            array.print(level + 1)

        ## print registered procedure arrays
        self.print_indent(level)
        print('  procedure arrays: ')
        for parray in self._proc_arrays:
            parray.print(level + 1)
        
        ## print entry point
        self.print_indent(level)
        print('  entry: ')
        self._entry.print(level + 1)

        ## print defined procedures
        self.print_indent(level)
        print('  procedures: ')
        for proc in self._procs:
            proc.print(level + 1)

class ProcNode(ASTNode):
    # id: IDNode
    # index : NumNode or None
    # params: [ IDNode ]
    # body: BlockNode
    def __init__(self, id, params, body, index=None):
        self._id = id
        self._params = params
        self._body = body
        self._index = index

    def print(self, level=0, end='\n'):
        self.print_indent(level)
        print('ProcNode')

        self.print_indent(level)
        print('  ID: ', end='')
        self._id.print(level + 1)
        
        if self._index:
            self.print_indent(level)
            print('  index: ', self._index._value)

        self.print_indent(level)
        print('  params: ', end='')
        for param in self._params:
            param.print(0, ' ')
        print()

        self.print_indent(level)
        print('  body: ', end='')
        self._body.print(level + 1)

    def name_in_array(self):
        if self._index: return f'{self.name()}[{self._index._value}]'
        return self.name()

    def name(self):
        return self._id.name()

class BlockNode(ASTNode):
    # statements: [ IfStmtNode | QifStmtNode | LocalStmtNode | WhileStmtNode | SkipStmtNode | AssignNode | UnitaryNode | CallNode ]
    def __init__(self, statements):
        self._statements = statements
        self._symbols = SymbolTable()

    def print(self, level=0, end='\n'):
        print('BlockNode')
        for stmt in self._statements:
            stmt.print(level)

class IfStmtNode(ASTNode):
    # branches: [ (cond: CValueNode, body: BlockNode, pre: BlockNode) ]
    def __init__(self, branches):
        self._branches = branches

    def print(self, level=0, end='\n'):
        self.print_indent(level)
        print('IfStmtNode')
        for cond, body, pre in self._branches:
            if pre:
                self.print_indent(level)
                print('  preprocess: ', end='')
                pre.print(level + 1)

            self.print_indent(level)
            if cond:
                print('  ->cond: ', end='')
                cond.print(0)
            else: 
                print('  else: ')

            self.print_indent(level)
            print('  ->', end='')
            body.print(level + 1)

class WhileStmtNode(ASTNode):
    # cond: CValueNode
    # body: BlockNode
    # pre: BlockNode
    def __init__(self, cond, body, pre=None):
        self._cond = cond
        self._body = body
        self._pre = pre

    def print(self, level=0, end='\n'):
        self.print_indent(level)
        print('WhileStmtNode')

        self.print_indent(level)
        print('  cond: ', end='')
        self._cond.print(0)

        if self._pre:
            self.print_indent(level)
            print('  preprocess: ', end='')
            self._pre.print(level + 1)

        self.print_indent(level)
        print('  body: ', end='')
        self._body.print(level + 1)

class QifStmtNode(ASTNode):
    # qbits: QBitNode
    # branches: { int: BlockNode or CallNode }
    def __init__(self, qbits, branches):
        self._qbits = qbits
        self._branches = branches

    def print(self, level=0, end='\n'):
        self.print_indent(level)
        print('QifStmtNode')

        self.print_indent(level)
        print('  qbits:')
        self._qbits.print(level + 1)

        self.print_indent(level)
        print('  branches: ')
        for val, body in self._branches:
            self.print_indent(level + 1)
            print('|' + str(val) + '> -> ', end='')
            if isinstance(body, BlockNode): body.print(level + 2)
            elif isinstance(body, CallNode): 
                print()
                body.print(level + 2)
            else: raise Exception(f'Unexpected operation')

class LocalStmtNode(ASTNode):
    # localvars: [ AssignNode ]
    # body: BlockNode
    def __init__(self, localvars, body):
        self._localvars = localvars
        self._body = body

    def print(self, level=0, end='\n'):
        self.print_indent(level)
        print('LocalStmtNode')

        self.print_indent(level)
        print('  localvars: ', end='')
        for var in self._localvars:
            print('[ ', end='')
            var.print(0, ' ] ')
        print()

        self.print_indent(level)
        print('  body: ', end='')
        self._body.print(level + 1)

class SkipStmtNode(ASTNode):
    def __init__(self):
        pass

    def print(self, level=0, end='\n'):
        self.print_indent(level)
        print('SkipStmtNode')

    def equal_to(self, node):
        return isinstance(node, SkipStmtNode)

class AssignNode(ASTNode):
    # left: IDNode or ArrayElementNode
    # right: CValueNode
    def __init__(self, left, right):
        self._left = left
        self._right = right

    def print(self, level=0, end='\n'):
        self.print_indent(level)
        print('AssignNode: ', end='')
        self._left.print(0, ' = ')
        self._right.print(0, end=end)

class CallNode(ASTNode):
    # callee: IDNode or ArrayElementNode
    # params: [ CValueNode ]
    def __init__(self, callee, params):
        self._callee = callee
        self._params = params

    def print(self, level=0, end='\n'):
        self.print_indent(level)
        print('CallNode')

        self.print_indent(level)
        print('  callee: ', end='')
        self._callee.print(0)

        self.print_indent(level)
        print('  params: ', end='')
        for param in self._params:
            param.print(0, ' ')
        print()

    def name_in_array(self):
        return self._callee.name_in_array()

    def name(self):
        return self._callee.name()

class UnitaryNode(ASTNode):
    # gate: BasicGateNode
    # qbits: [ QBitNode ]
    def __init__(self, gate, qbits):
        self._gate = gate
        self._qbits = qbits

    def print(self, level=0, end='\n'):
        self.print_indent(level)
        print('UnitaryNode')

        self.print_indent(level)
        print('  gate: ', end='')
        self._gate.print(0)

        self.print_indent(level)
        print('  qbits: ')
        for qbit in self._qbits:
            qbit.print(level + 1)

    def name(self):
        return self._gate.name()

class RangeNode(ASTNode):
    # low: CValueNode
    # up: CValueNode
    # index: CValueNode
    def __init__(self, low, up):
        self._low = low
        self._up = up

    def print(self, level=0, end='\n'):
        print('[RangeNode: low = ', end='')
        if self._low: self._low.print(0, ', ')
        else: print('None, ', end='')
        print('up = ', end='')
        if self._up: self._up.print(0, ']' + end)
        else: print('None]', end=end)

class IndexNode(ASTNode):
    # index: CValueNode
    def __init__(self, index):
        self._index = index

    def print(self, level=0, end='\n'):
        if self._index:
            print('[IndexNode: ', end='')
            self._index.print(0, '')
            print(' ]', end=end)
        else:
            print('None', end=end)

    def name(self):
        return self._index.name()

class ArrayElementNode(ASTNode):
    # id: IDNode
    # array: IDNode or ArrayElementNodeay
    # index: IndexNode
    def __init__(self, array, index):
        self._array = array
        self._index = index
        if isinstance(array, IDNode): self._id = array
        else: self._id = array._id

    def print(self, level=0, end='\n'):
        self.print_indent(level)
        print('[ArrayElementNode: ', end='')
        self._array.print(0, ', ')
        self._index.print(0, '')
        print(']', end=end)

    def name_in_array(self):
        return f'{self.name()}[{self._index.name()}]'

    def name(self):
        return self._id.name()

class QBitNode(ASTNode):
    # qreg: IDNode
    # range: IndexNode
    def __init__(self, qreg, index):
        self._qreg = qreg
        self._index = index

    def print(self, level=0, end='\n'):
        self.print_indent(level)
        print('QBitNode')

        self.print_indent(level)
        print('  qreg: ', end='')
        self._qreg.print(level + 1)

        self.print_indent(level)
        print('  index: ', end='')
        self._index.print(level + 1)

    def name(self):
        return self._qreg.name()

class QRegNode(ASTNode):
    # id: IDNode
    # length: CValueNode
    def __init__(self, id, length):
        self._id = id
        self._length = length

    def print(self, level=0, end='\n'):
        self.print_indent(level)
        print('QRegNode')

        self.print_indent(level)
        print('  id: ', end='')
        self._id.print(level + 1)

        self.print_indent(level)
        print('  length: ', end='')
        self._length.print(level + 1)

    def name(self):
        return self._id.name()

class NumNode(ASTNode):
    # value: int
    def __init__(self, value):
        self._value = value

    def print(self, level=0, end='\n'):
        print('[NumNode: ' + str(self._value) + ']', end=end)

    def equal_to(self, node):
        return isinstance(node, NumNode) and self._value == node._value

class IDNode(ASTNode):
    # id: str
    def __init__(self, id):
        self._id = id

    def print(self, level=0, end='\n'):
        print('[IDNode: ' + str(self._id) + ']', end=end)

    def equal_to(self, node):
        return isinstance(node, IDNode) and self._id == node._id

    def name_in_array(self):
        return self._id
    
    def name(self):
        return self._id
    
class BasicGateNode(IDNode):
    # id: str
    def __init__(self, id):
        self._id = id

    def print(self, level=0, end='\n'):
        print('[BasicGateNode: ' + str(self._id) + ']', end=end)

    def equal_to(self, node):
        return isinstance(node, BasicGateNode) and self._id == node._id
    
    def name(self):
        return self._id
        
class UndefinedNode(ASTNode):
    def __init__(self):
        pass
    
    def print(self, level=0, end='\n'):
        print('[UndefinedNode]', end=end)

class ArrayDeclNode(ASTNode):
    # id: IDNode
    # dimensions: [ CValueNode ]
    def __init__(self, id, dimensions):
        self._id = id
        self._dimensions = dimensions

    def print(self, level=0, end='\n'):
        self.print_indent(level)
        print('ArrayDeclNode')

        self.print_indent(level)
        print('  id: ', end='')
        self._id.print(level + 1)

        self.print_indent(level)
        print('  dimensions: ', end='')
        for dimension in self._dimensions:
            dimension.print(0, ' ')
        print()

    def name(self):
        return self._id.name()
    
class ProcArrayNode(ASTNode):
    # id: IDNode
    # size : NumNode
    # params: [ IDNode ]
    def __init__(self, id, size, params):
        self._id = id
        self._size = size
        self._params = params

    def print(self, level=0, end='\n'):
        self.print_indent(level)
        print('ProcArrayNode')

        self.print_indent(level)
        print('  ID: ', end='')
        self._id.print(level + 1)

        self.print_indent(level)
        print('  size: ', end='')
        self._size.print(0)

        self.print_indent(level)
        print('  params: ', end='')
        for param in self._params:
            param.print(0, ' ')
        print()

    def size(self):
        return self._size._value

    def name(self):
        return self._id.name()

class CValueNode(ASTNode):
    # abstract node of classical value
    def __init__(self):
        pass

    def value(self):
        pass

    def print(self, level=0, end='\n'):
        pass

    def equal_to(self, node):
        return isinstance(node, CValueNode) and self.value() == node.value()
    
class UnaOpNode(CValueNode):
    # right: CValueNode
    # op: Token
    def __init__(self, op, right):
        self._op = op
        self._right = right

    def value(self):
        if not self._right.value(): 
            return None
        elif self._op.type == 'MINUS':
            return -self._right.value()
        elif self._op.type == 'NOT':
            return not self._right.value()
        else:
            raise Exception('Unrecognized operator: ', self._op.value)
        
    def print(self, level=0, end='\n'):
        print('[CValueNode: ', end='')
        if self._op.type == 'MINUS':
            print('- ', end='')
        elif self._op.type == 'NOT':
            print('NOT ', end='')
        else:
            raise Exception('Unrecognized operator: ', self._op.value)
        self._right.print(0, '')
        print(']', end=end)

class BinOpNode(CValueNode):
    # left, right: CValueNode
    # op: Token
    def __init__(self, left, op, right):
        self._left = left
        self._op = op
        self._right = right

    def value(self):
        if not self._left.value() or not self._right.value():
            return None
        elif self._op.type == 'PLUS':
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
        elif self._op.type == 'NOTEQUAL':
            return self._left.value() != self._right.value()
        elif self._op.type == 'AND':
            return self._left.value() and self._right.value()
        elif self._op.type == 'OR':
            return self._left.value() or self._right.value()
        else:
            raise Exception('Unrecognized operator:', self._op.value)

    def print(self, level=0, end='\n'):
        print('[CValueNode: ', end='')
        self._left.print(0, '')
        if self._op.type == 'PLUS':
            print(' + ', end='')
        elif self._op.type == 'MINUS':
            print(' - ', end='')
        elif self._op.type == 'MULTIPLY':
            print(' * ', end='')
        elif self._op.type == 'GREATEREQ':
            print(' >= ', end='')
        elif self._op.type == 'GREATERTHAN':
            print(' > ', end='')
        elif self._op.type == 'LESSEQ':
            print(' < ', end='')
        elif self._op.type == 'LESSTHAN':
            print(' <= ', end='')
        elif self._op.type == 'EQUALTO':
            print(' == ', end='')
        elif self._op.type == 'NOTEQUAL':
            print(' != ', end='')
        elif self._op.type == 'AND':
            print(' and ', end='')
        elif self._op.type == 'OR':
            print(' or ', end='')
        else:
            raise Exception('Unexpected oprand:', self._op.value)
        self._right.print(0, '')
        print(']', end=end)
    
class SingletonNode(CValueNode):
    # value: IDNode or NumNode or ArrayElementNode
    def __init__(self, value):
        self._value = value

    def value(self):
        if isinstance(self._value, IDNode):
            return None
        elif isinstance(self._value, NumNode):
            return self._value._value
        elif isinstance(self._value, ArrayElementNode):
            return None
        else:
            raise Exception('Empty oprand')

    def print(self, level=0, end='\n'):
        if isinstance(self._value, IDNode):
            print('[SingletonNode: variable ' + str(self._value._id) + ']', end=end)
        elif isinstance(self._value, NumNode): 
            print('[SingletonNode: ' + str(self._value._value) + ']', end=end)
        elif isinstance(self._value, ArrayElementNode): 
            print('[SingletonNode: ', end='')
            self._value.print(0, '')
            print(']', end=end)
        else:
            raise Exception('Empty oprand')
        
    def name(self):
        if isinstance(self._value, IDNode):
            return self._value.name()
        elif isinstance(self._value, NumNode):
            return self._value._value
        return ''
        
class ProcParamNode(CValueNode):
    # id: IDNode
    def __init__(self, id):
        self._id = id

    def value(self):
        return None

    def print(self, level=0, end='\n'):
        print('[ProcParamNode: param ' + str(self._id._id) + ']', end=end)
