class CodeList:
    def __init__(self):
        self.list = []
        self.line_counter = 1
        self.label_table = {}

    def insert(self, inst, label=None):
        self.list.append((self.line_counter, label, inst))
        if label: 
            self.label_table[label] = self.line_counter
        self.line_counter += 1

    def lookup(self, label):
        if not self.label_table[label]: raise Exception(f'Label {label} not found')
        return self.label_table[label]
    
    def print(self):
        print(f'{'line':5}{'label':10}instruction')
        for line, label, inst in self.list:
            print(f'{line:<5}{(label if label else ''):<10}{inst.to_string()}')

# Code Emitter class
class CodeEmitter:
    def __init__(self, prefix='$'):
        self.code_list = CodeList()
        self.tempvar_prefix = prefix
        self.tempvar_counter = 0
        self.label_counter = 0
        self.available_tempvar_name = []

    def emit(self, inst, label=None):
        self.code_list.insert(inst, label)

    def code(self):
        return self.code_list
    
    def get_new_label(self):
        label = self.tempvar_prefix + 'l' + str(self.label_counter)
        self.label_counter += 1
        return label
    
    def get_tempvar_name(self):
        if len(self.available_tempvar_name):
            return self.available_tempvar_name.pop()
        varname = self.tempvar_prefix + str(self.tempvar_counter)
        self.tempvar_counter += 1
        return varname
    
    def free_tempvar_name(self, name):
        if isinstance(name, list): self.available_tempvar_name += name
        else: self.available_tempvar_name.append(name)
    
    def get_procentry_label(self, proc):
        return f'{proc.name_in_array()}.ent'
    
    def get_procbegin_label(self, proc):
        return f'{proc.name_in_array()}.beg'
    
    def get_procend_label(self, proc):
        return f'{proc.name_in_array()}.end'