import tkinter
from GUI import *
from system import System

if __name__ == '__main__':
    # initialize the system
    sys = System()

    # initialize a tkinter window
    window = Tk()
    app = Window(window, sys)

    # show window
    window.mainloop()
