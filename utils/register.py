# Register base class
class Register:
    def __init__(self):
        pass

    def is_system_reg(self):
        return False
    
    def is_user_reg(self):
        return False
    
    def to_string(self):
        return 'undefined register type'

# Register classes
class SystemReg(Register):
    def __init__(self, name):
        self.name = name

    def is_system_reg(self):
        return True
    
    def to_string(self):
        return self.name
    
class UserReg(Register):
    def __init__(self, index):
        self.index = index

    def is_user_reg(self):
        return True
    
    def to_string(self):
        return f'r{self.index}'
    
# Register Handler class
class RegisterHandler:
    def __init__(self):
        self.init_system_regs()
        self.user_regs = []
        self.user_counter = 0

    def init_system_regs(self):
        self.pc = SystemReg('pc')
        self.br = SystemReg('br')
        self.ins = SystemReg('ins')
        self.ro = SystemReg('ro')
        self.sp = SystemReg('sp')
        self.qifv = SystemReg('qifv')
        self.qifw = SystemReg('qifw')
        self.wait = SystemReg('wait')

    def clear_user_reg(self, reg):
        self.user_regs.append(reg)

    def get_user_reg(self):
        if len(self.user_regs): return self.user_regs.pop()
        self.user_counter += 1
        return UserReg(self.user_counter)