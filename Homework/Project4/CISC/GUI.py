# -------------------------------------------------------
# @Author :     Tenphun0503
# This file implements the ui logic
# ------------------------------------------------------
from tkinter import *
from tkinter.scrolledtext import ScrolledText


def txt_split(num_txt: str):
    """This function splits '00000000' into '0000 0000'
    It only works for str with the length of multiples of 4
    """
    txt = []
    if len(num_txt) % 4 != 0:
        return num_txt
    part = int(len(num_txt) / 4)
    for i in range(part):
        start = i * 4
        txt.append(num_txt[start:start + 4])
    return ' '.join(txt)


class MainWindow:
    def __init__(self, master, sys):
        self.master = master
        self.sys = sys
        self.cache = sys.cache
        self.ins_object = sys.ins
        self.pc = sys.pc
        self.mar = sys.mar
        self.mbr = sys.mbr
        self.ir = sys.ir
        self.mfr = sys.mfr
        self.cc = sys.cc
        self.gpr0 = sys.gpr0
        self.gpr1 = sys.gpr1
        self.gpr2 = sys.gpr2
        self.gpr3 = sys.gpr3
        self.x1 = sys.x1
        self.x2 = sys.x2
        self.x3 = sys.x3
        self.fpr0 = sys.fpr0
        self.fpr1 = sys.fpr1

        # for refreshing
        self.registers = [self.gpr0, self.gpr1, self.gpr2, self.gpr3, self.x1, self.x2, self.x3,
                          self.pc, self.mar, self.mbr, self.fpr0, self.fpr1, self.ir, self.mfr, self.cc]
        # parameters to update the label widget
        self.txt_value_GPR0 = StringVar()
        self.txt_value_GPR1 = StringVar()
        self.txt_value_GPR2 = StringVar()
        self.txt_value_GPR3 = StringVar()
        self.txt_value_IXR1 = StringVar()
        self.txt_value_IXR2 = StringVar()
        self.txt_value_IXR3 = StringVar()
        self.txt_value_FPR0 = StringVar()
        self.txt_value_FPR1 = StringVar()

        self.txt_value_PC = StringVar()
        self.txt_value_MAR = StringVar()
        self.txt_value_MBR = StringVar()
        self.txt_value_IR = StringVar()
        self.txt_value_MFR = StringVar()
        self.txt_value_CC = StringVar()
        self.txt_value_registers = [self.txt_value_GPR0, self.txt_value_GPR1, self.txt_value_GPR2, self.txt_value_GPR3,
                                    self.txt_value_IXR1, self.txt_value_IXR2, self.txt_value_IXR3, self.txt_value_PC,
                                    self.txt_value_MAR, self.txt_value_MBR, self.txt_value_FPR0, self.txt_value_FPR1,
                                    self.txt_value_IR, self.txt_value_MFR, self.txt_value_CC]
        self.refresh_reg_info()

        self.txt_value_Opcode = StringVar()
        self.txt_value_GPR_index = StringVar()
        self.txt_value_IXR_index = StringVar()
        self.txt_value_Indirect = StringVar()
        self.txt_value_Address = StringVar()
        self.refresh_instruction_info()

        # Test Instruction Input
        self.test_ins_input = StringVar()
        self.test_ins_input.set('')
        # set layout
        self.__set_window()

    def __set_window(self):
        """This function sets the layout of the window"""
        # GUI setting para
        win_title = 'CSCI6461'
        win_size = '1600x900'
        win_min_width = 1200
        win_min_height = 1200
        win_color = 'LightGray'
        win_margin = 10
        frame_style = RIDGE
        text_box_style = RIDGE
        instruction_btn_width = 5
        interact_btn_width = 10

        # GUI setting
        self.master.title(win_title)
        self.master.geometry(win_size)
        self.master.minsize(win_min_width, win_min_height)
        self.master["bg"] = win_color

        # setting layout of main window
        self.master.grid_columnconfigure(0, weight=1, minsize=1200)
        self.master.grid_rowconfigure(0, weight=0, minsize=350)
        self.master.grid_rowconfigure(1, weight=0, minsize=120)
        self.master.grid_rowconfigure(2, weight=0, minsize=100)
        self.master.grid_rowconfigure(3, weight=1)

        # Frame 1
        self.frame1 = Frame(self.master, bd=2, relief=frame_style, padx=win_margin, pady=win_margin)
        self.frame1.grid(row=0, column=0, sticky=W + E, padx=win_margin, pady=win_margin)

        # setting layout of Frame 1
        self.frame1.grid_columnconfigure(1, weight=1, minsize=50)
        self.frame1.grid_columnconfigure(4, weight=1, minsize=50)
        for i in range(0, 7):
            self.frame1.grid_rowconfigure(i, weight=1, minsize=40)

        # labels of registers
        Label(self.frame1, text=self.gpr0.label).grid(row=0, column=0)
        Label(self.frame1, text=self.gpr1.label).grid(row=1, column=0)
        Label(self.frame1, text=self.gpr2.label).grid(row=2, column=0)
        Label(self.frame1, text=self.gpr3.label).grid(row=3, column=0)
        Label(self.frame1, text=self.x1.label).grid(row=4, column=0)
        Label(self.frame1, text=self.x2.label).grid(row=5, column=0)
        Label(self.frame1, text=self.x3.label).grid(row=6, column=0)
        Label(self.frame1, text=self.fpr0.label).grid(row=7, column=0)
        Label(self.frame1, text=self.fpr1.label).grid(row=8, column=0)
        Label(self.frame1, text=self.pc.label).grid(row=0, column=3)
        Label(self.frame1, text=self.mar.label).grid(row=1, column=3)
        Label(self.frame1, text=self.mbr.label).grid(row=2, column=3)
        Label(self.frame1, text=self.ir.label).grid(row=3, column=3)
        Label(self.frame1, text=self.mfr.label).grid(row=4, column=3)
        Label(self.frame1, text=self.cc.label).grid(row=5, column=3)

        # text box of registers
        Label(self.frame1, textvariable=self.txt_value_GPR0, relief=text_box_style).grid(row=0, column=1, sticky=W + E)
        Label(self.frame1, textvariable=self.txt_value_GPR1, relief=text_box_style).grid(row=1, column=1, sticky=W + E)
        Label(self.frame1, textvariable=self.txt_value_GPR2, relief=text_box_style).grid(row=2, column=1, sticky=W + E)
        Label(self.frame1, textvariable=self.txt_value_GPR3, relief=text_box_style).grid(row=3, column=1, sticky=W + E)
        Label(self.frame1, textvariable=self.txt_value_IXR1, relief=text_box_style).grid(row=4, column=1, sticky=W + E)
        Label(self.frame1, textvariable=self.txt_value_IXR2, relief=text_box_style).grid(row=5, column=1, sticky=W + E)
        Label(self.frame1, textvariable=self.txt_value_IXR3, relief=text_box_style).grid(row=6, column=1, sticky=W + E)
        Label(self.frame1, textvariable=self.txt_value_FPR0, relief=text_box_style).grid(row=7, column=1, sticky=W + E)
        Label(self.frame1, textvariable=self.txt_value_FPR1, relief=text_box_style).grid(row=8, column=1, sticky=W + E)
        Label(self.frame1, textvariable=self.txt_value_PC, relief=text_box_style).grid(row=0, column=4, sticky=W + E)
        Label(self.frame1, textvariable=self.txt_value_MAR, relief=text_box_style).grid(row=1, column=4, sticky=W + E)
        Label(self.frame1, textvariable=self.txt_value_MBR, relief=text_box_style).grid(row=2, column=4, sticky=W + E)
        Label(self.frame1, textvariable=self.txt_value_IR, relief=text_box_style).grid(row=3, column=4, sticky=W + E)
        Label(self.frame1, textvariable=self.txt_value_MFR, relief=text_box_style).grid(row=4, column=4, sticky=W + E)
        Label(self.frame1, textvariable=self.txt_value_CC, relief=text_box_style).grid(row=5, column=4, sticky=W + E)

        # LD button of registers
        Button(self.frame1, text='LD', command=lambda: self.func_reg_load(0)).grid(row=0, column=2)
        Button(self.frame1, text='LD', command=lambda: self.func_reg_load(1)).grid(row=1, column=2)
        Button(self.frame1, text='LD', command=lambda: self.func_reg_load(2)).grid(row=2, column=2)
        Button(self.frame1, text='LD', command=lambda: self.func_reg_load(3)).grid(row=3, column=2)
        Button(self.frame1, text='LD', command=lambda: self.func_reg_load(4)).grid(row=4, column=2)
        Button(self.frame1, text='LD', command=lambda: self.func_reg_load(5)).grid(row=5, column=2)
        Button(self.frame1, text='LD', command=lambda: self.func_reg_load(10)).grid(row=7, column=2)
        Button(self.frame1, text='LD', command=lambda: self.func_reg_load(11)).grid(row=8, column=2)
        Button(self.frame1, text='LD', command=lambda: self.func_reg_load(6)).grid(row=6, column=2)
        Button(self.frame1, text='LD', command=lambda: self.func_reg_load(7)).grid(row=0, column=5)
        Button(self.frame1, text='LD', command=lambda: self.func_reg_load(8)).grid(row=1, column=5)
        Button(self.frame1, text='LD', command=lambda: self.func_reg_load(9)).grid(row=2, column=5)

        # Frame2
        self.frame2 = Frame(self.master, bd=2, relief=frame_style, padx=win_margin, pady=win_margin)
        self.frame2.grid(row=1, column=0, sticky=W + E, padx=win_margin, pady=win_margin)

        # setting layout of Frame 2
        for i in range(16):
            self.frame2.grid_columnconfigure(i, weight=1, minsize=20)
        for i in range(3):
            self.frame2.grid_rowconfigure(i, weight=1, minsize=40)

        # label of Instruction
        Label(self.frame2, text='Operation').grid(row=0, column=0, columnspan=6)
        Label(self.frame2, text='GPR').grid(row=0, column=6, columnspan=2)
        Label(self.frame2, text='IXR').grid(row=0, column=8, columnspan=2)
        Label(self.frame2, text='I').grid(row=0, column=10)
        Label(self.frame2, text='Address').grid(row=0, column=11, columnspan=5)

        # text box of Instruction
        Label(self.frame2, textvariable=self.txt_value_Opcode, relief=text_box_style).grid(row=1, column=0,
                                                                                           columnspan=6,
                                                                                           sticky=W + E)
        Label(self.frame2, textvariable=self.txt_value_GPR_index, relief=text_box_style).grid(row=1, column=6,
                                                                                              columnspan=2,
                                                                                              sticky=W + E)
        Label(self.frame2, textvariable=self.txt_value_IXR_index, relief=text_box_style).grid(row=1, column=8,
                                                                                              columnspan=2,
                                                                                              sticky=W + E)
        Label(self.frame2, textvariable=self.txt_value_Indirect, relief=text_box_style).grid(row=1, column=10,
                                                                                             sticky=W + E)
        Label(self.frame2, textvariable=self.txt_value_Address, relief=text_box_style).grid(row=1,
                                                                                            column=11,
                                                                                            columnspan=5,
                                                                                            sticky=W + E)

        # button of Instruction: to set corresponding value to 1 or 0
        Button(self.frame2, text='0', width=instruction_btn_width,
               command=lambda: self.func_instruction(0)).grid(row=2, column=0)
        Button(self.frame2, text='1', width=instruction_btn_width,
               command=lambda: self.func_instruction(1)).grid(row=2, column=1)
        Button(self.frame2, text='2', width=instruction_btn_width,
               command=lambda: self.func_instruction(2)).grid(row=2, column=2)
        Button(self.frame2, text='3', width=instruction_btn_width,
               command=lambda: self.func_instruction(3)).grid(row=2, column=3)
        Button(self.frame2, text='4', width=instruction_btn_width,
               command=lambda: self.func_instruction(4)).grid(row=2, column=4)
        Button(self.frame2, text='5', width=instruction_btn_width,
               command=lambda: self.func_instruction(5)).grid(row=2, column=5)
        Button(self.frame2, text='6', width=instruction_btn_width,
               command=lambda: self.func_instruction(6)).grid(row=2, column=6)
        Button(self.frame2, text='7', width=instruction_btn_width,
               command=lambda: self.func_instruction(7)).grid(row=2, column=7)
        Button(self.frame2, text='8', width=instruction_btn_width,
               command=lambda: self.func_instruction(8)).grid(row=2, column=8)
        Button(self.frame2, text='9', width=instruction_btn_width,
               command=lambda: self.func_instruction(9)).grid(row=2, column=9)
        Button(self.frame2, text='10', width=instruction_btn_width,
               command=lambda: self.func_instruction(10)).grid(row=2, column=10)
        Button(self.frame2, text='11', width=instruction_btn_width,
               command=lambda: self.func_instruction(11)).grid(row=2, column=11)
        Button(self.frame2, text='12', width=instruction_btn_width,
               command=lambda: self.func_instruction(12)).grid(row=2, column=12)
        Button(self.frame2, text='13', width=instruction_btn_width,
               command=lambda: self.func_instruction(13)).grid(row=2, column=13)
        Button(self.frame2, text='14', width=instruction_btn_width,
               command=lambda: self.func_instruction(14)).grid(row=2, column=14)
        Button(self.frame2, text='15', width=instruction_btn_width,
               command=lambda: self.func_instruction(15)).grid(row=2, column=15)

        # Frame3
        self.frame3 = Frame(self.master, padx=win_margin, pady=win_margin)
        self.frame3.grid(row=2, column=0, sticky=W + E, padx=win_margin)
        self.frame3.grid_columnconfigure(0, weight=1)
        self.frame3.grid_columnconfigure(1, weight=1)

        self.frame3_1 = Frame(self.frame3, padx=win_margin, pady=win_margin)
        self.frame3_1.grid(row=0, column=0, sticky=W + E, padx=win_margin)
        self.frame3_1.grid_rowconfigure(0, weight=0)
        self.frame3_1.grid_rowconfigure(1, weight=0, minsize=20)

        # Input and Output
        self.input_content = StringVar()
        self.input_trigger = IntVar()
        self.input_entry = Entry(self.frame3_1, textvariable=self.input_content, state='disabled')
        self.input_entry.grid(row=0, column=0, columnspan=2, sticky=W + E)
        self.input_btn = Button(self.frame3_1, text='Enter', width=interact_btn_width,
                                command=lambda: self.input_trigger.set(1))
        self.input_btn.grid(row=0, column=2, padx=10, pady=5, sticky=W + E)
        self.input = [self.input_entry, self.input_content, self.input_btn, self.input_trigger]

        self.out = ScrolledText(self.frame3_1, relief=text_box_style, width=50, height=10, state='disabled')
        self.out.grid(row=1, column=0, sticky=W + E)

        # state indicator
        Label(self.frame3_1, text='Halt/Run').grid(row=1, column=3, padx=10, pady=5, sticky=E)
        self.canvas = Canvas(self.frame3_1, width=40, height=40)
        self.canvas.grid(row=1, column=4, sticky=W)
        self.canvas.create_rectangle(5, 15, 20, 30, fill="red")

        self.frame3_2 = Frame(self.frame3, padx=win_margin, pady=win_margin)
        self.frame3_2.grid(row=0, column=1, sticky=E, padx=win_margin)

        # button of interaction
        btn_store = Button(self.frame3_2, text='Store', width=interact_btn_width, command=self.func_store)
        btn_store.grid(row=0, column=0, padx=10, pady=5, sticky=W + E)
        btn_st_plus = Button(self.frame3_2, text='St+', width=interact_btn_width, command=self.func_st_plus)
        btn_st_plus.grid(row=0, column=1, padx=10, pady=5, sticky=W + E)
        btn_load = Button(self.frame3_2, text='Load', width=interact_btn_width, command=self.func_load)
        btn_load.grid(row=0, column=2, padx=10, pady=5, sticky=W + E)
        btn_reset = Button(self.frame3_2, text='Reset', width=interact_btn_width, command=self.reset)
        btn_reset.grid(row=0, column=3, columnspan=2, padx=10, pady=5, sticky=W + E)
        btn_ss = Button(self.frame3_2, text='SS', width=interact_btn_width, command=lambda: self.func_ss(True))
        btn_ss.grid(row=1, column=0, padx=10, pady=5, sticky=W + E)
        btn_run = Button(self.frame3_2, text='Run', width=interact_btn_width, command=self.func_run)
        btn_run.grid(row=1, column=1, padx=10, pady=5, sticky=W + E)
        btn_pg1 = Button(self.frame3_2, text='Program1', width=interact_btn_width, command=self.func_pg1)
        btn_pg1.grid(row=1, column=2, padx=10, pady=5, sticky=W + E)
        btn_pg2 = Button(self.frame3_2, text='Program2', width=interact_btn_width, command=self.func_pg2)
        btn_pg2.grid(row=1, column=3, padx=10, pady=5, sticky=W + E)

        btn_ipl = Button(self.frame3_2, text='IPL', width=interact_btn_width, command=self.func_ipl)
        btn_ipl.grid(row=2, column=0, padx=10, pady=5, sticky=W + E)
        Entry(self.frame3_2, textvariable=self.test_ins_input).grid(row=2, column=1, columnspan=2, sticky=W + E)
        btn_test = Button(self.frame3_2, text='Test', width=interact_btn_width, command=self.func_test)
        btn_test.grid(row=2, column=3, padx=10, pady=5, sticky=W + E)

        self.btns = [btn_store, btn_st_plus, btn_load, btn_ss, btn_run, btn_ipl, btn_test]

        # Frame4
        self.frame4 = Frame(self.master, bd=2, relief=frame_style, padx=win_margin, pady=win_margin)
        self.frame4.grid(row=3, column=0, sticky=W + E + N + S, padx=win_margin, pady=win_margin)

        # setting layout of Frame 4
        self.frame4.rowconfigure(0, weight=0, minsize=20)
        self.frame4.rowconfigure(1, weight=1, minsize=30)
        self.frame4.columnconfigure(0, weight=1, minsize=50)
        self.frame4.columnconfigure(1, weight=1, minsize=100)
        self.frame4.columnconfigure(2, weight=1, minsize=50)

        # label of info
        label_step_info = Label(self.frame4, text='Step_Info')
        label_step_info.grid(row=0, column=0, sticky=W + S + N)
        label_mem_info = Label(self.frame4, text='Sys_Info')
        label_mem_info.grid(row=0, column=1, sticky=W + S + N)
        label_ipl_info = Label(self.frame4, text='IPL_Info')
        label_ipl_info.grid(row=0, column=2, sticky=W + S + N)

        # text box of info
        self.txt_step_info = ScrolledText(self.frame4, relief=text_box_style)
        self.txt_step_info.grid(row=1, column=0, sticky=W + E + S + N)
        self.txt_step_info.insert(INSERT, 'System Is Ready')
        self.txt_step_info.configure(state='disabled')

        self.txt_sys_info = ScrolledText(self.frame4, relief=text_box_style)
        self.txt_sys_info.grid(row=1, column=1, sticky=W + E + S + N)
        self.refresh_sys_info()
        self.txt_sys_info.configure(state='disabled')

        self.txt_ipl_info = ScrolledText(self.frame4, relief=text_box_style)
        self.txt_ipl_info.grid(row=1, column=2, sticky=W + E + S + N)
        self.txt_ipl_info.insert(INSERT, 'Please press IPL to pre-load the program')
        self.txt_ipl_info.configure(state='disabled')

    def reset(self):
        """This function resets all the system"""
        self.sys.reset(self.out)
        self.refresh_reg_info()
        self.refresh_instruction_info()

        self.txt_ipl_info.configure(state='normal')
        self.txt_sys_info.configure(state='normal')
        self.txt_step_info.configure(state='normal')

        self.txt_ipl_info.delete(1.0, END)
        self.txt_sys_info.delete(1.0, END)
        self.txt_step_info.delete(1.0, END)

        self.txt_ipl_info.insert(INSERT, 'Please press IPL to pre-load the program')
        self.refresh_sys_info()
        self.txt_step_info.insert(INSERT, 'System Is Ready')

        self.txt_ipl_info.configure(state='disabled')
        self.txt_sys_info.configure(state='disabled')
        self.txt_step_info.configure(state='disabled')

        self.canvas.create_rectangle(5, 15, 20, 30, fill="red")

    def change_btn_state(self, state):
        for i in self.btns:
            if state:
                i.configure(state='normal')
            else:
                i.configure(state='disabled')

    def refresh_instruction_info(self):
        """This function refreshes the text of instruction"""
        space = '\t   '
        self.txt_value_Opcode.set(space.join(list(self.ins_object.opcode)))
        self.txt_value_GPR_index.set(space.join(list(self.ins_object.gpr_index)))
        self.txt_value_IXR_index.set(space.join(list(self.ins_object.ixr_index)))
        self.txt_value_Indirect.set(space.join(list(self.ins_object.indirect)))
        self.txt_value_Address.set(space.join(list(self.ins_object.address)))

    def refresh_sys_info(self):
        """This function refreshes the mem_info"""
        content = ''
        self.txt_sys_info.configure(state='normal')
        self.txt_sys_info.delete(1.0, END)
        for i in self.registers:
            content += i.label + ':\t' + txt_split(i.value.zfill(i.size)) + '\n'
        content += self.cache.print_out()
        content += self.cache.mem.print_out()
        self.txt_sys_info.insert(INSERT, content)
        self.txt_sys_info.configure(state='disabled')

    def refresh_reg_info(self):
        """This function refreshes the text of registers"""
        length = len(self.registers)
        for i in range(length):
            self.txt_value_registers[i].set(txt_split(self.registers[i].value.zfill(self.registers[i].size)))

    def func_instruction(self, index: int):
        """This function sets the bit of the instruction into 1 or 0"""
        print("button " + str(index) + " is pressed")
        self.sys.set_instruction(index)
        self.refresh_instruction_info()

    def func_reg_load(self, index: int):
        """This function loads the value of instruction into a register"""
        print("button " + self.registers[index].label + " is pressed")
        self.txt_step_info.configure(state='normal')
        self.txt_step_info.delete(1.0, END)
        self.txt_step_info.insert(INSERT, 'Load value to ' + self.registers[index].label + ':\n')
        self.sys.reg_load_ins(index, self.txt_step_info)
        self.txt_step_info.configure(state='disabled')
        self.refresh_reg_info()
        self.refresh_sys_info()

    def func_load(self):
        """This function loads the value of MEM[MAR] into MBR"""
        print('button Load is pressed')
        self.txt_step_info.configure(state='normal')
        self.txt_step_info.delete(1.0, END)
        self.txt_step_info.insert(INSERT, 'Load from Memory:\n\n')
        self.sys.load(self.txt_step_info)
        self.txt_step_info.configure(state='disabled')
        self.refresh_reg_info()
        self.refresh_sys_info()

    def func_store(self):
        """This function stores the value of MBR into MEM[MAR]"""
        print('button Store is pressed')
        self.txt_step_info.configure(state='normal')
        self.txt_step_info.delete(1.0, END)
        self.txt_step_info.insert(INSERT, 'Store into Memory:\n\n')
        self.sys.store(self.txt_step_info)
        self.txt_step_info.configure(state='disabled')
        self.refresh_sys_info()

    def func_st_plus(self):
        """This function stores the value of MBR into MEM[MAR] and MAR++"""
        print('button S+ is pressed')
        self.txt_step_info.configure(state='normal')
        self.txt_step_info.delete(1.0, END)
        self.txt_step_info.insert(INSERT, 'Store-plus:\n\n')
        self.sys.st_plus(self.txt_step_info)
        self.txt_step_info.configure(state='disabled')
        self.refresh_reg_info()
        self.refresh_sys_info()

    def func_pg1(self):
        """This function reset the system and preload the program1"""
        print('button pg1 is pressed')
        self.reset()
        self.txt_ipl_info.configure(state='normal')
        self.txt_step_info.configure(state='normal')
        self.txt_ipl_info.delete(1.0, END)
        self.txt_step_info.delete(1.0, END)
        self.sys.load_pg1(self.txt_ipl_info, self.txt_step_info)
        # mem_info refresh
        self.txt_ipl_info.configure(state='disabled')
        self.txt_step_info.configure(state='disabled')
        self.refresh_sys_info()
        self.refresh_reg_info()

    def func_pg2(self):
        """This function reset the system and preload the program1"""
        print('button pg1 is pressed')
        self.reset()
        self.txt_ipl_info.configure(state='normal')
        self.txt_step_info.configure(state='normal')
        self.txt_ipl_info.delete(1.0, END)
        self.txt_step_info.delete(1.0, END)
        self.sys.load_pg2(self.txt_ipl_info, self.txt_step_info)
        # mem_info refresh
        self.txt_ipl_info.configure(state='disabled')
        self.txt_step_info.configure(state='disabled')
        self.refresh_sys_info()
        self.refresh_reg_info()

    def func_ipl(self):
        """This function reset the system and preload the ipl.txt"""
        print('button ipl is pressed')
        self.reset()
        self.txt_ipl_info.configure(state='normal')
        self.txt_step_info.configure(state='normal')
        self.txt_ipl_info.delete(1.0, END)
        self.txt_step_info.delete(1.0, END)
        self.sys.load_file(self.txt_ipl_info, self.txt_step_info)
        # mem_info refresh
        self.txt_ipl_info.configure(state='disabled')
        self.txt_step_info.configure(state='disabled')
        self.refresh_sys_info()
        self.refresh_reg_info()

    def func_ss(self, if_ss: bool):
        """This function implements single step"""
        self.txt_step_info.configure(state='normal')
        if if_ss:
            print('button ss is pressed')
            self.change_btn_state(False)
            self.canvas.create_rectangle(5, 15, 20, 30, fill="green")
            self.txt_step_info.delete(1.0, END)
        self.txt_step_info.insert(INSERT, '-------------------------------------------------\n')
        self.txt_step_info.insert(INSERT, 'Step: PC = ' + self.pc.value + ' = ' + self.pc.get_value() + '\n\n')
        state = self.sys.single_step(self.txt_step_info, self.input, self.out)
        if if_ss:
            self.txt_step_info.insert(INSERT, 'System Halted\n\n')
            self.canvas.create_rectangle(5, 15, 20, 30, fill="red")
            self.change_btn_state(True)
        self.txt_step_info.yview_moveto(1.0)
        self.txt_step_info.configure(state='disabled')
        self.refresh_reg_info()
        self.refresh_sys_info()
        # Program done indicator for func_run
        if state == 'DONE':
            return True
        return False

    def func_run(self):
        """This function implements RUN"""
        print('button run is pressed')
        self.canvas.create_rectangle(5, 15, 20, 30, fill="green")
        self.change_btn_state(False)
        if_done = False
        self.txt_step_info.configure(state='normal')
        self.txt_step_info.delete(1.0, END)
        while not if_done:
            if_done = self.func_ss(False)
        self.txt_step_info.configure(state='normal')
        self.txt_step_info.insert(INSERT, 'System Halted!\n\n')
        self.canvas.create_rectangle(5, 15, 20, 30, fill="red")
        self.txt_step_info.configure(state='disabled')
        self.change_btn_state(True)

    def func_test(self):
        """This function implements instruction testing"""
        print('button test is pressed')
        self.txt_step_info.configure(state='normal')
        self.txt_step_info.delete(1.0, END)
        ins = self.test_ins_input.get()
        ins = ins.replace('\n', '')
        ins = ins.replace(',', ' ')
        temp = ins
        ins = []
        for i in temp.split(' '):
            if i != '':
                ins.append(i)
        ins = ' '.join(ins)
        self.txt_step_info.insert(INSERT, 'Input: ' + ins + '\n\n')
        self.sys.test_ins(ins, self.txt_step_info, self.input, self.out)
        self.refresh_reg_info()
        self.refresh_sys_info()
        self.txt_step_info.configure(state='disabled')
        self.test_ins_input.set('')
