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
        self.opcode = []
        self.dict_opcode = {0 : 'HLT', 1 : 'LDR', 2 : 'STR', 3 : 'LDA',
                            4 : 'AMR', 5 : 'SMR', 6 : 'AIR', 7 : 'SIR',
                            8 : 'JZ', 9 : 'JNE', 10 : 'JCC', 11 : 'JMA',
                            12 : 'JSR', 13 : 'RFS', 14 : 'SOB', 15 : 'JGE',
                            16 : 'MLT', 17 : 'DVD', 18 : 'TRR', 19 : 'AND',
                            20 : 'ORR', 21 : 'NOT', 24 : 'TRAP', 25 : 'SRC',
                            26 : 'RRC', 33 : 'LDX', 34 : 'STX', 49 : 'IN',
                            50 : 'OUT'}
        self.dict_opcode.setdefault(0, 'HLT')
        self.gpr_index = []
        self.ixr_index = []
        self.indirect = []
        self.address = []

        self.rx = []
        self.ry = []

        self.a_l = []
        self.l_r = []
        self.count = []

        self.__update()

    def __update(self):
        """This function decodes the instruciton and can be used to refresh the values
        """
        self.opcode = self.value[:6]
        opcode_value = int(self.opcode,2)
        # Arithmetic and Logical Instructions (Register to Register)
        if opcode_value in [16, 17, 18, 19, 20, 21]:
            self.rx = self.value[6:8]
            self.ry = self.value[8:10]
        # Shift/Rotate Instructions
        elif opcode_value in [25, 26]:
            self.gpr_index = self.value[6:8]
            self.a_l = self.value[8]
            self.l_r = self.value[9]
            self.count = self.value[12:]
        else:
            self.gpr_index = self.value[6:8]
            self.ixr_index = self.value[8:10]
            self.indirect = self.value[10]
            self.address = self.value[11:]

    def reset(self):
        self.value = '0' * 16
        self.__update()

    def print_out(self):
        """This function translates the instruction and prints it out at the Step_info
        """
        opcode_value = int(self.opcode,2)
        word = self.dict_opcode[int(self.opcode,2)] + ' '
        # Halt
        if opcode_value == 0:
            word += '0'
        # Arithmetic and Logical Instructions (Register to Register)
        elif opcode_value in [16, 17, 18, 19, 20, 21]:
            word += str(int(self.rx,2)) + ' '
            word += str(int(self.ry,2)) + ' '
        # Shift/Rotate Instructions
        elif opcode_value in [25, 26]:
            word += str(int(self.gpr_index,2)) + ' '
            word += self.a_l + ' '
            word += self.l_r + ' '
        else:
            word += str(int(self.gpr_index,2)) + ' '
            word += str(int(self.ixr_index,2)) + ' '
            word += self.indirect + ' '
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
