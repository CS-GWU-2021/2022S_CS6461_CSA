import tkinter
from GUI import *
from system import System

if __name__ == '__main__':

    file_dir = './Programs/program.txt'
    pc_default = 6

    #file_dir = './Programs/program1.txt'
    #pc_default = int('100',16)

    #file_dir = './Programs/ipl.txt'
    #pc_default = int('1010',2)

    # initialize the system
    sys = System(file_dir, pc_default)

    # initialize a tkinter window
    window = Tk()
    app = MainWindow(window, sys)

    # show window
    window.mainloop()
