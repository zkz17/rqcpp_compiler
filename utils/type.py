# Variable Type classes
class Type:
    def __init__(self):
        pass

    def is_param(self):
        return False

    def is_procedure(self):
        return False

    def is_classical(self):
        return False
    
    def is_quantum(self):
        return False
    
    def is_array(self):
        return False
    
    def equal_to(self, type):
        return False
    
class ProcParamType(Type):
    def __init__(self):
        super().__init__()

    def is_param(self):
        return True
    
    # Only classical param is allowed for now
    def is_classical(self):
        return True
    
    def equal_to(self, type):
        return isinstance(type, ProcParamType)
    
class ProcedureType(Type):
    def __init__(self, num_param=0):
        super().__init__()
        self.num_param = num_param
        self.param_types = []
        for i in range(num_param):
            self.param_types.append(ProcParamType())

    def is_procedure(self):
        return True
    
    def equal_to(self, type):
        return isinstance(type, ProcedureType)
    
class ClassicalType(Type):
    def __init__(self):
        super().__init__()

    def is_classical(self):
        return True
    
    def equal_to(self, type):
        return isinstance(type, ClassicalType)
    
class QuantumType(Type):
    def __init__(self):
        super().__init__()

    def is_quantum(self):
        return True
    
    def equal_to(self, type):
        return isinstance(type, QuantumType)
    
class ArrayType(Type):
    def __init__(self, element_type, length=0):
        self.element_type = element_type
        self.length = length

    def is_classical(self):
        return self.element_type.is_classical()

    def is_array(self):
        return True
    
    def equal_to(self, type):
        return isinstance(type, ArrayType) and self.element_type.equal_to(type.element_type)