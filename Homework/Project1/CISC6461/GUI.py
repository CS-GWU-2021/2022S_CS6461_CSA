from tkinter import *

'''
Under Construction
'''

class Window():
    def __init__(self, master=None):
        self.master = master

        # initialize all of the txt value
        self.value_GPR0 = self.value_GPR1 = self.value_GPR2 = self.value_GPR3 = self.zero_gene(16)
        self.value_IXR1 = self.value_IXR2 = self.value_IXR3 = self.zero_gene(16)
        self.value_PC = self.value_MAR = self.zero_gene(12)
        self.value_MBR = self.value_IR = self.zero_gene(16)
        self.value_MFR = self.zero_gene(4)
        self.value_instruction = self.zero_gene(16)
        self.value_step_info = self.value_mem_info = 'Initialize the app'

        self.instruction = StringVar()

    # Interface layout
    def set_window(self):
        # GUI setting para
        win_title = 'CSCI6461'
        win_size = '1600x900'
        win_min_width = 1200
        win_min_height = 750
        win_color = 'SteelBlue'
        win_margin = 10
        frame_sytle = RIDGE
        text_box_style = RIDGE
        instruction_btn_width=5
        interact_btn_width=10

        # GUI setting
        self.master.title(win_title)
        self.master.geometry(win_size)
        self.master.minsize(win_min_width,win_min_height)
        #self.master["bg"] = win_color  

        # setting layout of main window
        self.master.grid_columnconfigure(0,weight=1, minsize=1200)
        self.master.grid_rowconfigure(0,weight=0, minsize=350)
        self.master.grid_rowconfigure(1,weight=0, minsize=120)
        self.master.grid_rowconfigure(2,weight=0, minsize=100)
        self.master.grid_rowconfigure(3,weight=1)


        # Frame 1
        self.frame1 = Frame(self.master, bd=2, relief=frame_sytle, padx=win_margin, pady=win_margin)
        self.frame1.grid(row=0, column=0, sticky=W+E, padx=win_margin, pady=win_margin)
        
        # setting layout of frame 1
        self.frame1.grid_columnconfigure(1, weight=1, minsize=50)
        self.frame1.grid_columnconfigure(4, weight=1, minsize=50)
        for i in range(0,7):
            self.frame1.grid_rowconfigure(i, weight=1, minsize=40)


        # labels of registers
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

        # text box of registers
        txt_GPR0 = Label(self.frame1, text=self.txt_split(self.value_GPR0), relief=text_box_style).grid(row=0,column=1,sticky=W+E)
        txt_GPR1 = Label(self.frame1, text=self.txt_split(self.value_GPR1), relief=text_box_style).grid(row=1,column=1,sticky=W+E)
        txt_GPR2 = Label(self.frame1, text=self.txt_split(self.value_GPR2), relief=text_box_style).grid(row=2,column=1,sticky=W+E)
        txt_GPR3 = Label(self.frame1, text=self.txt_split(self.value_GPR3), relief=text_box_style).grid(row=3,column=1,sticky=W+E)
        txt_IXR1 = Label(self.frame1, text=self.txt_split(self.value_IXR1), relief=text_box_style).grid(row=4,column=1,sticky=W+E)
        txt_IXR2 = Label(self.frame1, text=self.txt_split(self.value_IXR2), relief=text_box_style).grid(row=5,column=1,sticky=W+E)
        txt_IXR3 = Label(self.frame1, text=self.txt_split(self.value_IXR3), relief=text_box_style).grid(row=6,column=1,sticky=W+E)

        txt_PC = Label(self.frame1, text=self.txt_split(self.value_PC), relief=text_box_style).grid(row=0,column=4,sticky=W+E)
        txt_MAR = Label(self.frame1, text=self.txt_split(self.value_MAR), relief=text_box_style).grid(row=1,column=4,sticky=W+E)
        txt_MBR = Label(self.frame1, text=self.txt_split(self.value_MBR), relief=text_box_style).grid(row=2,column=4,sticky=W+E)
        txt_IR = Label(self.frame1, text=self.txt_split(self.value_IR), relief=text_box_style).grid(row=3,column=4,sticky=W+E)
        txt_MFR = Label(self.frame1,text=self.txt_split(self.value_MFR), relief=text_box_style).grid(row=4,column=4,sticky=W+E)

        # LD button of registers
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
        self.frame2 = Frame(self.master, bd=2, relief=frame_sytle, padx=win_margin, pady=win_margin)
        self.frame2.grid(row=1, column=0, sticky=W+E, padx=win_margin, pady=win_margin)

        # setting layout of frame 1
        for i in range(16):
            self.frame2.grid_columnconfigure(i,weight=1, minsize=20)
        for i in range(3):
            self.frame2.grid_rowconfigure(i,weight=1, minsize=40)

        # label of Instruction
        label_Operation = Label(self.frame2, text='Operation').grid(row=0,column=0,columnspan=6)
        label_GPR = Label(self.frame2, text='GPR').grid(row=0,column=6,columnspan=2)
        label_IXR = Label(self.frame2, text='IXR').grid(row=0,column=8,columnspan=2)
        label_I = Label(self.frame2, text='I').grid(row=0,column=10)
        label_Address = Label(self.frame2, text='Address').grid(row=0,column=11,columnspan=5)

        # text box of Instruction
        txt_Operation = Label(self.frame2, text=self.value_instruction[0:6], textvariable=self.instruction, relief=text_box_style).grid(row=1,column=0,columnspan=6,sticky=W+E)
        txt_GPR = Label(self.frame2, text=self.value_instruction[6:8], relief=text_box_style).grid(row=1,column=6,columnspan=2,sticky=W+E)
        txt_IXR = Label(self.frame2, text=self.value_instruction[8:10], relief=text_box_style).grid(row=1,column=8,columnspan=2,sticky=W+E)
        txt_I = Label(self.frame2, text=self.value_instruction[10:11], relief=text_box_style).grid(row=1,column=10,sticky=W+E)
        txt_Address = Label(self.frame2, text=self.value_instruction[11:16], relief=text_box_style).grid(row=1,column=11,columnspan=5,sticky=W+E)

        # button of Instruction: to set corresponding value to 1 or 0       
        btn_Ope0 = Button(self.frame2, text='0',width=instruction_btn_width, command = self.func_btn_instruction(0)).grid(row=2,column=0)
        btn_Ope1 = Button(self.frame2, text='1',width=instruction_btn_width, command = self.func_btn_instruction(1)).grid(row=2,column=1)
        btn_Ope2 = Button(self.frame2, text='2',width=instruction_btn_width, command = self.func_btn_instruction(2)).grid(row=2,column=2)
        btn_Ope3 = Button(self.frame2, text='3',width=instruction_btn_width, command = self.func_btn_instruction(3)).grid(row=2,column=3)
        btn_Ope4 = Button(self.frame2, text='4',width=instruction_btn_width, command = self.func_btn_instruction(4)).grid(row=2,column=4)
        btn_Ope5 = Button(self.frame2, text='5',width=instruction_btn_width, command = self.func_btn_instruction(5)).grid(row=2,column=5)
        btn_GPR6 = Button(self.frame2, text='6',width=instruction_btn_width, command = self.func_btn_instruction(6)).grid(row=2,column=6)
        btn_GPR7 = Button(self.frame2, text='7',width=instruction_btn_width, command = self.func_btn_instruction(7)).grid(row=2,column=7)
        btn_IXR8 = Button(self.frame2, text='8',width=instruction_btn_width, command = self.func_btn_instruction(8)).grid(row=2,column=8)
        btn_IXR9 = Button(self.frame2, text='9',width=instruction_btn_width, command = self.func_btn_instruction(9)).grid(row=2,column=9)
        btn_I10 = Button(self.frame2, text='10',width=instruction_btn_width, command = self.func_btn_instruction(10)).grid(row=2,column=10)
        btn_Add11 = Button(self.frame2, text='11',width=instruction_btn_width, command = self.func_btn_instruction(11)).grid(row=2,column=11)
        btn_Add12 = Button(self.frame2, text='12',width=instruction_btn_width, command = self.func_btn_instruction(12)).grid(row=2,column=12)
        btn_Add13 = Button(self.frame2, text='13',width=instruction_btn_width, command = self.func_btn_instruction(13)).grid(row=2,column=13)
        btn_Add14 = Button(self.frame2, text='14',width=instruction_btn_width, command = self.func_btn_instruction(14)).grid(row=2,column=14)
        btn_Add15 = Button(self.frame2, text='15',width=instruction_btn_width, command = self.func_btn_instruction(15)).grid(row=2,column=15)
        btn_instruction = [btn_Ope0, btn_Ope1, btn_Ope2, btn_Ope3, btn_Ope4, btn_Ope5,
                           btn_GPR6, btn_GPR7, btn_IXR8, btn_IXR9, btn_I10,
                           btn_Add11, btn_Add12, btn_Add13, btn_Add14, btn_Add15]

        # Frame3
        self.frame3 = Frame(self.master,padx=win_margin,pady=win_margin)
        self.frame3.grid(row=2,column=0,sticky=E,padx=win_margin)

        # button of interaction
        btn_store = Button(self.frame3, text='Store',width=interact_btn_width).grid(row=0,column=0,padx=10,pady=5,sticky=W+E)
        btn_st_plus = Button(self.frame3, text='St+',width=interact_btn_width).grid(row=0,column=1,padx=10,pady=5,sticky=W+E)
        btn_load = Button(self.frame3, text='Load',width=interact_btn_width).grid(row=0,column=2,padx=10,pady=5,sticky=W+E)
        btn_ipl = Button(self.frame3, text='IPL',width=interact_btn_width).grid(row=0,column=3,padx=10,pady=5,sticky=W+E)
        btn_ss = Button(self.frame3, text='SS',width=interact_btn_width).grid(row=1,column=1,padx=10,pady=5,sticky=W+E)
        btn_run = Button(self.frame3, text='Run',width=interact_btn_width).grid(row=1,column=2,padx=10,pady=5,sticky=W+E)
        btn_mem_log = Button(self.frame3, text='Mem Info',width=interact_btn_width).grid(row=1,column=3,padx=10,pady=5,sticky=W+E)

        # Frame4
        self.frame4 = Frame(self.master, bd=2, relief=frame_sytle, padx=win_margin,pady=win_margin)
        self.frame4.grid(row=3,column=0,sticky=W+E+N+S,padx=win_margin,pady=win_margin)
        self.frame4.rowconfigure(0,weight=0,minsize=20)
        self.frame4.rowconfigure(1,weight=1,minsize=30)
        self.frame4.columnconfigure(0,weight=1,minsize=50)
        self.frame4.columnconfigure(1,weight=4,minsize=200)

        # label of info 
        label_step_info = Label(self.frame4, text='Step_Info').grid(row=0,column=0,sticky=W+S+N)
        label_mem_info = Label(self.frame4, text='Mem_Info').grid(row=0,column=1,sticky=W+S+N)

        # text box of info
        txt_step_info = Label(self.frame4,text=self.value_step_info,justify='left',anchor='nw',relief=text_box_style).grid(row=1,column=0,sticky=W+E+S+N)
        txt_mem_info = Label(self.frame4,text=self.value_mem_info,justify='left',anchor='nw',relief=text_box_style).grid(row=1,column=1,columnspan=4,sticky=W+E+S+N)
    
    # generate zeros
    def zero_gene(self, bit_num):
        txt=''
        for i in range(bit_num):
            txt += '0'
        return txt

    # split each 4 digits, only for value of registers (only for multiples of 4)
    def txt_split(self, num_txt):
        txt=[]
        part = int(len(num_txt)/4)
        for i in range(part):
            start = i*4
            txt.append(num_txt[start:start+4])
        return ' '.join(txt)

    # function for btn_instruction: press button to set bit into 1 or 0
    def func_btn_instruction(self, index):
        print("button "+str(index)+" is pressed")

        if self.value_instruction[index] == '1':
            
            self.value_instruction[index] = '0'
        else:
            self.value_instruction[index] = '1'
            print(self.value_instruction[index])
        self.instruction.set(self.value_instruction)
