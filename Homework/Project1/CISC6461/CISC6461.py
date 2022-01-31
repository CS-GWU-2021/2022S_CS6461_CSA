from tkinter import *

'''
Under Construction
'''

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

        # widget can take all window
        self.pack(fill=BOTH, expand=1)

        # create button, link it to clickExitButton()
        exitButton = Button(self, text="Exit", command=self.clickExitButton)

        # place button at (0,0)
        exitButton.place(x=0, y=0)

        # create a text, and place it
        text = Label(self, text="Just do it")
        text.place(x=70,y=90)

    def clickExitButton(self):
        exit()

# initialize tkinter
root = Tk()
app = Window(root)

# set window feature
root.wm_title("CSCI6461")
root.wm_geometry("800x450")

# show window
root.mainloop()

