#-----------------------------------------------------------------
# @Author :     Tenphun0503
# This file contains all of the needed registers class
# PC MAR MBR IR CC MFR GPR IXR
#-----------------------------------------------------------------
from memory import *

class Register:
    """This class is the super class of all of registers
    Parameters:
    --------------
    size : int type; the size of the register
    value: str type; the value of the register
    label: str type; the kind of the register
    """
    def __init__(self, size=0, label=''):
        self.size = size
        self.value = '0' * self.size
        self.label = label

    def check_overflow(self, input_value) -> bool:
        """This function returns True when register overflows
        Parameters:
        ------------
        input_value: str type; input value
        """
        return True if len(input_value) > self.size else False

    def add_2(self, adder : str):
        """This function adds a binary value to the register
        Parameters:
        ------------
        adder: the binary number that going to be added to
        """
        temp = bin(int(self.value,2) + int(adder,2))[2:]
        if self.check_overflow(temp) != True:
            self.value = temp
        else:
            print(self.label + ' overflow error')

    def add_10(self, adder : int):
        """This function adds a decimal value to the register
        Parameters:
        ------------
        adder: the decimal number that going to be added to
        """
        temp = bin(int(self.value,2) + adder)[2:]
        if self.check_overflow(temp) != True:
            self.value = temp
        else:
            print(self.label + ' overflow error')

    def reset(self):
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

    def get_from_PC(self, pc : PC):
        """The function for MAR <- PC
        """
        self.value = pc.value

class MBR(Register):
    """This is the class of Memory Buffer Register
    MBR has 16 bits
    """
    def __init__(self, size=16, label='MBR'):
        super().__init__(size=size, label=label)

    def load_from_mem(self, mar : MAR, mem : Memory):
        """The function for MBR <- MEM[MAR]
        """
        address = int(''.join(mar.value),2)
        self.value = mem.get_from_memory(address)

    def store_to_mem(self, mar : MAR, mem : Memory):
        """The function for MEM[MAR] <- MBR
        """
        address = int(''.join(mar.value),2)
        mem.set_to_memory(address,self.value)

class IR(Register):
    """This is the class of Instruction Register
    IR has 16 bits
    """
    def __init__(self, size=16, label='IR'):
        super().__init__(size=size, label=label)

    def get_from_MBR(self, mbr : MBR):
        """The function for IR <- MBR
        """
        self.value = mbr.value

class CC(Register):
    """This is the class of Condition Code
    CC has 4 bits
    """
    def __init__(self, size=4, label='CC'):
        super().__init__(size=size, label=label)

class MFR(Register):
    """This is the class of Memory Falut Register
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
