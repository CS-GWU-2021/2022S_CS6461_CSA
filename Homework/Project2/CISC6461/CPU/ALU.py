#-----------------------------------------------------------------
# @Author :     Tenphun0503
# This file implements ALU
#-----------------------------------------------------------------
from CPU.registers import *
from memory import *

class ALU:
    def __init__(self):
        self.irr = Register(16, 'IRR')

    def arithmetic_cal(self, operation : str, o1 : str, o2 : str):
        """This function do arithmetic calculation
        operation can be one of:
        '+', '-', '*', '/', '%'
        """
        self.irr.reset()
        o1_value = int(o1,2)
        o2_value = int(o2,2)
        if operation == '+':
            value = o1_value + o2_value
            self.irr.add_10(value)
        elif operation == '-':
            value = o1_value - o2_value
            self.irr.add_10(value)
        elif operation == '*':
            value = o1_value * o2_value
            self.irr.add_10(value)
        elif operation == '/':
            value = o1_value / o2_value
            self.irr.add_10(value)
        elif operation == '%':
            value = o1_value % o2_value
            self.irr.add_10(value)
        return self.irr.value
