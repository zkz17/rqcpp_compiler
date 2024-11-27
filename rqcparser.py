from astnode import *

# Parser class
class RQCParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        if self.pos < len(self.tokens):
            #print(self.tokens[self.pos])
            return self.tokens[self.pos]
        else:
            return None

    def consume(self, expected_type=None):
        token = self.current_token()
        if token is None:
            raise Exception('Unexpected end of input')
        if expected_type and token.type != expected_type:
            raise Exception(f'Expected {expected_type}, found {token.type}')
        self.pos += 1
        return token

    def parse(self):
        return self.program()
    
    def program(self):
        qregs = []
        procs = []
        entry = None

        newline = self.current_token()
        while not newline is None:
            self.consume('NEWLINE')
            if self.current_token() and self.current_token().type == 'QBITS': # Qubit register declaration
                qregs += self.qregs()
            elif self.current_token() and self.current_token().type == 'PROCEDURE': # Procedure declaration
                self.consume('PROCEDURE')
                if self.current_token() and self.current_token().type == 'MAIN':
                    if entry: raise Exception('Conflict definition of procedure \'main\'')
                    entry = self.main()
                else:
                    procs.append(self.procedure())

            newline = self.current_token()

        return TopNode(entry, procs, qregs)
    
    def main(self):
        self.consume('MAIN')
        self.consume('LPAREN')
        self.consume('RPAREN')
        self.consume('COLON')
        body = self.block_statement()
        return ProcNode(IDNode('main'), [], body)
    
    def procedure(self):
        token = self.consume('ID')
        id = IDNode(str(token.value))

        ## Parse procedure params
        params = []
        self.consume('LPAREN')
        while True:
            params.append(IDNode(str(self.consume('ID').value)))
            token = self.consume()
            if token.type == 'COMMA': continue
            elif token.type == 'RPAREN': break
            else: raise Exception('Unexpected token:', token)

        ## Parse procedure body
        self.consume('COLON')
        body = self.block_statement()

        return ProcNode(id, params, body)
    
    def block_statement(self):
        statements = []
        self.consume('INDENT')
        while self.current_token() and self.current_token().type != 'DEDENT':
            self.consume('NEWLINE')
            statements.append(self.statement())
        self.consume('DEDENT')
        return BlockNode(statements)
    
    def statement(self):
        token = self.current_token()
        if token.type == 'SKIP':
            self.consume('SKIP')
            return SkipStmtNode()
        elif token.type == 'IF':
            return self.if_statement()
        elif token.type == 'WHILE':
            return self.while_statement()
        elif token.type == 'QIF':
            return self.qif_statement()
        elif token.type == 'BEGIN':
            return self.local_statement()
        elif token.type == 'ID':
            self.consume('ID')
            id = IDNode(str(token.value))

            token = self.current_token()
            if not token or token.type == 'NEWLINE' or token.type == 'DEDENT': # What are you doing? 
                return id
            elif token.type == 'ASSIGN': # AssignNode
                self.consume('ASSIGN')
                right = self.classical_expr()
                return AssignNode(id, right)
            elif token.type == 'LBRACKET': # UnitaryNode
                self.consume('LBRACKET')
                qbits = []
                ## Parse qbits
                while True:
                    qbits.append(self.qbit())
                    if self.current_token() and self.current_token().type == 'COMMA': self.consume('COMMA')
                    else: break
                self.consume('RBRACKET')
                return UnitaryNode(id, qbits)
            elif token.type == 'LPAREN': # CallNode
                self.consume('LPAREN')
                params = []
                while True:
                    params.append(self.classical_expr())
                    if self.current_token() and self.current_token().type == 'COMMA': self.consume('COMMA')
                    else: break
                self.consume('RPAREN')
                return CallNode(id, params)
        else: raise Exception('Unexpected token:', token)
        
    def if_statement(self):
        branches = []

        ## Parse 'if' condition and body
        self.consume('IF')
        cond = self.expr_boolean()
        self.consume('THEN')
        self.consume('COLON')
        body = self.block_statement()
        branches.append((cond, body))
        self.consume('NEWLINE')

        ## Parse optional 'elif' condition and body
        while self.current_token() and self.current_token().type == 'ELIF':
            self.consume('ELIF')
            cond = self.expr_boolean()
            self.consume('THEN')
            self.consume('COLON')
            body = self.block_statement()
            branches.append((cond, body))
            self.consume('NEWLINE')

        ## Parse optional 'else' condition and body
        if self.current_token() and self.current_token().type == 'ELSE':
            self.consume('ELSE')
            self.consume('COLON')
            body = self.block_statement()
            branches.append((None, body))
            self.consume('NEWLINE')

        self.consume('FI')
        return IfStmtNode(branches)
    
    def while_statement(self):
        self.consume('WHILE')
        cond = self.expr_boolean()
        self.consume('DO')
        self.consume('COLON')
        body = self.block_statement()
        self.consume('NEWLINE')
        self.consume('OD')
        return WhileStmtNode(cond, body)
    
    def qif_statement(self):
        self.consume('QIF')
        qbit = self.qbit()
        self.consume('COLON')
        self.consume('INDENT')

        ## Parse guarded commands
        branches = []
        while self.current_token() and self.current_token().type != 'DEDENT':
            self.consume('NEWLINE')
            ket = self.consume('KET')
            guard = int(str(ket.value)[1:-1])
            self.consume('RARROW')
            body = self.block_statement()
            branches.append((guard, body))

        self.consume('DEDENT')
        self.consume('NEWLINE')
        self.consume('FIQ')
        return QifStmtNode(qbit, branches)
    
    def local_statement(self):
        self.consume('BEGIN')
        self.consume('LOCAL')

        ## Parse local assignment
        localvars = []
        while True:
            id = IDNode(str(self.consume('ID').value))
            self.consume('ASSIGN')
            right = self.classical_expr()
            localvars.append(AssignNode(id, right))
            if self.current_token() and self.current_token().type == 'COMMA': self.consume('COMMA')
            else: break

        self.consume('COLON')
        body = self.block_statement()
        self.consume('NEWLINE')
        self.consume('END')
        return LocalStmtNode(localvars, body)

    def qbit(self):
        qreg = IDNode(str(self.consume('ID').value))
        range = RangeNode(None, None)
        if self.current_token() and self.current_token().type == 'LBRACKET':
            self.consume('LBRACKET')
            range = self.range()
            self.consume('RBRACKET')
        return QBitNode(qreg, range)

    def qregs(self):
        qregs = []
        self.consume('QBITS')
        token = self.consume('ID')
        id = IDNode(str(token.value))

        while True: # parallel definition divided by COMMA
            token = self.current_token()
            if token.type == 'LBRACKET': 
                self.consume('LBRACKET')
                length = self.classical_expr()
                self.consume('RBRACKET')
                qregs.append(QRegNode(id, length))
                    
            if self.current_token().type == 'COMMA':
                self.consume('COMMA')
                token = self.consume('ID')
                id = IDNode(str(token.value))
            else: 
                break
        return qregs
    
    def range(self):
        if self.current_token() and self.current_token().type == 'COLON':
            self.consume('COLON')
            up = self.classical_expr()
            return RangeNode(None, up)
        else:
            low = self.classical_expr()
            if self.current_token() and self.current_token().type == 'COLON':
                self.consume('COLON')
                up = None
                if self.current_token() and self.current_token().type != 'RBRACKET':
                    up = self.classical_expr()
                return RangeNode(low, up)
            else: return RangeNode(low, low)

    def classical_expr(self): 
        return self.expr_plus_minus()
    
    def expr_boolean(self):
        node = self.expr_plus_minus()

        while self.current_token and self.current_token().type in ['GREATEREQ', 'GREATERTHAN', 'LESSEQ', 'LESSTHAN', 'EQUALTO']: 
            op = self.consume()
            right = self.expr_plus_minus()
            node = BinOpNode(node, op, right)
        return node
    
    def expr_plus_minus(self):
        node = self.expr_mul_div()

        while self.current_token and self.current_token().type in ['PLUS', 'MINUS']:
            op = self.consume()
            right = self.expr_mul_div()
            node = BinOpNode(node, op, right)
        return node

    def expr_mul_div(self):
        node = self.expr_primary()

        while self.current_token() and self.current_token().type in ['MULTIPLY']:
            op = self.consume()
            right = self.expr_primary()
            node = BinOpNode(node, op, right)
        return node

    def expr_primary(self):
        token = self.current_token()
        if token.type == 'LPAREN':
            self.consume('LPAREN')
            expr = self.expr_boolean()
            self.consume('RPAREN')
            return expr
        else:
            return SingletonNode(self.term())

    def term(self):
        token = self.current_token()
        if token.type == 'INTEGER':
            self.consume()
            return NumNode(int(token.value))
        elif token.type == 'ID':
            self.consume()
            return IDNode(str(token.value))
        else:
            raise Exception('Unexpected token:', token)