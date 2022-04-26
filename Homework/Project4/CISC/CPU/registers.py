# -----------------------------------------------------------------
# @Author :     Tenphun0503
# This file contains all the needed registers class
# PC MAR MBR IR CC MFR GPR IXR
# -----------------------------------------------------------------
class Register:
    """This class is the super class of all of registers
    Parameters:
    --------------
    size : int type; the size of the register
    value: str type; the value of the register
    label: str type; the kind of the register
    """

    def __init__(self, size=4, label='register'):
        self.size = size
        self.value = '0' * self.size
        self.label = label

    def check_state(self, input_value):
        """This function checks if the value cause fault"""
        max_value = int('1' * self.size, 2)
        min_value = int('0' * self.size, 2)
        if input_value > max_value:
            return 'OVERFLOW'
        elif input_value < min_value:
            return 'UNDERFLOW'
        else:
            return '0000'

    def add_10(self, adder: int):
        """This function adds value and return the state of the register
        Parameters:
        ------------
        adder: the decimal number that going to be added to
        """
        value = int(self.value, 2) + adder
        if value >= 0:
            temp = bin(value)[2:].zfill(self.size)
        else:
            temp = bin(value)[3:].zfill(self.size)
        state = self.check_state(value)
        self.value = str(int(temp[-self.size:]))
        return state

    def get_value(self):
        """Return str type of decimal value"""
        return str(int(self.value, 2))

    def reset(self):
        """This function resets the register"""
        self.value = '0' * self.size


class PC(Register):
    """This is the class of Program Counter
    PC has 12 bits
    """

    def __init__(self, size=12, label='PC'):
        super().__init__(size=size, label=label)

    def next(self):
        """This function defines how pc find the next instruction"""
        self.add_10(1)


class MAR(Register):
    """This is the class of Memory Address Register
    MAR has 12 bits

    Function:
    ------------
    get_from_PC
    """

    def __init__(self, size=12, label='MAR'):
        super().__init__(size=size, label=label)

    def get_from_PC(self, pc: PC):
        """The function for MAR <- PC
        """
        self.value = pc.value


class MBR(Register):
    """This is the class of Memory Buffer Register
    MBR has 16 bits
    """

    def __init__(self, size=16, label='MBR'):
        super().__init__(size=size, label=label)


class IR(Register):
    """This is the class of Instruction Register
    IR has 16 bits
    """

    def __init__(self, size=16, label='IR'):
        super().__init__(size=size, label=label)

    def get_from_MBR(self, mbr: MBR):
        """The function for IR <- MBR
        """
        self.value = mbr.value


class CC(Register):
    """This is the class of Condition Code
    CC has 4 bits
    """

    def __init__(self, size=4, label='CC'):
        super().__init__(size=size, label=label)
        self.state = '0000'

    def reset(self):
        self.value = '0' * self.size
        self.state = '0000'

    def set_state(self, state: str):
        self.reset()
        self.state = state
        value = list(self.value)
        if state == 'OVERFLOW':
            value[0] = '1'
        elif state == 'UNDERFLOW':
            value[1] = '1'
        elif state == 'DIVZERO':
            value[2] = '1'
        elif state == 'EQUALORNOT':
            value[3] = '1'
        self.value = ''.join(value)


class MFR(Register):
    """This is the class of Memory Fault Register
    MFR has 4 bits
    """

    def __init__(self, size=4, label='MFR'):
        super().__init__(size=size, label=label)


class GPR(Register):
    """This is the class of General Purpose Register
    GPR has 16 bits
    """

    def __init__(self, size=16, label='GPR'):
        super().__init__(size=size, label=label)


class IXR(Register):
    """This is the class of Index Register
    IXR has 16 bits
    """

    def __init__(self, size=16, label='IXR'):
        super().__init__(size=size, label=label)


class FPR(Register):
    """This is the class of Floating Point Register
    FPR has 4 bits
    """

    def __init__(self, size=16, label='FPR'):
        super().__init__(size=size, label=label)
        self.s = None
        self.e = None
        self.m = None

    def reset(self):
        self.value = '0' * self.size
        self.s = None
        self.e = None
        self.m = None

    def update(self):
        print('update', self.value)
        self.s = int(self.value[0], 2)
        self.e = int(self.value[1:8], 2) - 63
        self.m = 1
        for id, i in enumerate(self.value[8:]):
            self.m += int(i) * (1 / (2 ** (id + 1)))
        value = ((-1) ** self.s) * self.m * (2 ** self.e)
        print('update', self.s, self.e, self.m)
        return value

    def encode(self, value):
        if value >= 0:
            self.s = 0
        else:
            self.s = 1
        self.e = 0
        self.m = abs(value)
        while self.m >= 2:
            self.m = self.m / 2
            self.e += 1
        while self.m < 1:
            self.m = self.m * 2
            self.e -= 1
        print('encode', self.s, self.e, self.m)
        s = str(self.s)
        e = bin(self.e + 63)[2:].zfill(7)
        m = self.m - 1
        temp = ''
        for i in range(8):
            m *= 2
            if m >= 1:
                temp += '1'
                m -= 1
            else:
                temp += '0'
        m = temp
        return s + e + m

    def convert(self, value):

        if value >= 0:
            self.s = '0'
        else:
            self.s = '1'
        self.e = bin(int(value))[2:].zfill(7)
        temp = ''
        remain = value - int(value)
        print('remain', remain)
        for i in range(8):
            remain *= 2
            if remain >= 1:
                temp += '1'
                remain -= 1
            else:
                temp += '0'
        self.m = temp
        print(self.s, self.e, self.m)
        return self.s + self.e + self.m

    def reverse_convert(self, value):
        self.s = int(value[0])
        self.e = int(value[1:8], 2)
        self.m = 0
        for id, i in enumerate(value[8:]):
            if i == '1':
                self.m += int(i) * (1 / (2 ** (id + 1)))
        value = ((-1) ** self.s) * (self.m + self.e)
        return value

