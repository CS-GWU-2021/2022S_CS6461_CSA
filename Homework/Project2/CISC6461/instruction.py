#-------------------------------------------------------
# @Author:      Tenphun0503 & Jimmy;
# this file contains the class of instruction
#------------------------------------------------------

class Instruction:    
    """This is the class for Instruction:
    Parameters:
    --------------
    value : str type; the whole instruction
    opcode\gpr_index\ixr_index\indirect\address:
    str type; each part of the instruction
    """
    def __init__(self, value = '0' * 16):
        if len(value) < 16:
            value = value.zfill(16)
        self.value = value
        self.update()

    def update(self):
        """This function decodes the instruciton and can be used to refresh the values
        """
        self.opcode = self.value[:6]
        self.gpr_index = self.value[6:8]
        self.ixr_index = self.value[8:10]
        self.indirect = self.value[10:11]
        self.address = self.value[11:]

    def reset(self):
        self.value = '0' * 16
        self.update()

    def print_out(self):
        """This function translates the instruction and prints it out at the Step_info
        """
        dict_opcode = {1 : 'LDR', 2 : 'STR', 3 : 'LDA', 33 : 'LDX', 34 : 'STX'}
        dict_opcode.setdefault(0, 'HLT')
        word = dict_opcode[int(self.opcode,2)] + ' '
        word += str(int(self.gpr_index,2)) + ' '
        word += str(int(self.ixr_index,2)) + ' '
        word += str(int(self.indirect,2)) + ' '
        word += str(int(self.address,2))
        return word