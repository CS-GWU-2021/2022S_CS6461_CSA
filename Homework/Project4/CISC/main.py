# ---------------------------------------------
# @Author: Tenphun0503
# This is the main script
# ---------------------------------------------
from GUI import *
from system import System

if __name__ == '__main__':
    # initialize the preload program
    file_dir = 'program3.txt'
    text_dir = 'test.txt'
    pc_default = 6

    # initialize the system
    sys = System(file_dir, pc_default, text_dir)

    # initialize a tkinter window
    window = Tk()
    app = MainWindow(window, sys)

    # show window
    window.mainloop()