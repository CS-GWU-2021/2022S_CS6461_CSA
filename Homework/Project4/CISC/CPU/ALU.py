# -----------------------------------------------------------------
# @Author :     Tenphun0503
# This file implements ALU
# -----------------------------------------------------------------
from CPU.registers import *


class ALU:
    def __init__(self, cc):
        self.irr = Register(16, 'IRR')
        self.value = 0
        self.cc = cc

    def reset(self):
        self.irr = Register(16, 'IRR')
        self.value = 0

    def arithmetic_cal(self, operation: str, o1: str, o2: str):
        """This function does arithmetic calculation
        operation can be one of:
        '+', '-', '*', '/', '%'
        """
        self.reset()
        o1_value = int(o1, 2)
        o2_value = int(o2, 2)
        if operation == '+':
            self.value = o1_value + o2_value
        elif operation == '-':
            self.value = o1_value - o2_value
        elif operation == '*':
            self.irr.size = 32
            self.value = o1_value * o2_value
        elif operation == '/':
            self.value = int(o1_value / o2_value)
        elif operation == '%':
            self.value = o1_value % o2_value
        # check OVERFLOW or UNDERFLOW
        state = self.irr.add_10(self.value)
        self.cc.set_state(state)
        return self.irr.value

    def logic_cal(self, operation: str, o1: str, o2=''):
        """This function does logical calculation
        operation can be one of:
        '&', '|', '~'
        """
        self.reset()
        if operation == '&':
            self.value = int(o1, 2) & int(o2, 2)
        elif operation == '|':
            self.value = int(o1, 2) | int(o2, 2)
        elif operation == '~':
            # self.value = ~ o1_value
            value = []
            for i in list(o1):
                if i == '1':
                    value.append('0')
                else:
                    value.append('1')
            value = ''.join(value)
            self.value = int(value, 2)
        # check OVERFLOW or UNDERFLOW
        state = self.irr.add_10(self.value)
        self.cc.set_state(state)
        return self.irr.value

    def shift(self, value: str, count, l_r, a_l):
        """This function does shift"""
        self.reset()
        # left
        if l_r == 1:
            temp = '0' * count
            value += temp
        # right
        else:
            # logically
            if a_l == 1:
                temp = '0' * count
                length = len(value)
                value = temp + value
                value = value[:length]
            # arithmetically
            else:
                temp = value[0] * count
                length = len(value)
                value = temp + value
                value = value[:length]
        self.value = int(value, 2)
        state = self.irr.add_10(self.value)
        self.cc.set_state(state)
        return self.irr.value

    def rotate(self, value: str, count, l_r, a_l):
        """This function does rotate"""
        self.reset()
        temp = value
        print(temp)
        while count > 0:
            # logically
            if a_l == 1:
                # left
                if l_r == 1:
                    temp = value[1:] + value[0]
                # right
                else:
                    temp = value[-1] + value[:-1]
            value = temp
            count -= 1
            print(count, value)
        print(value)
        self.value = int(value, 2)
        state = self.irr.add_10(self.value)
        self.cc.set_state(state)
        return self.irr.value

    def fp_cal(self, operation: str, o1: str, o2: str):
        self.reset()
        fp1 = FPR()
        fp2 = FPR()
        fp1.value = o1
        fp2.value = o2.zfill(16)
        v1 = fp1.update()
        v2 = fp2.update()
        print('fp_cal', v1, v2)
        if operation == '+':
            self.value = v1 + v2
        elif operation == '-':
            self.value = v1 - v2
        self.irr.value = fp1.encode(self.value)
        return self.irr.value
