#-------------------------------------------------------
# This file contains the class of Window
# It does most of computation
#------------------------------------------------------
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from CPU.registers import *
from instruction import *
from memory import *

class Window():
    def __init__(self, master, sys):
        self.master = master

        self.mem = sys.mem
        self.ins_object = sys.ins
        self.pc = sys.pc
        self.mar = sys.mar
        self.mbr = sys.mbr
        self.ir = sys.ir
        self.mfr = sys.mfr
        self.gpr0 = sys.gpr0
        self.gpr1 = sys.gpr1
        self.gpr2 = sys.gpr2
        self.gpr3 = sys.gpr3
        self.x1 = sys.x1
        self.x2 = sys.x2
        self.x3 = sys.x3
        # for refreshing
        self.registers = [self.gpr0, self.gpr1, self.gpr2, self.gpr3, self.x1, self.x2, self.x3, self.pc, self.mar, self.mbr, self.ir, self.mfr]

        self.xs = [sys.x1, sys.x2, sys.x3]
        self.gprs = [sys.gpr0, sys.gpr1, sys.gpr2, sys.gpr3]

        # parameters to update the label widget
        self.txt_value_GPR0 = StringVar()
        self.txt_value_GPR1 = StringVar()
        self.txt_value_GPR2 = StringVar()
        self.txt_value_GPR3 = StringVar()
        self.txt_value_IXR1 = StringVar()
        self.txt_value_IXR2 = StringVar()
        self.txt_value_IXR3 = StringVar()
        self.txt_value_PC = StringVar()
        self.txt_value_MAR = StringVar()
        self.txt_value_MBR = StringVar()
        self.txt_value_IR = StringVar()
        self.txt_value_MFR = StringVar()
        self.txt_value_registers = [self.txt_value_GPR0,self.txt_value_GPR1,self.txt_value_GPR2,self.txt_value_GPR3,
                                    self.txt_value_IXR1,self.txt_value_IXR2,self.txt_value_IXR3,
                                    self.txt_value_PC,self.txt_value_MAR,self.txt_value_MBR,self.txt_value_IR,self.txt_value_MFR]
        self.refresh_reg_info()

        self.txt_value_Opcode = StringVar()
        self.txt_value_GPR_index = StringVar()
        self.txt_value_IXR_index = StringVar()
        self.txt_value_Indirect = StringVar()
        self.txt_value_Address = StringVar()
        self.refresh_instruction_info()

        # set layout
        self.set_window()

    def set_window(self):
        """This functin sets the layout of the window"""
        # GUI setting para
        win_title = 'CSCI6461'
        win_size = '1600x900'
        win_min_width = 1200
        win_min_height = 750
        win_color = 'LightGray'
        win_margin = 10
        frame_sytle = RIDGE
        text_box_style = RIDGE
        instruction_btn_width=5
        interact_btn_width=10

        # GUI setting
        self.master.title(win_title)
        self.master.geometry(win_size)
        self.master.minsize(win_min_width,win_min_height)
        self.master["bg"] = win_color

        # setting layout of main window
        self.master.grid_columnconfigure(0,weight=1, minsize=1200)
        self.master.grid_rowconfigure(0,weight=0, minsize=350)
        self.master.grid_rowconfigure(1,weight=0, minsize=120)
        self.master.grid_rowconfigure(2,weight=0, minsize=100)
        self.master.grid_rowconfigure(3,weight=1)

        # Frame 1
        self.frame1 = Frame(self.master, bd=2, relief=frame_sytle, padx=win_margin, pady=win_margin)
        self.frame1.grid(row=0, column=0, sticky=W+E, padx=win_margin, pady=win_margin)

        # setting layout of Frame 1
        self.frame1.grid_columnconfigure(1, weight=1, minsize=50)
        self.frame1.grid_columnconfigure(4, weight=1, minsize=50)
        for i in range(0,7):
            self.frame1.grid_rowconfigure(i, weight=1, minsize=40)

        # labels of registers
        label_GPR0 = Label(self.frame1, text=self.gpr0.label).grid(row=0,column=0)
        label_GPR1 = Label(self.frame1, text=self.gpr1.label).grid(row=1,column=0)
        label_GPR2 = Label(self.frame1, text=self.gpr2.label).grid(row=2,column=0)
        label_GPR3 = Label(self.frame1, text=self.gpr3.label).grid(row=3,column=0)
        label_IXR1 = Label(self.frame1, text=self.x1.label).grid(row=4,column=0)
        label_IXR2 = Label(self.frame1, text=self.x2.label).grid(row=5,column=0)
        label_IXR3 = Label(self.frame1, text=self.x3.label).grid(row=6,column=0)
        label_PC = Label(self.frame1, text=self.pc.label).grid(row=0,column=3)
        label_MAR = Label(self.frame1, text=self.mar.label).grid(row=1,column=3)
        label_MBR = Label(self.frame1, text=self.mbr.label).grid(row=2,column=3)
        label_IR = Label(self.frame1, text=self.ir.label).grid(row=3,column=3)
        label_MFR = Label(self.frame1, text=self.mfr.label).grid(row=4,column=3)

        # text box of registers
        txt_GPR0 = Label(self.frame1, textvariable = self.txt_value_GPR0, relief=text_box_style).grid(row=0,column=1,sticky=W+E)
        txt_GPR1 = Label(self.frame1, textvariable = self.txt_value_GPR1, relief=text_box_style).grid(row=1,column=1,sticky=W+E)
        txt_GPR2 = Label(self.frame1, textvariable = self.txt_value_GPR2, relief=text_box_style).grid(row=2,column=1,sticky=W+E)
        txt_GPR3 = Label(self.frame1, textvariable = self.txt_value_GPR3, relief=text_box_style).grid(row=3,column=1,sticky=W+E)
        txt_IXR1 = Label(self.frame1, textvariable = self.txt_value_IXR1, relief=text_box_style).grid(row=4,column=1,sticky=W+E)
        txt_IXR2 = Label(self.frame1, textvariable = self.txt_value_IXR2, relief=text_box_style).grid(row=5,column=1,sticky=W+E)
        txt_IXR3 = Label(self.frame1, textvariable = self.txt_value_IXR3, relief=text_box_style).grid(row=6,column=1,sticky=W+E)
        txt_PC = Label(self.frame1, textvariable = self.txt_value_PC, relief=text_box_style).grid(row=0,column=4,sticky=W+E)
        txt_MAR = Label(self.frame1, textvariable = self.txt_value_MAR, relief=text_box_style).grid(row=1,column=4,sticky=W+E)
        txt_MBR = Label(self.frame1, textvariable = self.txt_value_MBR, relief=text_box_style).grid(row=2,column=4,sticky=W+E)
        txt_IR = Label(self.frame1, textvariable = self.txt_value_IR, relief=text_box_style).grid(row=3,column=4,sticky=W+E)
        txt_MFR = Label(self.frame1,textvariable = self.txt_value_MFR, relief=text_box_style).grid(row=4,column=4,sticky=W+E)

        # LD button of registers
        btn_GPR0 = Button(self.frame1, text='LD', command = lambda: self.func_reg_load(self.gpr0)).grid(row=0,column=2)
        btn_GPR1 = Button(self.frame1, text='LD', command = lambda: self.func_reg_load(self.gpr1)).grid(row=1,column=2)
        btn_GPR2 = Button(self.frame1, text='LD', command = lambda: self.func_reg_load(self.gpr2)).grid(row=2,column=2)
        btn_GPR3 = Button(self.frame1, text='LD', command = lambda: self.func_reg_load(self.gpr3)).grid(row=3,column=2)
        btn_IXR1 = Button(self.frame1, text='LD', command = lambda: self.func_reg_load(self.x1)).grid(row=4,column=2)
        btn_IXR2 = Button(self.frame1, text='LD', command = lambda: self.func_reg_load(self.x2)).grid(row=5,column=2)
        btn_IXR3 = Button(self.frame1, text='LD', command = lambda: self.func_reg_load(self.x3)).grid(row=6,column=2)
        btn_PC = Button(self.frame1, text='LD', command = lambda: self.func_reg_load(self.pc)).grid(row=0,column=5)
        btn_MAR = Button(self.frame1, text='LD', command = lambda: self.func_reg_load(self.mar)).grid(row=1,column=5)
        btn_MBR = Button(self.frame1, text='LD', command = lambda: self.func_reg_load(self.mbr)).grid(row=2,column=5)


        # Frame2
        self.frame2 = Frame(self.master, bd=2, relief=frame_sytle, padx=win_margin, pady=win_margin)
        self.frame2.grid(row=1, column=0, sticky=W+E, padx=win_margin, pady=win_margin)

        # setting layout of Frame 2
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
        txt_Operation = Label(self.frame2, textvariable=self.txt_value_Opcode, relief=text_box_style).grid(row=1,column=0,columnspan=6,sticky=W+E)
        txt_GPR = Label(self.frame2, textvariable=self.txt_value_GPR_index, relief=text_box_style).grid(row=1,column=6,columnspan=2,sticky=W+E)
        txt_IXR = Label(self.frame2, textvariable=self.txt_value_IXR_index, relief=text_box_style).grid(row=1,column=8,columnspan=2,sticky=W+E)
        txt_I = Label(self.frame2, textvariable=self.txt_value_Indirect, relief=text_box_style).grid(row=1,column=10,sticky=W+E)
        txt_Address = Label(self.frame2, textvariable=self.txt_value_Address, relief=text_box_style).grid(row=1,column=11,columnspan=5,sticky=W+E)

        # button of Instruction: to set corresponding value to 1 or 0
        btn_Ope0 = Button(self.frame2, text='0',width=instruction_btn_width, command = lambda: self.func_instruction(0)).grid(row=2,column=0)
        btn_Ope1 = Button(self.frame2, text='1',width=instruction_btn_width, command = lambda: self.func_instruction(1)).grid(row=2,column=1)
        btn_Ope2 = Button(self.frame2, text='2',width=instruction_btn_width, command = lambda: self.func_instruction(2)).grid(row=2,column=2)
        btn_Ope3 = Button(self.frame2, text='3',width=instruction_btn_width, command = lambda: self.func_instruction(3)).grid(row=2,column=3)
        btn_Ope4 = Button(self.frame2, text='4',width=instruction_btn_width, command = lambda: self.func_instruction(4)).grid(row=2,column=4)
        btn_Ope5 = Button(self.frame2, text='5',width=instruction_btn_width, command = lambda: self.func_instruction(5)).grid(row=2,column=5)
        btn_GPR6 = Button(self.frame2, text='6',width=instruction_btn_width, command = lambda: self.func_instruction(6)).grid(row=2,column=6)
        btn_GPR7 = Button(self.frame2, text='7',width=instruction_btn_width, command = lambda: self.func_instruction(7)).grid(row=2,column=7)
        btn_IXR8 = Button(self.frame2, text='8',width=instruction_btn_width, command = lambda: self.func_instruction(8)).grid(row=2,column=8)
        btn_IXR9 = Button(self.frame2, text='9',width=instruction_btn_width, command = lambda: self.func_instruction(9)).grid(row=2,column=9)
        btn_I10 = Button(self.frame2, text='10',width=instruction_btn_width, command = lambda: self.func_instruction(10)).grid(row=2,column=10)
        btn_Add11 = Button(self.frame2, text='11',width=instruction_btn_width, command = lambda: self.func_instruction(11)).grid(row=2,column=11)
        btn_Add12 = Button(self.frame2, text='12',width=instruction_btn_width, command = lambda: self.func_instruction(12)).grid(row=2,column=12)
        btn_Add13 = Button(self.frame2, text='13',width=instruction_btn_width, command = lambda: self.func_instruction(13)).grid(row=2,column=13)
        btn_Add14 = Button(self.frame2, text='14',width=instruction_btn_width, command = lambda: self.func_instruction(14)).grid(row=2,column=14)
        btn_Add15 = Button(self.frame2, text='15',width=instruction_btn_width, command = lambda: self.func_instruction(15)).grid(row=2,column=15)

        # Frame3
        self.frame3 = Frame(self.master,padx=win_margin,pady=win_margin)
        self.frame3.grid(row=2,column=0,sticky=E,padx=win_margin)

        # button of interaction
        btn_store = Button(self.frame3, text='Store',width=interact_btn_width, command = lambda: self.func_store(self.mar, self.mbr, self.mem)).grid(row=0,column=0,padx=10,pady=5,sticky=W+E)
        btn_st_plus = Button(self.frame3, text='St+',width=interact_btn_width, command = lambda: self.func_st_plus(self.mar, self.mbr, self.mem)).grid(row=0,column=1,padx=10,pady=5,sticky=W+E)
        btn_load = Button(self.frame3, text='Load',width=interact_btn_width, command = lambda: self.func_load(self.mar, self.mbr, self.mem)).grid(row=0,column=2,padx=10,pady=5,sticky=W+E)
        btn_reset = Button(self.frame3, text='Reset',width=interact_btn_width, command = self.reset).grid(row=0,column=3,padx=10,pady=5,sticky=W+E)
        btn_ss = Button(self.frame3, text='SS',width=interact_btn_width, command = lambda: self.func_ss(self.mem, self.pc, self.mar, self.mbr, self.ir, True)).grid(row=1,column=0,padx=10,pady=5,sticky=W+E)
        btn_run = Button(self.frame3, text='Run',width=interact_btn_width, command = lambda: self.func_run(self.mem, self.pc, self.mar, self.mbr, self.ir)).grid(row=1,column=1,padx=10,pady=5,sticky=W+E)
        btn_ipl = Button(self.frame3, text='IPL',width=interact_btn_width, command = lambda: self.func_ipl(self.pc, self.mem)).grid(row=1,column=2,padx=10,pady=5,sticky=W+E)

        # Frame4
        self.frame4 = Frame(self.master, bd=2, relief=frame_sytle, padx=win_margin,pady=win_margin)
        self.frame4.grid(row=3,column=0,sticky=W+E+N+S,padx=win_margin,pady=win_margin)

        # setting layout of Frame 4
        self.frame4.rowconfigure(0,weight=0,minsize=20)
        self.frame4.rowconfigure(1,weight=1,minsize=30)
        self.frame4.columnconfigure(0,weight=1, minsize=50)
        self.frame4.columnconfigure(1,weight=1, minsize=100)
        self.frame4.columnconfigure(2,weight=1, minsize=50)

        # label of info
        label_step_info = Label(self.frame4, text='Step_Info')
        label_step_info.grid(row=0,column=0,sticky=W+S+N)
        label_mem_info = Label(self.frame4, text='Mem_Info')
        label_mem_info.grid(row=0,column=1,sticky=W+S+N)
        label_ipl_info = Label(self.frame4, text='IPL_Info')
        label_ipl_info.grid(row=0,column=2,sticky=W+S+N)

        # text box of info
        self.txt_step_info = ScrolledText(self.frame4, relief=text_box_style)
        self.txt_step_info.grid(row=1,column=0,sticky=W+E+S+N)
        self.txt_step_info.insert(INSERT, 'System Is Ready')

        self.txt_mem_info = ScrolledText(self.frame4, relief=text_box_style)
        self.txt_mem_info.grid(row=1,column=1, sticky=W+E+S+N)
        self.refresh_mem_info()

        self.txt_ipl_info = ScrolledText(self.frame4, relief=text_box_style)
        self.txt_ipl_info.grid(row=1,column=2,sticky=W+E+S+N)
        self.txt_ipl_info.insert(INSERT, 'Please press IPL to pre-load the program')


    def txt_split(self, num_txt):
        """This function splits '00000000' into '0000 0000'
        It only works for str with the length of multiples of 4
        """
        txt = []
        if len(num_txt)%4 != 0:
            return num_txt
        part = int(len(num_txt)/4)
        for i in range(part):
            start = i*4
            txt.append(num_txt[start:start+4])
        return ' '.join(txt)

    def reset(self):
        """This function resets all of the system"""
        self.mem.reset_memory()
        for i in self.registers:
            i.reset()
        self.ins_object.reset()

        self.refresh_reg_info()
        self.refresh_instruction_info()

        self.txt_ipl_info.delete(1.0, END)
        self.txt_mem_info.delete(1.0, END)
        self.txt_step_info.delete(1.0, END)
        self.txt_ipl_info.insert(INSERT, 'Please press IPL to pre-load the program')
        self.refresh_mem_info()
        self.txt_step_info.insert(INSERT, 'System Is Ready')

    def refresh_instruction_info(self):
        """This function refreshes the text of instruction"""
        space = '\t   '
        self.txt_value_Opcode.set(space.join(list(self.ins_object.opcode)))
        self.txt_value_GPR_index.set(space.join(list(self.ins_object.gpr_index)))
        self.txt_value_IXR_index.set(space.join(list(self.ins_object.ixr_index)))
        self.txt_value_Indirect.set(space.join(list(self.ins_object.indirect)))
        self.txt_value_Address.set(space.join(list(self.ins_object.address)))

    def refresh_mem_info(self):
        """This function refreshes the mem_info"""
        content = ''
        self.txt_mem_info.delete(1.0, END)
        for i in self.registers:
            content += i.label + ':\t' + self.txt_split(i.value.zfill(i.size)) +'\n'
        for i in range(len(self.mem.memory)):
            content += str(i) + ':\t' + str(int(self.mem.memory[i])) + '\n'
        self.txt_mem_info.insert(INSERT, content)

    def refresh_reg_info(self):
        """This function refreshes the text of tegisters"""
        length = len(self.registers)
        for i in range(length):
            self.txt_value_registers[i].set(self.txt_split(self.registers[i].value.zfill(self.registers[i].size)))

    def func_instruction(self, index):
        """This function sets the bit of the instruction into 1 or 0"""
        print("button "+str(index)+" is pressed")
        temp = list(self.ins_object.value)
        if temp[index] == '1':
            temp[index] = '0'
        else:
            temp[index] = '1'
        self.ins_object.value = ''.join(temp)
        self.ins_object.update()
        self.refresh_instruction_info()

    def func_reg_load(self, reg : Register):
        """This function loads the value of instruciton into a register"""
        print("button "+ reg.label+" is pressed")
        self.txt_step_info.delete(1.0, END)
        self.txt_step_info.insert(INSERT, 'Load value to ' + reg.label + ':\n')
        reg.value = self.ins_object.value[16-reg.size:16]
        self.refresh_reg_info()
        self.refresh_mem_info()
        self.txt_step_info.insert(INSERT, reg.label + ' <- ' + str(int(reg.value)))

    def func_load(self, mar : MAR, mbr : MBR, mem : Memory):
        """This function loads the value of MEM[MAR] into MBR"""
        print('button Load is pressed')
        self.txt_step_info.delete(1.0, END)
        self.txt_step_info.insert(INSERT, 'Load from Memory:\n\n')
        self.txt_step_info.insert(INSERT, 'MBR <- MEM[MAR]:\n')
        mbr.load_from_mem(mar,mem)
        self.refresh_reg_info()
        self.refresh_mem_info()
        self.txt_step_info.insert(INSERT,  'MBR = MEM[' + str(int(mar.value,2)) + '] = ' + str(int(mbr.value)) + '\n')

    def func_store(self, mar : MAR, mbr : MBR, mem : Memory):
        """This function stores the value of MBR into MEM[MAR]"""
        print('button Store is pressed')
        self.txt_step_info.delete(1.0, END)
        self.txt_step_info.insert(INSERT, 'Store into Memory:\n\n')
        self.txt_step_info.insert(INSERT, 'MEM[MAR] <- MBR:\n')
        mbr.store_to_mem(mar,mem)
        self.refresh_mem_info()
        self.txt_step_info.insert(INSERT,  'MEM['+ str(int(mar.value,2)) + '] = ' + str(int(mem.memory[int(mar.value,2)])) + '\n')

    def func_st_plus(self, mar : MAR, mbr : MBR, mem : Memory):
        """This function stores the value of MBR into MEM[MAR] and MAR++"""
        print('button S+ is pressed')
        self.txt_step_info.delete(1.0, END)
        self.txt_step_info.insert(INSERT, 'Store-plus:\n\n')
        self.txt_step_info.insert(INSERT, 'MEM[MAR] <- MBR:\n')
        mbr.store_to_mem(mar, mem)
        self.txt_step_info.insert(INSERT,  'MEM['+ str(int(mar.value,2)) + '] = ' + str(int(mem.memory[int(mar.value,2)])) + '\n\n')

        self.txt_step_info.insert(INSERT, 'MAR++:\n')
        mar.add_10(1)
        self.refresh_reg_info()
        self.refresh_mem_info()
        self.txt_step_info.insert(INSERT, 'MAR = ' + str(int(mar.value)) + '\n')

    def func_ipl(self, pc : PC, mem = Memory):
        """This function reset the system and pre-load the ipl.txt"""
        self.reset()
        self.txt_ipl_info.delete(1.0, END)
        self.txt_step_info.delete(1.0, END)
        file_dir = './ipl.txt'
        try:
            with open(file_dir, 'r') as f:
                lines = f.readlines()
            f.close()
        except FileNotFoundError:
             self.txt_ipl_info.insert(INSERT, file_dir + ' does not exist')
             return

        for i in lines:
            # ipl_info update
            self.txt_ipl_info.insert(INSERT, i)
            # mem[add] <- value
            temp = i.split(' ')
            add, value = int(temp[0],16),bin(int(temp[1][0:4],16))[2:]
            mem.set_to_memory(add,value)
            # step_info update
            self.txt_step_info.insert(INSERT, 'MEM[' + str(add) + '] = ' + value + '\n')

        # set pc (10 by default)
        pc.value = '1010'
        self.txt_step_info.insert(INSERT, 'PC has been set to ' + pc.value)
        # mem_info refresh
        self.refresh_mem_info()
        self.refresh_reg_info()

    def func_ss(self, mem : Memory, pc : PC, mar : MAR, mbr : MBR, ir : IR, if_clean : bool):
        """This function implements single step"""
        print('button ss is pressed')
        if if_clean:
            self.txt_step_info.delete(1.0, END)
        self.txt_step_info.insert(INSERT, '-------------------------------------------------\n')
        self.txt_step_info.insert(INSERT, 'Step: PC = ' + pc.value + '\n\n')

        # Fetch Instruction
        self.txt_step_info.insert(INSERT, 'Fetch Instruction \n')
        # MAR <- PC
        mar.get_from_PC(pc)
        self.txt_step_info.insert(INSERT, 'MAR <- PC :\t\t\tMAR = ' + mar.value + '\n')
        # MBR <- mem[MAR]
        mbr.load_from_mem(mar,mem)
        self.txt_step_info.insert(INSERT, 'MBR <- MEM['+ str(int(mar.value,2)) + '] :\t\t\tMBR = ' + mbr.value + '\n')
        # IR <- MBR
        ir.get_from_MBR(mbr)
        self.txt_step_info.insert(INSERT, 'IR <- MBR :\t\t\tIR = ' + ir.value + '\n\n')


        # Decode
        self.txt_step_info.insert(INSERT, 'Decode Instruction \n')
        word = Instruction(ir.value)
        op = int(word.opcode,2)
        gpr = self.gprs[int(word.gpr_index,2)]

        # Halt
        if op == 0:
            self.txt_step_info.insert(INSERT, 'Program is done\n\n')
            return False
        self.txt_step_info.insert(INSERT, 'Instruction :\t\t\t' + word.print_out() + '\n\n')


        # Locate
        self.txt_step_info.insert(INSERT, 'Locate EA \n')
        # IAR <- ADD
        iar = Register(12, 'IAR')
        iar.value = str(int(word.address))
        self.txt_step_info.insert(INSERT, 'IAR <- Add :\t\t\tIAR = ' + iar.value + '\n')
        # IAR += X[IXR] if IXR = 1 or 2 or 3
        ixr_id = int(word.ixr_index,2)
        if ixr_id != 0:
            ixr = self.xs[ixr_id-1]
            iar.add_2(ixr.value)
            self.txt_step_info.insert(INSERT, 'IAR += ' + ixr.label + ' :\t\t\tIAR = ' + iar.value + '\n')
        # IAR <- MEM[IAR] if I = 1
        if int(word.indirect,2) == 1:
            add = int(iar.value,2)
            iar.value = mem.get_from_memory(add)
            self.txt_step_info.insert(INSERT, 'IAR <- MEM[' + str(add) + '] :\t\t\tIAR = ' + iar.value + '\n')
        # MAR <- IAR
        mar.value = iar.value
        self.txt_step_info.insert(INSERT, 'MAR <- IAR :\t\t\tMAR = ' + mar.value + '\n\n')

        # Excute and Deposit
        self.txt_step_info.insert(INSERT, 'Excute and Deposit Result \n')


        irr = Register(16,'IRR')
        # LDR
        if op == 1:
            # MBR <- MEM[MAR]
            mbr.load_from_mem(mar,mem)
            self.txt_step_info.insert(INSERT, 'MBR <- MEM['+ str(int(mar.value,2)) + '] :\t\t\tMBR = ' + mbr.value + '\n')
            # IRR <- MBR
            irr.value = mbr.value
            self.txt_step_info.insert(INSERT, 'IRR <- MBR :\t\t\tIRR = ' + irr.value + '\n')
            # R[GPR] <- IRR
            gpr.value = irr.value
            self.txt_step_info.insert(INSERT, gpr.label + ' <- IRR :\t\t\t' + gpr.label + ' = ' + gpr.value + '\n')
        # STR
        elif op == 2:
            # IRR <- R[GPR]
            irr.value = gpr.value
            self.txt_step_info.insert(INSERT, 'IRR <- ' + gpr.label + ' :\t\t\tIRR = ' + irr.value + '\n')
            # MBR <- IRR
            mbr.value = irr.value
            self.txt_step_info.insert(INSERT, 'MBR <- IRR :\t\t\tMBR = ' + mbr.value + '\n')
            # MEM[MAR] <- MBR
            mbr.store_to_mem(mar, mem)
            self.txt_step_info.insert(INSERT, 'MEM['+ str(int(mar.value,2)) + '] <- MBR :\t\t\tMEM['+ str(int(mar.value,2)) + '] = ' + mem.memory[int(mar.value,2)] + '\n')
        # LDA
        elif op == 3:
            # MBR <- MAR
            mbr.value = mar.value
            self.txt_step_info.insert(INSERT, 'MBR <- MAR : \t\t\tMBR = ' + mbr.value + '\n')
            # IRR <- MBR
            irr.value = mbr.value
            self.txt_step_info.insert(INSERT, 'IRR <- MBR :\t\t\tIRR = ' + irr.value + '\n')
            # R[GPR] <- IRR
            gpr.value = irr.value
            self.txt_step_info.insert(INSERT, gpr.label + ' <- IRR :\t\t\t' + gpr.label + ' = ' + gpr.value + '\n')
        # LDX
        elif op == 33:
            # MBR <- MEM[MAR]
            mbr.load_from_mem(mar,mem)
            self.txt_step_info.insert(INSERT, 'MBR <- MEM['+ str(int(mar.value,2)) + '] :\t\t\tMBR = ' + mbr.value + '\n')
            # IRR <- MBR
            irr.value = mbr.value
            self.txt_step_info.insert(INSERT, 'IRR <- MBR :\t\t\tIRR = ' + irr.value + '\n')
            # X[IXR] <- IRR
            ixr = self.xs[ixr_id-1]
            ixr.value = irr.value
            self.txt_step_info.insert(INSERT, ixr.label + ' <- IRR :\t\t\t' + ixr.label + ' = ' + ixr.value + '\n')
        # STX
        elif op == 34:
            # IRR <- X[IXR]
            ixr = self.xs[ixr_id-1]
            irr.value = ixr.value
            self.txt_step_info.insert(INSERT, 'IRR <- ' + ixr.label + ' :\t\t\tIRR = ' + irr.value + '\n')
            # MBR <- IRR
            mbr.value = irr.value
            self.txt_step_info.insert(INSERT, 'MBR <- IRR :\t\t\tMBR = ' + mbr.value + '\n')
            # MEM[MAR] <- MBR
            mbr.store_to_mem(mar, mem)
            self.txt_step_info.insert(INSERT, 'MEM['+ str(int(mar.value,2)) + '] <- MBR :\t\t\tMEM['+ str(int(mar.value,2)) + '] = ' + mem.memory[int(mar.value,2)] + '\n')

        # PC++
        pc.next()
        self.txt_step_info.insert(INSERT, '\nPC++ :\t\t\tPC = ' + pc.value + '\n')
        self.refresh_reg_info()
        self.refresh_mem_info()
        return True

    def func_run(self, mem : Memory, pc : PC, mar : MAR, mbr : MBR, ir : IR):
        """This function implements RUN"""
        if_run = True
        self.txt_step_info.delete(1.0, END)
        while if_run:
            if_run = self.func_ss(mem,pc,mar,mbr,ir,False)
