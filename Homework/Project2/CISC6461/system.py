from GUI import *
from CPU.registers import *
from memory import *
from instruction import *
import tools

class System:
    def __init__(self):
        # initialize memory
        self.mem = Memory()
        # initialize an instruction object
        self.ins = Instruction()
        # initialize registers
        self.pc = PC()
        self.mar = MAR()
        self.mbr = MBR()
        self.ir = IR()
        self.mfr = MFR()
        self.gpr0 = GPR(label='GPR0')
        self.gpr1 = GPR(label='GPR1')
        self.gpr2 = GPR(label='GPR2')
        self.gpr3 = GPR(label='GPR3')
        self.x1 = IXR(label='IXR1')
        self.x2 = IXR(label='IXR2')
        self.x3 = IXR(label='IXR3')

    def fetch(self):
        pass

    def decode(self):
        pass

    def execute(self):
        pass

    def deposit(self):
        pass
