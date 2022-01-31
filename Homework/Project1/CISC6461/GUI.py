from tkinter import *

'''
Under Construction
'''

class Window(Frame):
    def __init__(self, master=None):
        #Frame.__init__(self, master)
        self.master = master

    # Interface layout
    def set_window(self):
        self.master.title('CSCI6461')
        self.master.geometry('1600x900')
        self.master.minsize(1200,750)
        #self.master["bg"] = "SteelBlue"  

        self.master.grid_columnconfigure(0,weight=1, minsize=1200)
        self.master.grid_rowconfigure(0,weight=0, minsize=350)
        self.master.grid_rowconfigure(1,weight=0, minsize=120)
        self.master.grid_rowconfigure(2,weight=0, minsize=100)
        self.master.grid_rowconfigure(3,weight=1)


        # Frame1
        self.frame1 = Frame(self.master, bd=2, relief=RIDGE,padx=10,pady=10)
        self.frame1.grid(row=0,column=0,sticky=W+E,padx=10,pady=10)
        
        self.frame1.grid_columnconfigure(1,weight=1, minsize=50)
        self.frame1.grid_columnconfigure(4,weight=1, minsize=50)
        self.frame1.grid_rowconfigure(0,weight=1, minsize=40)
        self.frame1.grid_rowconfigure(1,weight=1, minsize=40)
        self.frame1.grid_rowconfigure(2,weight=1, minsize=40)
        self.frame1.grid_rowconfigure(3,weight=1, minsize=40)
        self.frame1.grid_rowconfigure(4,weight=1, minsize=40)
        self.frame1.grid_rowconfigure(5,weight=1, minsize=40)
        self.frame1.grid_rowconfigure(6,weight=1, minsize=40)

        # label
        label_GPR0 = Label(self.frame1, text='GPR0').grid(row=0,column=0)
        label_GPR1 = Label(self.frame1, text="GPR1").grid(row=1,column=0)
        label_GPR2 = Label(self.frame1, text="GPR2").grid(row=2,column=0)
        label_GPR3 = Label(self.frame1, text="GPR3").grid(row=3,column=0)
        label_IXR1 = Label(self.frame1, text="IXR1").grid(row=4,column=0)
        label_IXR2 = Label(self.frame1, text="IXR2").grid(row=5,column=0)
        label_IXR3 = Label(self.frame1, text="IXR3").grid(row=6,column=0)

        label_PC = Label(self.frame1, text="PC").grid(row=0,column=3)
        label_MAR = Label(self.frame1, text="MAR").grid(row=1,column=3)
        label_MBR = Label(self.frame1, text="MBR").grid(row=2,column=3)
        label_IR = Label(self.frame1, text="IR").grid(row=3,column=3)
        label_MFR = Label(self.frame1, text="MFR").grid(row=4,column=3)

        # text
        txt_GPR0 = Label(self.frame1, text='0000', relief=RIDGE).grid(row=0,column=1,sticky=W+E)
        txt_GPR1 = Label(self.frame1, text='0000', relief=RIDGE).grid(row=1,column=1,sticky=W+E)
        txt_GPR2 = Label(self.frame1, text='0000', relief=RIDGE).grid(row=2,column=1,sticky=W+E)
        txt_GPR3 = Label(self.frame1, text='0000', relief=RIDGE).grid(row=3,column=1,sticky=W+E)
        txt_IXR1 = Label(self.frame1, text='0000', relief=RIDGE).grid(row=4,column=1,sticky=W+E)
        txt_IXR2 = Label(self.frame1, text='0000', relief=RIDGE).grid(row=5,column=1,sticky=W+E)
        txt_IXR3 = Label(self.frame1, text='0000', relief=RIDGE).grid(row=6,column=1,sticky=W+E)

        txt_PC = Label(self.frame1, text='0000', relief=RIDGE).grid(row=0,column=4,sticky=W+E)
        txt_MAR = Label(self.frame1, text='0000', relief=RIDGE).grid(row=1,column=4,sticky=W+E)
        txt_MBR = Label(self.frame1, text='0000', relief=RIDGE).grid(row=2,column=4,sticky=W+E)
        txt_IR = Label(self.frame1, text='0000', relief=RIDGE).grid(row=3,column=4,sticky=W+E)
        txt_MFR = Label(self.frame1, text='0000', relief=RIDGE).grid(row=4,column=4,sticky=W+E)

        # button
        btn_GPR0 = Button(self.frame1, text='LD').grid(row=0,column=2)
        btn_GPR1 = Button(self.frame1, text='LD').grid(row=1,column=2)
        btn_GPR2 = Button(self.frame1, text='LD').grid(row=2,column=2)
        btn_GPR3 = Button(self.frame1, text='LD').grid(row=3,column=2)
        btn_IXR1 = Button(self.frame1, text='LD').grid(row=4,column=2)
        btn_IXR2 = Button(self.frame1, text='LD').grid(row=5,column=2)
        btn_IXR3 = Button(self.frame1, text='LD').grid(row=6,column=2)

        btn_PC = Button(self.frame1, text='LD').grid(row=0,column=5)
        btn_MAR = Button(self.frame1, text='LD').grid(row=1,column=5)
        btn_MBR = Button(self.frame1, text='LD').grid(row=2,column=5)


        # Frame2
        self.frame2 = Frame(self.master, bd=2, relief=RIDGE, padx=10,pady=10)
        self.frame2.grid(row=1,column=0,sticky=W+E,padx=10,pady=10)

        self.frame2.grid_columnconfigure(0,weight=1, minsize=20)
        self.frame2.grid_columnconfigure(1,weight=1, minsize=20)
        self.frame2.grid_columnconfigure(2,weight=1, minsize=20)
        self.frame2.grid_columnconfigure(3,weight=1, minsize=20)
        self.frame2.grid_columnconfigure(4,weight=1, minsize=20)
        self.frame2.grid_columnconfigure(5,weight=1, minsize=20)
        self.frame2.grid_columnconfigure(6,weight=1, minsize=20)
        self.frame2.grid_columnconfigure(7,weight=1, minsize=20)
        self.frame2.grid_columnconfigure(8,weight=1, minsize=20)
        self.frame2.grid_columnconfigure(9,weight=1, minsize=20)
        self.frame2.grid_columnconfigure(10,weight=1, minsize=20)
        self.frame2.grid_columnconfigure(11,weight=1, minsize=20)
        self.frame2.grid_columnconfigure(12,weight=1, minsize=20)
        self.frame2.grid_columnconfigure(13,weight=1, minsize=20)
        self.frame2.grid_columnconfigure(14,weight=1, minsize=20)
        self.frame2.grid_columnconfigure(15,weight=1, minsize=20)
        self.frame2.grid_rowconfigure(0,weight=1, minsize=30)
        self.frame2.grid_rowconfigure(1,weight=1, minsize=40)
        self.frame2.grid_rowconfigure(2,weight=1, minsize=40)

        # label
        label_Operation = Label(self.frame2, text='Operation').grid(row=0,column=0,columnspan=6)
        label_GPR = Label(self.frame2, text='GPR').grid(row=0,column=6,columnspan=2)
        label_IXR = Label(self.frame2, text='IXR').grid(row=0,column=8,columnspan=2)
        label_I = Label(self.frame2, text='I').grid(row=0,column=10)
        label_Address = Label(self.frame2, text='Address').grid(row=0,column=11,columnspan=5)

        # text
        txt_Operation = Label(self.frame2, text='000000', relief=RIDGE).grid(row=1,column=0,columnspan=6,sticky=W+E)
        txt_GPR = Label(self.frame2, text='000000', relief=RIDGE).grid(row=1,column=6,columnspan=2,sticky=W+E)
        txt_IXR = Label(self.frame2, text='000000', relief=RIDGE).grid(row=1,column=8,columnspan=2,sticky=W+E)
        txt_I = Label(self.frame2, text='00000', relief=RIDGE).grid(row=1,column=10,sticky=W+E)
        txt_Address = Label(self.frame2, text='00000', relief=RIDGE).grid(row=1,column=11,columnspan=5,sticky=W+E)

        # button
        btn_width=5
        btn_Ope0 = Button(self.frame2, text='0',width=btn_width).grid(row=2,column=0)
        btn_Ope1 = Button(self.frame2, text='1',width=btn_width).grid(row=2,column=1)
        btn_Ope2 = Button(self.frame2, text='2',width=btn_width).grid(row=2,column=2)
        btn_Ope3 = Button(self.frame2, text='3',width=btn_width).grid(row=2,column=3)
        btn_Ope4 = Button(self.frame2, text='4',width=btn_width).grid(row=2,column=4)
        btn_Ope5 = Button(self.frame2, text='5',width=btn_width).grid(row=2,column=5)
        btn_GPR6 = Button(self.frame2, text='6',width=btn_width).grid(row=2,column=6)
        btn_GPR7 = Button(self.frame2, text='7',width=btn_width).grid(row=2,column=7)
        btn_IXR8 = Button(self.frame2, text='8',width=btn_width).grid(row=2,column=8)
        btn_IXR9 = Button(self.frame2, text='9',width=btn_width).grid(row=2,column=9)
        btn_I10 = Button(self.frame2, text='10',width=btn_width).grid(row=2,column=10)
        btn_Add11 = Button(self.frame2, text='11',width=btn_width).grid(row=2,column=11)
        btn_Add12 = Button(self.frame2, text='12',width=btn_width).grid(row=2,column=12)
        btn_Add13 = Button(self.frame2, text='13',width=btn_width).grid(row=2,column=13)
        btn_Add14 = Button(self.frame2, text='14',width=btn_width).grid(row=2,column=14)
        btn_Add15 = Button(self.frame2, text='15',width=btn_width).grid(row=2,column=15)


        # Frame3
        self.frame3 = Frame(self.master,padx=10,pady=10)
        self.frame3.grid(row=2,column=0,sticky=E,padx=10)

        # button
        btn_store = Button(self.frame3, text='Store',width=10).grid(row=0,column=0,padx=10,pady=5,sticky=W+E)
        btn_load = Button(self.frame3, text='Load',width=10).grid(row=0,column=1,padx=10,pady=5,sticky=W+E)
        btn_ipl = Button(self.frame3, text='IPL',width=10).grid(row=0,column=2,padx=10,pady=5,sticky=W+E)

        btn_ss = Button(self.frame3, text='SS',width=10).grid(row=1,column=0,padx=10,pady=5,sticky=W+E)
        btn_run = Button(self.frame3, text='Run',width=10).grid(row=1,column=1,padx=10,pady=5,sticky=W+E)
        btn_mem_log = Button(self.frame3, text='Mem Log',width=10).grid(row=1,column=2,padx=10,pady=5,sticky=W+E)

        # Frame4
        self.frame4 = Frame(self.master, bd=2, relief=RIDGE, padx=10,pady=10)
        self.frame4.grid(row=3,column=0,sticky=W+E+N+S,padx=10,pady=10)
        self.frame4.rowconfigure(0,weight=0,minsize=20)
        self.frame4.rowconfigure(1,weight=1,minsize=30)
        self.frame4.columnconfigure(0,weight=1,minsize=50)
        self.frame4.columnconfigure(1,weight=4,minsize=200)

        # label
        label_step_log = Label(self.frame4, text='Step_Log').grid(row=0,column=0,sticky=W+S+N)
        label_mem_log = Label(self.frame4, text='Mem_Log').grid(row=0,column=1,sticky=W+S+N)

        # text
        txt_step_log = Label(self.frame4,text='Word is fecthed\ndecode the word',justify='left',anchor='nw',relief=RIDGE).grid(row=1,column=0,sticky=W+E+S+N)
        txt_mem_log = Label(self.frame4,text='GPR0: 0000101010\nGPR1: 0000000000',justify='left',anchor='nw',relief=RIDGE).grid(row=1,column=1,columnspan=4,sticky=W+E+S+N)

def gui_draw():
    # initialize tkinter
    window = Tk()
    app = Window(window)

    # set layout
    app.set_window()

    # show window
    window.mainloop()

