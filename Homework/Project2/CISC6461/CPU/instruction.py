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

        self.dict_opcode = {1 : 'LDR', 2 : 'STR', 3 : 'LDA',
                            4 : 'AMR', 5 : 'SMR', 6 : 'AIR', 7 : 'SIR',
                            8 : 'JZ', 9 : 'JNE', 10 : 'JCC',
                            11 : 'JMA', 12 : 'JSR', 13 : 'RFS',
                            14 : 'SOB', 15 : 'JGE',
                            33 : 'LDX', 34 : 'STX'}
        self.dict_opcode.setdefault(0, 'HLT')

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
        word = self.dict_opcode[int(self.opcode,2)] + ' '
        word += str(int(self.gpr_index,2)) + ' '
        word += str(int(self.ixr_index,2)) + ' '
        word += str(int(self.indirect,2)) + ' '
        word += str(int(self.address,2))
        return word

    def decode_test(self, ins_test):
        dict = {str:num for num,str in self.dict_opcode.items()}
        if len(ins_test.split(' ')) != 5:
            print('Wrong Number of args')
            return 'NUMERROR'
        self.opcode, self.gpr_index, self.ixr_index, self.indirect, self.address = ins_test.split(' ')
        if self.opcode not in dict.keys():
            print("Wrong Operation")
            return 'OPERROR'
        if int(self.gpr_index) not in [0,1,2,3]:
            print("Wrong Gpr")
            return 'GPRERROR'
        if int(self.ixr_index) not in [0,1,2,3]:
            print("Wrong IXR")
            return 'IXRERROR'
        if int(self.indirect) not in [0,1]:
            print("Wrong Indirect")
            return 'IERROR'
        self.opcode = bin(dict[self.opcode])[2:]
        self.gpr_index = bin(int(self.gpr_index))[2:]
        self.ixr_index = bin(int(self.ixr_index))[2:]
        self.indirect = bin(int(self.indirect))[2:]
        self.address = bin(int(self.address))[2:]
