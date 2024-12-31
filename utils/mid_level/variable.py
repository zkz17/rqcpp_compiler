# Mid-Level Variable class
class Variable:
    def __init__(self, name, index=None):
        self.name = name
        if index: self.index = Variable(index)
        else: self.index = index

    def is_immediate(self):
        return False

    def to_string(self):
        return self.name + ('[' + self.index.to_string() + ']' if self.index else '')
    
class Immediate(Variable):
    def __init__(self, value):
        self.value = value

    def is_immediate(self):
        return True

    def to_string(self):
        return str(self.value)