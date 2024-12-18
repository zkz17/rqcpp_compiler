# Label class
class Label:
    def __init__(self, label, suffix='', index=''):
        self.label = label
        self.suffix = suffix
        self.index = index
        self.line = -1
        self.imm = 0

    def set_line(self, line):
        self.line = line

    def to_string(self):
        return self.label + self.index + self.suffix