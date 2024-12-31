from utils.mid_level.label import Label

class CodeList:
    def __init__(self):
        self.list = []

    def code(self):
        return self.list

    def insert(self, inst, label=None):
        self.list.append((label, inst))
    
    def print(self):
        line_counter = 0
        print(f'{'line':5}{'label':10}instruction')
        for label, inst in self.list:
            line_counter += 1
            print(f'{line_counter:<5}{(label.to_string() if label else ''):<10}{inst.to_string()}')

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
        return Label(label)
    
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
        return Label(proc.name(), index=(proc._index.name() if proc._index else ''), suffix='.ent')
    
    def get_procbegin_label(self, proc):
        return Label(proc.name(), index=(proc._index.name() if proc._index else ''), suffix='.beg')
    
    def get_procend_label(self, proc):
        return Label(proc.name(), index=(proc._index.name() if proc._index else ''), suffix='.end')