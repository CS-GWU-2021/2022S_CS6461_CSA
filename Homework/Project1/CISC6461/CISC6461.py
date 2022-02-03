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
    gpr0 = GPR()
    gpr1 = GPR()
    gpr2 = GPR()
    gpr3 = GPR()
    x1 = IXR()
    x2 = IXR()
    x3 = IXR()

    # initialize tkinter
    window = Tk()
    app = Window(window, gpr0, gpr1, gpr2, gpr3, x1, x2, x3, pc, mar, mbr, ir, mfr)
    # show window
    window.mainloop()
