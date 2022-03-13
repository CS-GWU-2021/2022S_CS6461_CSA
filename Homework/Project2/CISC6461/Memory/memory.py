#------------------------------------------------------
# @Author:      Tenphun0503
# this file contains the class of memory
#------------------------------------------------------
class Memory:
    """This is the class for Memory:
    Parameters:
    --------------
    size : int type; the size of the memory
    memory: str_list type: the space to store value
    """
    def __init__(self):
        self.size = 2048
        self.memory = ['0'] * self.size

    def reset(self):
        self.memory = ['0'] * self.size

    def memory_expansion(self):
        """If it is needed, memory size can be expanded to 4096
        """
        self.size = 4096
        self.memory = ['0'] * self.size

    def get_from_memory(self, address):
        return self.memory[address]

    def set_to_memory(self, address, value):
        self.memory[address] = value

    def get_value(self, address):
        """This function is for Step_info
        it returns string type of decimal values
        """
        address = int(address,2)
        return str(int(self.memory[address],2))

    def print_out(self):
        word = '\n-------------MEMORY--------------\n'
        for i, line in enumerate(self.memory):
            word += str(i) + ':\t' + str(int(line)) + '\n'
        return word
