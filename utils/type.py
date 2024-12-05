# Variable Type classes
class Type:
    def __init__(self):
        pass

    def is_classical(self):
        return False
    
    def is_quantum(self):
        return False
    
    def is_array(self):
        return False
    
    def equal_to(self, type):
        return False
    
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

    def is_array(self):
        return True
    
    def equal_to(self, type):
        return isinstance(type, ArrayType) and self.element_type.equal_to(type.element_type)