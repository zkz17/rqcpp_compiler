# Label class
class Label:
    def __init__(self, label, suffix='', index=''):
        self.label = label
        self.suffix = suffix
        self.index = index
        self.def_line = -1
        self.tgt_line = -1
        self.imm = 0

    def get_offset(self):
        return self.tgt_line - self.def_line

    def set_def_line(self, line):
        self.def_line = line

    def set_tgt_line(self, line):
        self.tgt_line = line

    def to_string(self):
        return self.label + ('' if self.index == '' else f'[{self.index}]') + self.suffix