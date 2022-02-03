import tkinter
from GUI import *
from CPU.registers import *
from memory import *
import tools

if __name__ == '__main__':
    # initialize memory
    mem = Memory()

    # initialize registers
    pc = PC()
    mar = MAR()
    mbr = MBR()
    ir = IR()
    mfr = MFR()
    gpr0 = GPR(label='GPR0')
    gpr1 = GPR(label='GPR1')
    gpr2 = GPR(label='GPR2')
    gpr3 = GPR(label='GPR3')
    x1 = IXR(label='IXR1')
    x2 = IXR(label='IXR2')
    x3 = IXR(label='IXR3')

    # initialize tkinter
    window = Tk()
    registers = []
    app = Window(window, gpr0, gpr1, gpr2, gpr3, x1, x2, x3, pc, mar, mbr, ir, mfr, mem)

    # show window
    window.mainloop()
