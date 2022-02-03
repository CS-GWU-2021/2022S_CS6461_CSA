#------------------------------------------------------
# @Author:      Tenphun0503
# this file contains the class of memory
#------------------------------------------------------

class Memory:
    def __init__(self):
        self.size = 2048
        self.memory = ['0'] * self.size

    def memory_expansion(self):
        self.size = 4096
        self.memory = ['0'] * self.size

    def get_from_memory(self, address):
        return self.memory[address]

    def set_to_memory(self, address, value):
        self.memory[address] = value

    def reset_memory(self):
        self.memory = ['0'] * self.size