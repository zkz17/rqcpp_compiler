# Label class
class Label:
    def __init__(self, name, suffix='', index=None):
        self.name = name
        self.suffix = suffix
        self.index = index
        self.def_line = -1
        self.tgt_line = -1
        self.imm = 0

    def is_immediate(self):
        return False

    def get_offset(self):
        return self.tgt_line - self.def_line

    def set_def_line(self, line):
        self.def_line = line

    def set_tgt_line(self, line):
        self.tgt_line = line

    def to_string(self):
        return self.name + (f'[{self.index.to_string()}]' if self.index else '') + self.suffix