# Memory Table Entry class
class MemoryEntry:
    def __init__(self, name, offset, size=1):
        self.name = name
        self.offset = offset
        self.size = size

    def to_string(self):
        return f'name: {self.name}, offset: {self.offset}, size: {self.size}'

# Memory Location Table class
class MemoryTable:
    def __init__(self):
        self.ctable = {}
        self.ccounter = 0
        self.qtable = {}
        self.qcounter = 0
        self.cword_length = 1

    def offset(self, varname):
        if varname in self.ctable:
            return self.ctable[varname].offset
        elif varname in self.qtable:
            return self.qtable[varname].offset + self.ccounter * self.cword_length

    def allocate(self, name, size=1):
        if not name in self.ctable and not name in self.qtable:
            self.ctable[name] = MemoryEntry(name, self.ccounter, size)
            self.ccounter += size

    def qallocate(self, name, size):
        if not name in self.qtable:
            self.qtable[name] = MemoryEntry(name, self.qcounter, size)
            self.qcounter += size

    def alloc_arrays(self, symboltable):
        for name, symbol in symboltable.table.items():
            if symbol.type.is_quantum():
                self.qallocate(name, symbol.size)
            elif symbol.type.is_array():
                self.allocate(name, symbol.size)

    def print(self):
        print('classical variables: ')
        for entry in self.ctable.values():
            print('  ', entry.to_string())
        print('quantum variables: ')
        for entry in self.qtable.values():
            print('  ', entry.to_string())