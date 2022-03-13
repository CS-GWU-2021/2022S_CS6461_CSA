#-----------------------------------------------------------------
# @Author :     Tenphun0503
# This file implements the main logic of the system
#-----------------------------------------------------------------
import time
from GUI import *
from CPU.registers import *
from CPU.instruction import *
from CPU.ALU import *
from memory import *
from ioDevice import *

class System:
    def __init__(self, file_dir, pc_default):
        # initialize memory
        self.mem = Memory()
        # initialize an instruction object
        self.ins = Instruction()
        # initialize registers
        self.pc = PC()
        self.mar = MAR()
        self.mbr = MBR()
        self.ir = IR()
        self.mfr = MFR()
        self.cc = CC()
        self.gpr0 = GPR(label='GPR0')
        self.gpr1 = GPR(label='GPR1')
        self.gpr2 = GPR(label='GPR2')
        self.gpr3 = GPR(label='GPR3')
        self.x1 = IXR(label='IXR1')
        self.x2 = IXR(label='IXR2')
        self.x3 = IXR(label='IXR3')
        # initialize ALU
        self.alu = ALU(self.cc)

        # for refreshing
        self.registers = [self.gpr0, self.gpr1, self.gpr2, self.gpr3, self.x1, self.x2, self.x3,
                            self.pc, self.mar, self.mbr, self.ir, self.mfr, self.cc]
        self.gprs = [self.gpr0, self.gpr1, self.gpr2, self.gpr3]
        self.xs = [self.x1, self.x2, self.x3]

        # initialize io devices
        self.keyboard = Keyboard()
        self.printer = Printer()

        self.file_dir = file_dir
        self.pc_default = pc_default

    def reset(self, output):
        """This function resets the system
        It's called in GUI.resets
        """
        self.mem.reset_memory()
        for reg in self.registers:
            reg.reset()
        self.ins.reset()
        self.alu.reset()
        self.keyboard.reset()
        self.printer.reset()
        output.configure(state='normal')
        output.delete(1.0, END)
        output.configure(state='disabled')

    def set_instruction(self, index):
        """This function sets the bit of instruciton into 1 or 0
        It's called in GUI.func_instruction
        """
        temp = list(self.ins.value)
        if temp[index] == '1':
            temp[index] = '0'
        else:
            temp[index] = '1'
        self.ins.value = ''.join(temp)
        self.ins.update()

    def reg_load_ins(self, index, txt):
        """This function loads register with the value of the instruciton
        It's called in GUI.func_reg_load
        """
        reg = self.registers[index]
        reg.value = self.ins.value[16-reg.size:16]
        txt.insert(INSERT, reg.label + '<-' + str(int(reg.value)))

    def load(self, txt):
        """MBR <- MEM[MAR]
        It's called in GUI.func_reg_load
        """
        txt.insert(INSERT, 'MBR <- MEM[MAR]:\n')
        self.mbr.load_from_mem(self.mar, self.mem)
        txt.insert(INSERT, 'MBR = MEM[' + self.mar.get_value() + '] = ' + str(int(self.mbr.value)) + '\n')

    def store(self, txt):
        """MEM[MAR] <- MBR
        It's called in GUI.fun_store
        """
        txt.insert(INSERT, 'MEM[MAR] <- MBR:\n')
        self.mbr.store_to_mem(self.mar, self.mem)
        txt.insert(INSERT, 'MEM[' + self.mar.get_value() + '] = '
                   + str(int(self.mem.get_from_memory(int(self.mar.value, 2)))) + '\n\n')

    def st_plus(self, txt):
        """MEM[MAR] <- MBR; MAR++
        It's called in GUI.fun_st_plus
        """
        txt.insert(INSERT, 'MEM[MAR] <- MBR:\n')
        self.mbr.store_to_mem(self.mar, self.mem)
        txt.insert(INSERT, 'MEM[' + self.mar.get_value() + '] = '
                   + str(int(self.mem.get_from_memory(int(self.mar.value, 2)))) + '\n\n')

        txt.insert(INSERT, 'MAR++:\n')
        self.mar.add_10(1)
        txt.insert(
            INSERT, 'MAR = ' + str(int(self.mar.value)) + '\n')

    def load_file(self, txt_ipl_info, txt_step_info):
        """Pre-load the file
        It's called in GUI.fun_ipl
        """
        try:
            with open(self.file_dir, 'r') as f:
                lines = f.readlines()
            f.close()
        except FileNotFoundError:
            txt_ipl_info.insert(INSERT, self.file_dir + 'does not exist')
            return

        for i in lines:
            i = i.replace('\n','')
            if i == '':
                continue
            # ipl_info update
            txt_ipl_info.insert(INSERT, i + '\n')
            # mem[add] <- value
            temp = i.split(' ')
            if temp[0] == '#':
                continue
            add, value = int(temp[0], 16), bin(int(temp[1][0:4], 16))[2:]
            self.mem.set_to_memory(add, value)
            # step_info update
            txt_step_info.insert(
                INSERT, 'MEM[' + str(add) + '] = ' + value + '\n')

        # set pc by default
        self.pc.value = bin(self.pc_default)[2:]
        txt_step_info.insert(INSERT, 'PC has been set to ' + self.pc.value)

    def __fetch(self, txt):
        """Fetching of instruciton"""
        txt.insert(INSERT, 'Fetch Instruction \n')
        # MAR <- PC
        self.mar.get_from_PC(self.pc)
        txt.insert(INSERT, 'MAR <- PC :\t\t\tMAR = ' + self.mar.value + '\n')
        # MBR <- mem[MAR]
        self.mbr.load_from_mem(self.mar, self.mem)
        txt.insert(INSERT, 'MBR <- MEM[' + self.mar.get_value() + '] :\t\t\tMBR = ' + self.mbr.value + '\n')
        # IR <- MBR
        self.ir.get_from_MBR(self.mbr)
        txt.insert(INSERT, 'IR <- MBR :\t\t\tIR = ' + self.ir.value + '\n\n')

    def __decode(self, txt):
        """Decoding of instruciton"""
        txt.insert(INSERT, 'Decode Instruction \n')
        word = Instruction(self.ir.value)
        txt.insert(INSERT, 'Instruction :\t\t\t' + word.print_out() + '\n\n')
        return word

    def __locate(self, txt, word):
        """Computation of EA"""
        txt.insert(INSERT, 'Locate EA \n')
        # IAR <- ADD
        iar = Register(12, 'IAR')
        iar.value = str(int(word.address))
        txt.insert(INSERT, 'IAR <- Add :\t\t\tIAR = ' + iar.value + '\n')
        # IAR += X[IXR] if IXR = 1 or 2 or 3
        ixr_id = int(word.ixr_index,2)
        if ixr_id != 0:
            ixr = self.xs[ixr_id-1]
            iar.value = bin(int(iar.value,2) + int(ixr.value,2))[2:]
            txt.insert(INSERT, 'IAR += ' + ixr.label + ' :\t\t\tIAR = ' + iar.value + '\n')
        # IAR <- MEM[IAR] if I = 1
        if int(word.indirect,2) == 1:
            add = int(iar.value,2)
            iar.value = self.mem.get_from_memory(add)
            txt.insert(INSERT, 'IAR <- MEM[' + str(add) + '] :\t\t\tIAR = ' + iar.value + '\n')
        # MAR <- IAR
        self.mar.value = iar.value
        txt.insert(INSERT, 'MAR <- IAR :\t\t\tMAR = ' + self.mar.value + '\n\n')

    def __execute_deposit(self, txt, word, input, output):
        """The execution and depostion"""
        txt.insert(INSERT, 'Excute and Deposit Result \n')
        irr = Register(16,'IRR')
        ea = self.mar.value
        op = int(word.opcode, 2)
        if op in [16, 17, 18, 19, 20, 21]:
            rx = self.gprs[int(word.rx,2)]
            if op != 21:
                ry = self.gprs[int(word.ry,2)]
        elif op in [25, 26]:
            a_l = int(word.a_l)
            l_r = int(word.l_r)
            count = int(word.count,2)
            gpr = self.gprs[int(word.gpr_index, 2)]
        else:
            gpr = self.gprs[int(word.gpr_index, 2)]
            ixr = self.xs[int(word.ixr_index,2)-1]
            immed = word.address
            devid = word.address
        # LDR
        if op == 1:
            # MBR <- MEM[MAR]
            self.mbr.load_from_mem(self.mar,self.mem)
            txt.insert(INSERT, 'MBR <- MEM['+ self.mar.get_value() + '] :\t\t\tMBR = ' + self.mbr.value + '\n')
            # IRR <- MBR
            irr.value = self.mbr.value
            txt.insert(INSERT, 'IRR <- MBR :\t\t\tIRR = ' + irr.value + '\n')
            # R[GPR] <- IRR
            gpr.value = irr.value
            txt.insert(INSERT, gpr.label + ' <- IRR :\t\t\t' + gpr.label + ' = ' + gpr.value + '\n')
        # STR
        elif op == 2:
            # IRR <- R[GPR]
            irr.value = gpr.value
            txt.insert(INSERT, 'IRR <- ' + gpr.label + ' :\t\t\tIRR = ' + irr.value + '\n')
            # MBR <- IRR
            self.mbr.value = irr.value
            txt.insert(INSERT, 'MBR <- IRR :\t\t\tMBR = ' + self.mbr.value + '\n')
            # MEM[MAR] <- MBR
            self.mbr.store_to_mem(self.mar, self.mem)
            txt.insert(INSERT, 'MEM['+ self.mar.get_value() + '] <- MBR :\t\t\tMEM['+ self.mar.get_value() + '] = ' + self.mem.memory[int(self.mar.value,2)] + '\n')
        # LDA
        elif op == 3:
            # MBR <- MAR
            self.mbr.value = self.mar.value
            txt.insert(INSERT, 'MBR <- MAR : \t\t\tMBR = ' + self.mbr.value + '\n')
            # IRR <- MBR
            irr.value = self.mbr.value
            txt.insert(INSERT, 'IRR <- MBR :\t\t\tIRR = ' + irr.value + '\n')
            # R[GPR] <- IRR
            gpr.value = irr.value
            txt.insert(INSERT, gpr.label + ' <- IRR :\t\t\t' + gpr.label + ' = ' + gpr.value + '\n')
        # AMR: R=c(R)+c(EA)
        elif op == 4:
            txt.insert(INSERT, gpr.label + ' + MEM['+ self.mar.get_value() + '] :\t\t\t')
            txt.insert(INSERT, gpr.get_value() + ' + ' + self.mem.get_value(self.mar.value) + '\n')
            # MBR <- MEM[MAR]
            self.mbr.load_from_mem(self.mar,self.mem)
            txt.insert(INSERT, 'MBR <- MEM['+ self.mar.get_value() + '] :\t\t\tMBR = ' + str(int(self.mbr.value)) + '\n')
            # IRR <- R[GPR] + MBR
            irr.value = self.alu.arithmetic_cal('+', gpr.value, self.mbr.value)
            txt.insert(INSERT, 'IRR <- ' + gpr.label + ' + MBR:\t\t\tIRR = ' + irr.value + '\n')
            # R[GPR] <- IRR
            gpr.value = irr.value
            txt.insert(INSERT, gpr.label + ' <- IRR :\t\t\t' + gpr.label + ' = ' + gpr.value + '\n')
        # SMR: R=c(R)-c(EA)
        elif op == 5:
            txt.insert(INSERT, gpr.label + ' - MEM['+ self.mar.get_value() + '] :\t\t\t')
            txt.insert(INSERT, gpr.get_value() + ' - ' + self.mem.get_value(self.mar.value) + '\n')
            # MBR <- MEM[MAR]
            self.mbr.load_from_mem(self.mar,self.mem)
            txt.insert(INSERT, 'MBR <- MEM['+ self.mar.get_value() + '] :\t\t\tMBR = ' + str(int(self.mbr.value)) + '\n')
            # IRR <- R[GPR] + MBR
            irr.value = self.alu.arithmetic_cal('-', gpr.value, self.mbr.value)
            txt.insert(INSERT, 'IRR <- ' + gpr.label + ' - MBR:\t\t\tIRR = ' + irr.value + '\n')
            # R[GPR] <- IRR
            gpr.value = irr.value
            txt.insert(INSERT, gpr.label + ' <- IRR :\t\t\t' + gpr.label + ' = ' + gpr.value + '\n')
        # AIR: R=c(R)+Immed
        elif op == 6:
            txt.insert(INSERT, gpr.label + ' + Immed : \t\t\t' + gpr.get_value() + ' + ' + str(int(immed,2)) + '\n')
            # IRR <- R[GPR] + Immed
            irr.value = self.alu.arithmetic_cal('+', gpr.value, immed)
            txt.insert(INSERT, 'IRR <- ' + gpr.label + ' + Immed:\t\t\tIRR = ' + irr.value + '\n')
            # R[GPR] <- IRR
            gpr.value = irr.value
            txt.insert(INSERT, gpr.label + ' <- IRR :\t\t\t' + gpr.label + ' = ' + gpr.value + '\n')
        # SIR: R=c(R)-Immed
        elif op == 7:
            txt.insert(INSERT, gpr.label + ' - Immed : \t\t\t' + gpr.get_value() + ' - ' + str(int(immed,2)) + '\n')
            # IRR <- R[GPR] - Immed
            irr.value = self.alu.arithmetic_cal('-', gpr.value, immed)
            txt.insert(INSERT, 'IRR <- ' + gpr.label + ' - Immed:\t\t\tIRR = ' + irr.value + '\n')
            # R[GPR] <- IRR
            gpr.value = irr.value
            txt.insert(INSERT, gpr.label + ' <- IRR :\t\t\t' + gpr.label + ' = ' + gpr.value + '\n')
        # JZ: PC=EA if c(R)=0 else PC++
        elif op == 8:
            txt.insert(INSERT, gpr.label +  ' = ' + str(int(gpr.value)) + '\t\t\t')
            if int(gpr.value,2) == 0:
                txt.insert(INSERT, gpr.label + ' == 0\n')
                # PC <- EA
                self.pc.value = ea
                txt.insert(INSERT, 'PC <- EA :\t\t\tPC = ' + self.pc.value + '\n\n')
            else:
                txt.insert(INSERT, gpr.label + ' != 0\n')
                # PC ++
                self.pc.next()
                txt.insert(INSERT, 'PC ++ :\t\t\tPC = ' + self.pc.value + '\n\n')
        # JNE: PC=EA if c(R)!=0 else PC++
        elif op == 9:
            txt.insert(INSERT, gpr.label +  ' = ' + str(int(gpr.value)) + '\t\t\t')
            if int(gpr.value,2) != 0:
                txt.insert(INSERT, gpr.label + ' != 0\n')
                # PC <- EA
                self.pc.value = ea
                txt.insert(INSERT, 'PC <- EA :\t\t\tPC = ' + self.pc.value + '\n\n')
            else:
                txt.insert(INSERT, gpr.label + ' == 0\n')
                # PC ++
                self.pc.next()
                txt.insert(INSERT, 'PC ++ :\t\t\tPC = ' + self.pc.value + '\n\n')
        # JCC: PC=EA if CC[r]=1 else PC++
        elif op == 10:
            index = int(word.gpr_index,2)
            txt.insert(INSERT, 'CC[' + str(index) +'] = ' + self.cc.value[index] + '\n')
            print(self.cc.value)
            if self.cc.value[index] == '1':
                # PC <- EA
                self.pc.value = ea
                txt.insert(INSERT, 'PC <- EA :\t\t\tPC = ' + self.pc.value + '\n\n')
            else:
                # PC ++
                self.pc.next()
                txt.insert(INSERT, 'PC ++ :\t\t\tPC = ' + self.pc.value + '\n\n')
        # JMA:  PC=EA
        elif op == 11:
            self.pc.value = ea
            txt.insert(INSERT, 'PC <- EA :\t\t\tPC = ' + self.pc.value + '\n\n')
        # JSR: R3=PC+1; PC=EA
        elif op == 12:
            self.pc.next()
            txt.insert(INSERT, 'PC ++ :\t\t\tPC = ' + self.pc.value + '\n')
            self.gpr3.value = self.pc.value
            txt.insert(INSERT, 'GPR3 <- PC :\t\t\tGPR3 = ' + self.gpr3.value + '\n')
            self.pc.value = ea
            txt.insert(INSERT, 'PC <- EA :\t\t\tPC = ' + self.pc.value + '\n\n')
        # RFS: R0=Immed; PC=c(R3)
        # if c(R3).len > pc.size pc=c(r3)[-pc.size:]
        elif op == 13:
            self.gpr0.value = immed
            txt.insert(INSERT, 'GPR0 <- Immed :\t\t\tGPR0 = ' + self.gpr0.value + '\n')
            self.pc.value = str(int(self.gpr3.value[-self.pc.size:]))
            txt.insert(INSERT, 'PC <- GPR3 :\t\t\tPC = ' + self.pc.value + '\n\n')
        # SOB: R=c(R)-1; PC=EA if C(R)>0 else PC++
        elif op == 14:
            gpr.value = self.alu.arithmetic_cal('-', gpr.value, '1')
            gpr_value = self.alu.value
            # 需要修改小于0时候的表达方式
            if gpr_value > 0:
                txt.insert(INSERT, gpr.label + ' -- :\t\t\t' + gpr.label + ' = ' + gpr.value + '\n')
                txt.insert(INSERT, gpr.label + ' > 0\n')
                self.pc.value = ea
                txt.insert(INSERT, 'PC <- EA : \t\t\tPC = ' + self.pc.value + '\n\n')
            else:
                txt.insert(INSERT, gpr.label + ' -- :\t\t\t' + gpr.label + ' = ' + str(gpr_value) + '\n')
                txt.insert(INSERT, gpr.label + ' <= 0\n')
                self.pc.next()
                txt.insert(INSERT, 'PC ++ : \t\t\tPC = ' + self.pc.value + '\n\n')
        # JGE: PC=EA if c(R)>=0 else PC++ 这玩意儿能小于0？
        elif op == 15:
            txt.insert(INSERT, gpr.label +  ' = ' + str(int(gpr.value)) + '\t\t\t')
            if int(gpr.value,2) >= 0:
                txt.insert(INSERT, gpr.label + ' >= 0\n')
                self.pc.value = ea
                txt.insert(INSERT, 'PC <- EA : \t\t\tPC = ' + self.pc.value + '\n\n')
            else:
                txt.insert(INSERT, gpr.label + ' < 0\n')
                self.pc.next()
                txt.insert(INSERT, 'PC ++ : \t\t\tPC = ' + self.pc.value + '\n\n')
        # MLT: Rx, Rx+1=c(Rx)*(Ry) 修改
        elif op == 16:
            if int(word.rx,2) not in [0,2] or int(word.ry,2) not in [0,2]:
                txt.insert(INSERT, "Rx, Ry must be 0 or 2\n")
            else:
                # Rx+1
                rxx = self.gprs[int(word.rx,2)+1]
                txt.insert(INSERT, rx.label + ' * ' + ry.label + ' :\t\t\t' + rx.get_value() + ' * ' + ry.get_value() + '\n')
                # IRR = Rx * Ry
                irr.value = self.alu.arithmetic_cal('*', rx.value, ry.value)
                txt.insert(INSERT, "IRR <- Rx * Ry\t\t\tIRR = " + irr.value + '\n')
                # Rx = Highter bits
                # Rx+1 = Lower bits
                rx.value = irr.value
                txt.insert(INSERT, rx.label + ' <- IRR\t\t\t' + rx.label + ' = ' + rx.value + '\n\n')
                txt.insert(INSERT, 'CC State:\t\t\t' + self.cc.state + '\n')
        # DVD: Rx, Rx+1=c(Rx)/(Ry)
        elif op == 17:
            if int(word.rx,2) not in [0,2] or int(word.ry,2) not in [0,2]:
                txt.insert(INSERT, "Rx, Ry must be 0 or 2\n")
            else:
                txt.insert(INSERT, rx.label + ' / ' + ry.label + ' :\t\t\t' + rx.get_value() + ' / ' + ry.get_value() + '\n')
                # Ry = 0 -> cc = DIVZERO
                if int(ry.value,2) == 0:
                    self.cc.set_state('DIVZERO')
                    txt.insert(INSERT, 'CC State:\t\t\t' + self.cc.state + '\n')
                else:
                    # Rx+1
                    rxx = self.gprs[int(word.rx,2)+1]
                    # Rx = Rx / Ry
                    irr.value = self.alu.arithmetic_cal('/', rx.value, ry.value)
                    txt.insert(INSERT, "IRR <- Rx / Ry\t\t\tIRR = " + irr.value + '\n')
                    rx.value = irr.value
                    txt.insert(INSERT, rx.label + ' <- IRR\t\t\t' + rx.label + ' = ' + rx.value + '\n\n')
                    # Rx+1 <- Rx % Ry
                    irr.value = self.alu.arithmetic_cal('%', rx.value, ry.value)
                    txt.insert(INSERT, "IRR <- Rx % Ry\t\t\tIRR = " + irr.value + '\n')
                    rxx.value = irr.value
                    txt.insert(INSERT, rxx.label + ' <- IRR\t\t\t' + rxx.label + ' = ' + rxx.value + '\n\n')
        # TRR: cc(4)=1 if c(Rx)=c(Ry) else cc(r)=0
        elif op == 18:
            if int(rx.value,2) == int(ry.value,2):
                self.cc.set_state('EQUALORNOT')
                txt.insert(INSERT, rx.label + ' = ' + ry.label + ' :\t\t\t' + rx.get_value() + ' = ' + ry.get_value() + '\n')
                txt.insert(INSERT, 'CC State:\t\t\t' + self.cc.state + '\n')
            else:
                self.cc.reset()
                txt.insert(INSERT, rx.label + ' != ' + ry.label + ' :\t\t\t' + rx.get_value() + ' != ' + ry.get_value() + '\n')
                txt.insert(INSERT, 'CC State:\t\t\t' + self.cc.state + '\n')
        # AND: c(Rx)=c(Rx) AND c(Ry)
        elif op == 19:
            txt.insert(INSERT, rx.label + ' :\t\t\t' + rx.value + '\n')
            txt.insert(INSERT, ry.label + ' :\t\t\t' + ry.value + '\n')
            irr.value = self.alu.logic_cal('&', rx.value, ry.value)
            txt.insert(INSERT,'IRR = Rx & Ry :\t\t\t' + irr.value.zfill(irr.size) + '\n')
            rx.value = irr.value
            txt.insert(INSERT, rx.label + ' <- IRR\t\t\t' + rx.label + ' = ' + rx.value + '\n\n')
        # ORR: c(Rx)=c(Rx) OR c(Ry)
        elif op == 20:
            txt.insert(INSERT, rx.label + ' :\t\t\t' + rx.value + '\n')
            txt.insert(INSERT, ry.label + ' :\t\t\t' + ry.value + '\n')
            irr.value = self.alu.logic_cal('|', rx.value, ry.value)
            txt.insert(INSERT,'IRR = Rx | Ry :\t\t\t' + irr.value.zfill(irr.size) + '\n')
            rx.value = irr.value
            txt.insert(INSERT, rx.label + ' <- IRR\t\t\t' + rx.label + ' = ' + rx.value + '\n\n')
        # NOT: c(Rx)=NOT c(Rx)
        elif op == 21:
            txt.insert(INSERT, rx.label + ' :\t\t\t' + rx.value + '\n')
            irr.value = self.alu.logic_cal('NOT', rx.value)
            txt.insert(INSERT,'IRR = ~ Rx  :\t\t\t' + irr.value.zfill(irr.size) + '\n')
            rx.value = irr.value
            txt.insert(INSERT, rx.label + ' <- IRR\t\t\t' + rx.label + ' = ' + rx.value + '\n\n')
        # SRC: c(R) is shifted left(L/R=1) or right(L/R=0) either logically(A/L=1) or arithmetically(A/L=0)
        elif op == 25:
            lr = 'left' if l_r == 1 else 'right'
            al = 'logically' if a_l == 1 else 'arithmetically'
            txt.insert(INSERT, gpr.label + ' is shifted ' + lr + ' ' + al + '\n')
            gpr.value = self.alu.shift(gpr.value.zfill(gpr.size), count, l_r, a_l)
            txt.insert(INSERT, gpr.label + ' :\t\t\t' + gpr.value + '\n')
            txt.insert(INSERT, 'CC State:\t\t\t' + self.cc.state + '\n')
        # RRC: c(R) is Rotated left(L/R=1) or right(L/R=0) either logically(A/L=1)
        elif op == 26:
            al = 'logically' if a_l == 1 else 'arithmetically'
            lr = 'left' if l_r == 1 else 'right'
            txt.insert(INSERT, gpr.label + ' is rotated ' + lr + ' ' + al + '\n')
            gpr.value = self.alu.rotate(gpr.value.zfill(gpr.size), count, l_r, a_l)
            txt.insert(INSERT, gpr.label + ' :\t\t\t' + gpr.value + '\n')
            txt.insert(INSERT, 'CC State:\t\t\t' + self.cc.state + '\n')
        # LDX
        elif op == 33:
            # MBR <- MEM[MAR]
            self.mbr.load_from_mem(self.mar,self.mem)
            txt.insert(INSERT, 'MBR <- MEM[' + self.mar.get_value() + '] :\t\t\tMBR = ' + self.mbr.value + '\n')
            # IRR <- MBR
            irr.value = self.mbr.value
            txt.insert(INSERT, 'IRR <- MBR :\t\t\tIRR = ' + irr.value + '\n')
            # X[IXR] <- IRR
            ixr.value = irr.value
            txt.insert(INSERT, ixr.label + ' <- IRR :\t\t\t' + ixr.label + ' = ' + ixr.value + '\n')
        # STX
        elif op == 34:
            # IRR <- X[IXR]
            irr.value = ixr.value
            txt.insert(INSERT, 'IRR <- ' + ixr.label + ' :\t\t\tIRR = ' + irr.value + '\n')
            # MBR <- IRR
            self.mbr.value = irr.value
            txt.insert(INSERT, 'MBR <- IRR :\t\t\tMBR = ' + self.mbr.value + '\n')
            # MEM[MAR] <- MBR
            self.mbr.store_to_mem(self.mar, self.mem)
            txt.insert(INSERT, 'MEM['+ self.mar.value.get_value() + '] <- MBR :\t\t\tMEM['+self.mar.value.get_value() + '] = ' + self.mem.memory[int(self.mar.value,2)] + '\n')
        # IN: R[GPR] <- In
        elif op == 49:
            txt.insert(INSERT, 'Please Input A Number\n\n')
            if self.keyboard.write(input):
                gpr.reset()
                gpr.add_10(self.keyboard.read())
                txt.insert(INSERT, gpr.label + ' <- Input :\t\t\t' + gpr.label + ' = ' + gpr.get_value() + '\n')
            else:
                txt.insert(INSERT, 'Invalid Input\n')
                gpr.reset()
        # OUT: Out <- R[GPR]
        elif op == 50:
            self.printer.write_line(gpr.get_value())
            output.configure(state='normal')
            output.delete(1.0, END)
            output.insert(INSERT, self.printer.read_content())
            output.yview_moveto('1.0')
            output.configure(state='disabled')
            txt.insert(INSERT, 'Output <- '+ gpr.label + ' :\t\t\tOutput ' + self.printer.read_line() +  '\n')

    def single_step(self, txt, input, output):
        """This function implements the single step
        It's called in GUI.func_ss
        """
        # Fetch
        self.__fetch(txt)
        # Decode
        word = self.__decode(txt)
        op = int(word.opcode, 2)
        # Halt if op = 0
        if op == 0:
            txt.insert(INSERT, 'Program is done\n\n')
            return 'DONE'
        # EA Compute: for some operation x, i are ignored, which means no EA needed
        if op not in [6, 7, 13, 16, 17, 18, 19, 20, 21, 25, 26, 49, 50]:
            self.__locate(txt, word)
        # Excute and Deposit
        self.__execute_deposit(txt, word, input, output)
        # PC++: for some operation, pc++ is not needed
        if op not in [8,9,10,11,12,14,15]:
            self.pc.next()
            txt.insert(INSERT, '\nPC++ :\t\t\tPC = ' + self.pc.value + '\n\n')

    def test_ins(self, ins, txt, input, output):
        """This function implements testing of input instrucitons
        It's called in GUI.func_test
        """
        i = Instruction()
        msg = i.decode_test(ins)
        txt.insert(INSERT, msg)
        if msg == 'Decoding Complete\n\n':
            # for some operation x, i are ignored, which means no EA needed
            if int(i.opcode,2) not in [6, 7, 13, 16, 17, 18, 19, 20, 21, 25, 26, 49, 50]:
                self.__locate(txt, i)
            self.__execute_deposit(txt, i, input, output)
