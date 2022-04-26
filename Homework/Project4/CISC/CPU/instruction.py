# -------------------------------------------------------
# @Author:      Tenphun0503 & Jimmy;
# this file contains the class of instruction
# ------------------------------------------------------
class Instruction:
    """This is the class for Instruction:
    Parameters:
    --------------
    value : str type; the whole instruction
    opcode/gpr_index/ixr_index/indirect/address:
    str type; each part of the instruction
    """

    def __init__(self, value='0' * 16):
        if len(value) < 16:
            value = value.zfill(16)
        self.value = value
        self.dict_opcode = {0: 'HLT', 1: 'LDR', 2: 'STR', 3: 'LDA', 4: 'AMR',
                            5: 'SMR', 6: 'AIR', 7: 'SIR', 8: 'JZ', 9: 'JNE',
                            10: 'JCC', 11: 'JMA', 12: 'JSR', 13: 'RFS', 14: 'SOB',
                            15: 'JGE', 16: 'MLT', 17: 'DVD', 18: 'TRR', 19: 'AND',
                            20: 'ORR', 21: 'NOT', 24: 'TRAP', 25: 'SRC', 26: 'RRC',
                            27: 'FADD', 28: 'FSUB', 29: 'VADD', 30: 'VSUB', 31: 'CNVRT',
                            33: 'LDX', 34: 'STX', 40: 'LDFR', 41: 'STFR', 49: 'IN', 50: 'OUT', 51: 'CHK'}
        self.dict_opcode.setdefault(0, 'HLT')
        # general operations
        self.opcode = None
        self.gpr_index = None
        self.fpr_index = None
        self.ixr_index = None
        self.indirect = None
        self.address = None
        # Arithmetic and Logical Instructions (Register to Register)
        self.rx = None
        self.ry = None
        # Shift/Rotate Instructions
        self.a_l = None
        self.l_r = None
        self.count = None
        # Trap Code
        self.trap_code = None

        self.update()

    def update(self):
        """This function decodes the instruction and can be used to refresh the values
        """
        self.opcode = self.value[:6]
        opcode_value = int(self.opcode, 2)
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
        # Trap Code
        elif opcode_value == 24:
            self.trap_code = self.value[12:]
        # FP and Vector
        elif opcode_value in [27, 28, 29, 30, 31, 40, 41]:
            self.fpr_index = self.value[6:8]
        self.gpr_index = self.value[6:8]
        self.ixr_index = self.value[8:10]
        self.indirect = self.value[10]
        self.address = self.value[11:]

    def reset(self):
        self.value = '0' * 16
        self.update()

    def print_out(self):
        """This function translates the instruction and prints it out at the Step_info
        """
        opcode_value = int(self.opcode, 2)
        word = self.dict_opcode[int(self.opcode, 2)] + ' '
        # Halt
        if opcode_value == 0:
            word += '0'
        # Arithmetic and Logical Instructions (Register to Register)
        elif opcode_value in [16, 17, 18, 19, 20, 21]:
            word += str(int(self.rx, 2)) + ' '
            if opcode_value != 21:
                word += str(int(self.ry, 2)) + ' '
        # Trap
        elif opcode_value == 24:
            word += str(int(self.trap_code, 2)) + ' '
        # Shift/Rotate Instructions
        elif opcode_value in [25, 26]:
            word += str(int(self.gpr_index, 2)) + ' '
            word += self.a_l + ' '
            word += self.l_r + ' '
        # IO
        elif opcode_value in [49, 50, 51]:
            word += str(int(self.gpr_index, 2)) + ' '
            word += str(int(self.address, 2))
        else:
            word += str(int(self.gpr_index, 2)) + ' '
            word += str(int(self.ixr_index, 2)) + ' '
            word += self.indirect + ' '
            word += str(int(self.address, 2))
        return word

    def decode_test(self, ins_test):
        dict = {str: num for num, str in self.dict_opcode.items()}
        ins_test = ins_test.split(' ')
        opcode = ins_test[0]
        num = len(ins_test)
        if opcode not in dict.keys():
            return "Unknown Operation"
        else:
            self.opcode = dict[opcode]

        # Arithmetic and Logical Instructions (Register to Register)
        if self.opcode in [16, 17, 18, 19, 20]:
            if num != 3:
                return opcode + ' needs two paras: ' + opcode + ' rx ry\n'
            else:
                rx = int(ins_test[1])
                ry = int(ins_test[2])
                if rx not in [0, 1, 2, 3]:
                    return "Rx should be 0, 1, 2 or 3\n"
                elif ry not in [0, 1, 2, 3]:
                    return "Ry should be 0, 1, 2 or 3\n"
                else:
                    self.opcode = bin(self.opcode)[2:].zfill(6)
                    self.rx = bin(rx)[2:].zfill(2)
                    self.ry = bin(ry)[2:].zfill(2)
                    self.value = self.opcode + self.rx + self.ry + '000000'
        elif self.opcode == 21:
            if num != 2:
                return opcode + ' needs one para: ' + opcode + ' rx\n'
            else:
                rx = int(ins_test[1])
                if rx not in [0, 1, 2, 3]:
                    return "Rx should be 0, 1, 2 or 3\n"
                else:
                    self.opcode = bin(self.opcode)[2:].zfill(6)
                    self.rx = bin(rx)[2:].zfill(2)
                    self.value = self.opcode + self.rx + '00000000'
        # Shift/Rotate Instructions
        elif self.opcode in [25, 26]:
            if num != 5:
                return opcode + ' needs 4 paras: ' + opcode + ' R Count L/R A/L\n'
            else:
                r, count, l_r, a_l = ins_test[1:]
                if int(r) not in [0, 1, 2, 3]:
                    return "R should be 0, 1, 2 or 3\n"
                elif int(count) < 0 or int(count) > 15:
                    return "Count should be in range of 0:15"
                elif int(l_r) not in [0, 1]:
                    return "L/R should be 0 or 1\n"
                elif int(a_l) not in [0, 1]:
                    return "A/L should be 0 or 1\n"
                else:
                    self.opcode = bin(self.opcode)[2:].zfill(6)
                    self.gpr_index = bin(int(r))[2:].zfill(2)
                    self.count = bin(int(count))[2:].zfill(4)
                    self.l_r = bin(int(l_r))[2:].zfill(1)
                    self.a_l = bin(int(a_l))[2:].zfill(1)
                    self.value = self.opcode + self.gpr_index + self.a_l + self.l_r + '00' + self.count
        # Trap Code
        elif self.opcode == 24:
            if num != 2:
                return f'{opcode} needs 1 para: {opcode} TrapCode\n'
            else:
                trap_code = ins_test[1]
                if int(trap_code) < 0 or int(trap_code) > 15:
                    return "TrapCode should be in range of 0:15"
                else:
                    self.opcode = bin(self.opcode)[2:].zfill(6)
                    self.trap_code = bin(int(trap_code))[2:].zfill(4)
                    self.value = self.opcode + '000000' + self.trap_code
        # IO
        elif self.opcode in [49, 50, 51]:
            if num != 3:
                return opcode + ' needs 2 paras: ' + opcode + ' R DevID\n'
            else:
                r, id = ins_test[1:]
                if int(r) not in [0, 1, 2, 3]:
                    return "R should be 0, 1, 2 or 3\n"
                else:
                    self.opcode = bin(self.opcode)[2:].zfill(6)
                    self.gpr_index = bin(int(r))[2:].zfill(2)
                    self.address = bin(int(id))[2:].zfill(5)
                    self.value = self.opcode + self.gpr_index + '000' + self.address
        else:
            if num != 5:
                msg = opcode + ' needs 4 paras: r  x  i  add\n'
                msg += 'Set 0 if a para is ignored\n'
                return msg
            else:
                r, x, i, add = ins_test[1:]
                if self.opcode in [27, 28, 29, 30, 31, 40, 41]:
                    if int(r) not in [0, 1]:
                        return 'R should be 0 or 1\n'
                if int(r) not in [0, 1, 2, 3]:
                    return 'R should be 0, 1, 2 or 3\n'
                elif int(x) not in [0, 1, 2, 3]:
                    return 'X should be 0, 1, 2 or 3\n'
                elif int(i) not in [0, 1]:
                    return "I should be 0 or 1\n"
                else:
                    self.opcode = bin(self.opcode)[2:].zfill(6)
                    self.gpr_index = bin(int(r))[2:].zfill(2)
                    self.fpr_index = bin(int(r))[2:].zfill(2)
                    self.ixr_index = bin(int(x))[2:].zfill(2)
                    self.indirect = bin(int(i))[2:].zfill(1)
                    self.address = bin(int(add))[2:].zfill(5)
                    self.value = self.opcode + self.gpr_index + self.ixr_index + self.indirect + self.address
        hex_value = hex(int(self.value, 2))[2:]
        print(f'Encoded Instruction: ' + self.value)
        print('' + hex_value.upper().zfill(4) + '')
        return f'Decoding Complete\n\n'
