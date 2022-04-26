# -----------------------------------------------------------------
# @Author:     Tenphun0503
# This file implements the main logic of the system
# -----------------------------------------------------------------
from CPU.ALU import *
from CPU.instruction import *
from GUI import *
from Memory.cache import *
from ioDevice import *


class System:
    def __init__(self, file_dir, pc_default, text_dir=None):
        # initialize cache
        self.cache = Cache()
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
        self.fpr0 = FPR(label='FPR0')
        self.fpr1 = FPR(label='FPR1')
        # initialize ALU
        self.alu = ALU(self.cc)
        # initialize io devices
        self.keyboard = Keyboard()
        self.printer = Printer()
        self.reader = Reader()

        # for refreshing
        self.registers = [self.gpr0, self.gpr1, self.gpr2, self.gpr3, self.x1, self.x2, self.x3,
                          self.pc, self.mar, self.mbr, self.fpr0, self.fpr1, self.ir, self.mfr, self.cc]
        self.gprs = [self.gpr0, self.gpr1, self.gpr2, self.gpr3]
        self.xs = [self.x1, self.x2, self.x3]
        self.fprs = [self.fpr0, self.fpr1]

        self.file_dir = file_dir
        self.pc_default = pc_default
        self.text_dir = text_dir
        self.pnum = 0
        self.content = None

        # TODO: add mfr, like cc, 4 digits code
        # 0001: Illegal Memory Address to Reserved locations
        # 0010: Illegal TRAP code
        # 0100: Illegal Operation code
        # 1000: Illegal Memory Address beyond 2048

    def reset(self, output):
        """This function resets the system
        It's called in GUI.resets
        """
        self.cache.reset()
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
        """This function sets the bit of instruction into 1 or 0
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
        """This function loads register with the value of the instruction
        It's called in GUI.func_reg_load
        """
        reg = self.registers[index]
        reg.value = self.ins.value[16 - reg.size:16]
        txt.insert(INSERT, reg.label + '<-' + str(int(reg.value)))

    def load(self, txt):
        """MBR <- MEM[MAR]
        It's called in GUI.func_reg_load
        """
        txt.insert(INSERT, 'MBR <- MEM[MAR]:\n')
        self.mbr.value = self.cache.get(int(self.mar.value, 2))
        txt.insert(INSERT, 'MBR <- ' + self.cache.msg)

    def store(self, txt):
        """MEM[MAR] <- MBR
        It's called in GUI.fun_store
        """
        txt.insert(INSERT, 'MEM[MAR] <- MBR:\n')
        self.cache.set(int(self.mar.value, 2), self.mbr.value)
        txt.insert(INSERT, self.cache.msg)

    def st_plus(self, txt):
        """MEM[MAR] <- MBR; MAR++
        It's called in GUI.fun_st_plus
        """
        txt.insert(INSERT, 'MEM[MAR] <- MBR:\n')
        self.cache.set(int(self.mar.value, 2), self.mbr.value)
        txt.insert(INSERT, self.cache.msg)
        txt.insert(INSERT, 'MAR++:\n')
        self.mar.add_10(1)
        txt.insert(INSERT, 'MAR = ' + str(int(self.mar.value)) + '\n')

    def load_pg1(self, txt_ipl_info, txt_step_info):
        """Preload the program1
        It's called in GUI.func_pg1
        """
        try:
            with open('program1.txt', 'r') as f:
                lines = f.readlines()
            f.close()
        except FileNotFoundError:
            txt_ipl_info.insert(INSERT, 'Program1.txt does not exist')
            return

        for i in lines:
            i = i.replace('\n', '')
            if i == '':
                continue
            # ipl_info update
            txt_ipl_info.insert(INSERT, i + '\n')
            # mem[add] <- value
            temp = i.split(' ')
            if temp[0] == '#':
                continue
            add, value = int(temp[0], 16), bin(int(temp[1][0:4], 16))[2:]
            self.cache.mem.set_to_memory(add, value)
            # step_info update
            txt_step_info.insert(INSERT, f'MEM[{str(add)}] = {value}\n')

        # set pc by default
        self.pc.value = bin(6)[2:]
        txt_step_info.insert(INSERT, 'PC has been set to ' + self.pc.value)
        self.pnum = 1

    def load_pg2(self, txt_ipl_info, txt_step_info):
        """Preload the program2
        It's called in GUI.func_pg2
        """
        try:
            with open('program2.txt', 'r') as f:
                lines = f.readlines()
            f.close()
        except FileNotFoundError:
            txt_ipl_info.insert(INSERT, 'Program2.txt does not exist')
            return

        for i in lines:
            i = i.replace('\n', '')
            if i == '':
                continue
            # ipl_info update
            txt_ipl_info.insert(INSERT, i + '\n')
            # mem[add] <- value
            temp = i.split(' ')
            if temp[0] == '#':
                continue
            add, value = int(temp[0], 16), bin(int(temp[1][0:4], 16))[2:]
            self.cache.mem.set_to_memory(add, value)
            # step_info update
            txt_step_info.insert(INSERT, f'MEM[{str(add)}] = {value}\n')

        # set pc by default
        self.pc.value = bin(6)[2:]
        txt_step_info.insert(INSERT, 'PC has been set to ' + self.pc.value)
        self.text_dir = 'test.txt'
        self.pnum = 2

    def load_file(self, txt_ipl_info, txt_step_info):
        """Preload the file
        It's called in GUI.fun_ipl
        """
        try:
            with open(self.file_dir, 'r') as f:
                lines = f.readlines()
            f.close()
        except FileNotFoundError:
            txt_ipl_info.insert(INSERT, self.file_dir + ' does not exist')
            return

        for i in lines:
            i = i.replace('\n', '')
            if i == '':
                continue
            # ipl_info update
            txt_ipl_info.insert(INSERT, i + '\n')
            # mem[add] <- value
            temp = i.split(' ')
            if temp[0] == '#':
                continue
            add, value = int(temp[0], 16), bin(int(temp[1][0:4], 16))[2:]
            self.cache.mem.set_to_memory(add, value)
            # step_info update
            # TODO: update all of the text info
            txt_step_info.insert(INSERT, f'MEM[{str(add)}] = {value}\n')

        # set pc by default
        self.pc.value = bin(self.pc_default)[2:]
        txt_step_info.insert(INSERT, 'PC has been set to ' + self.pc.value)

    def __fetch(self, txt):
        """Fetching of instruction"""
        txt.insert(INSERT, 'Fetch Instruction \n')
        # MAR <- PC
        self.mar.get_from_PC(self.pc)
        txt.insert(INSERT, 'MAR <- PC :\t\t\t' + self.mar.value + '\n')
        # MBR <- mem[MAR]
        self.mbr.value = self.cache.get(int(self.mar.value, 2))
        txt.insert(INSERT, 'MBR <- ' + self.cache.msg)
        # IR <- MBR
        self.ir.get_from_MBR(self.mbr)
        txt.insert(INSERT, 'IR <- MBR :\t\t\t' + self.ir.value + '\n\n')

    def __decode(self, txt):
        """Decoding of instruction"""
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
        txt.insert(INSERT, 'IAR <- Add :\t\t\t' + iar.value + '\n')
        # IAR += X[IXR] if IXR = 1 or 2 or 3
        ixr_id = int(word.ixr_index, 2)
        if ixr_id != 0:
            ixr = self.xs[ixr_id - 1]
            iar.value = bin(int(iar.value, 2) + int(ixr.value, 2))[2:]
            txt.insert(INSERT, 'IAR += ' + ixr.label + ' :\t\t\t' + iar.value + '\n')
        # IAR <- MEM[IAR] if I = 1
        if int(word.indirect, 2) == 1:
            add = int(iar.value, 2)
            iar.value = self.cache.get(add)
            txt.insert(INSERT, 'IAR <- ' + self.cache.msg)
        # MAR <- IAR
        self.mar.value = iar.value
        txt.insert(INSERT, 'MAR <- IAR :\t\t\t' + self.mar.value + '\n\n')

    def __execute_deposit(self, txt, word, input, output):
        """The execution and deposition"""
        txt.insert(INSERT, 'Execute and Deposit Result \n')
        irr = Register(16, 'IRR')
        ea = self.mar.value
        op = int(word.opcode, 2)
        if op in [16, 17, 18, 19, 20, 21]:
            rx = self.gprs[int(word.rx, 2)]
            if op != 21:
                ry = self.gprs[int(word.ry, 2)]
        elif op in [25, 26]:
            a_l = int(word.a_l)
            l_r = int(word.l_r)
            count = int(word.count, 2)
            gpr = self.gprs[int(word.gpr_index, 2)]
        # FP and Vector
        elif op in [27, 28, 29, 30, 31, 40, 41]:
            fpr = self.fprs[int(word.fpr_index, 2)]
            ixr = self.xs[int(word.ixr_index, 2) - 1]
        else:
            gpr = self.gprs[int(word.gpr_index, 2)]
            ixr = self.xs[int(word.ixr_index, 2) - 1]
            immed = word.address
            devid = int(word.address, 2)
        # LDR
        if op == 1:
            # MBR <- MEM[MAR]
            self.mbr.value = self.cache.get(int(self.mar.value, 2))
            txt.insert(INSERT, 'MBR <- ' + self.cache.msg)
            # IRR <- MBR
            irr.value = self.mbr.value
            txt.insert(INSERT, 'IRR <- MBR :\t\t\t' + irr.value + '\n')
            # R[GPR] <- IRR
            gpr.value = irr.value
            txt.insert(INSERT, gpr.label + ' <- IRR :\t\t\t' + gpr.value + '\n')
        # STR
        elif op == 2:
            # IRR <- R[GPR]
            irr.value = gpr.value
            txt.insert(INSERT, 'IRR <- ' + gpr.label + ' :\t\t\t' + irr.value + '\n')
            # MBR <- IRR
            self.mbr.value = irr.value
            txt.insert(INSERT, 'MBR <- IRR :\t\t\t' + self.mbr.value + '\n')
            # MEM[MAR] <- MBR
            self.cache.set(int(self.mar.value, 2), self.mbr.value)
            txt.insert(INSERT, self.cache.msg)
        # LDA
        elif op == 3:
            # MBR <- MAR
            self.mbr.value = self.mar.value
            txt.insert(INSERT, 'MBR <- MAR : \t\t\t' + self.mbr.value + '\n')
            # IRR <- MBR
            irr.value = self.mbr.value
            txt.insert(INSERT, 'IRR <- MBR :\t\t\t' + irr.value + '\n')
            # R[GPR] <- IRR
            gpr.value = irr.value
            txt.insert(INSERT, gpr.label + ' <- IRR :\t\t\t' + gpr.value + '\n')
        # AMR: R=c(R)+c(EA)
        elif op == 4:
            # MBR <- MEM[MAR]
            self.mbr.value = self.cache.get(int(self.mar.value, 2))
            txt.insert(INSERT, 'MBR <- ' + self.cache.msg)
            # IRR <- R[GPR] + MBR
            irr.value = self.alu.arithmetic_cal('+', gpr.value, self.mbr.value)
            txt.insert(INSERT, 'IRR <- ' + gpr.label + ' + MBR:\t\t\t' + irr.value + '\n')
            # R[GPR] <- IRR
            gpr.value = irr.value
            txt.insert(INSERT, gpr.label + ' <- IRR :\t\t\t' + gpr.value + '\n')
        # SMR: R=c(R)-c(EA)
        elif op == 5:
            # MBR <- MEM[MAR]
            self.mbr.value = self.cache.get(int(self.mar.value, 2))
            txt.insert(INSERT, 'MBR <- ' + self.cache.msg)
            # IRR <- R[GPR] - MBR
            irr.value = self.alu.arithmetic_cal('-', gpr.value, self.mbr.value)
            txt.insert(INSERT, 'IRR <- ' + gpr.label + ' - MBR:\t\t\t' + irr.value + '\n')
            # R[GPR] <- IRR
            gpr.value = irr.value
            txt.insert(INSERT, gpr.label + ' <- IRR :\t\t\t' + gpr.value + '\n')
        # AIR: R=c(R)+Immed
        elif op == 6:
            # IRR <- R[GPR] + Immed
            irr.value = self.alu.arithmetic_cal('+', gpr.value, immed)
            txt.insert(INSERT, 'IRR <- ' + gpr.label + ' + Immed:\t\t\t' + irr.value + '\n')
            # R[GPR] <- IRR
            gpr.value = irr.value
            txt.insert(INSERT, gpr.label + ' <- IRR :\t\t\t' + gpr.value + '\n')
        # SIR: R=c(R)-Immed
        elif op == 7:
            # IRR <- R[GPR] - Immed
            irr.value = self.alu.arithmetic_cal('-', gpr.value, immed)
            txt.insert(INSERT, 'IRR <- ' + gpr.label + ' - Immed:\t\t\t' + irr.value + '\n')
            # R[GPR] <- IRR
            gpr.value = irr.value
            txt.insert(INSERT, gpr.label + ' <- IRR :\t\t\t' + gpr.value + '\n')
        # JZ: PC=EA if c(R)=0 else PC++
        elif op == 8:
            txt.insert(INSERT, gpr.label + ' = ' + str(int(gpr.value)) + '\t\t\t')
            if int(gpr.value, 2) == 0:
                txt.insert(INSERT, '== 0\n')
                self.pc.value = ea
                txt.insert(INSERT, 'PC <- EA :\t\t\t' + self.pc.value + '\n\n')
            else:
                txt.insert(INSERT, '!= 0\n')
                self.pc.next()
                txt.insert(INSERT, 'PC ++ :\t\t\t' + self.pc.value + '\n\n')
        # JNE: PC=EA if c(R)!=0 else PC++
        elif op == 9:
            txt.insert(INSERT, gpr.label + ' = ' + str(int(gpr.value)) + '\t\t\t')
            if int(gpr.value, 2) != 0:
                txt.insert(INSERT, '!= 0\n')
                self.pc.value = ea
                txt.insert(INSERT, 'PC <- EA :\t\t\t' + self.pc.value + '\n\n')
            else:
                txt.insert(INSERT, '== 0\n')
                self.pc.next()
                txt.insert(INSERT, 'PC++ :\t\t\t' + self.pc.value + '\n\n')
        # JCC: PC=EA if CC[r]=1 else PC++
        elif op == 10:
            index = int(word.gpr_index, 2)
            txt.insert(INSERT, 'CC[' + str(index) + '] = ' + self.cc.value[index] + '\t\t\t')
            if self.cc.value[index] == '1':
                txt.insert(INSERT, '== 1\n')
                self.pc.value = ea
                txt.insert(INSERT, 'PC <- EA :\t\t\t' + self.pc.value + '\n\n')
            else:
                txt.insert(INSERT, '!= 1\n')
                self.pc.next()
                txt.insert(INSERT, 'PC++ :\t\t\t' + self.pc.value + '\n\n')
        # JMA:
        elif op == 11:
            # PC <- EA
            self.pc.value = ea
            txt.insert(INSERT, 'PC <- EA :\t\t\t' + self.pc.value + '\n\n')
        # JSR:
        elif op == 12:
            # PC ++
            self.pc.next()
            txt.insert(INSERT, 'PC++ :\t\t\t' + self.pc.value + '\n')
            # R[3] <- PC
            self.gpr3.value = self.pc.value
            txt.insert(INSERT, 'GPR3 <- PC :\t\t\t' + self.gpr3.value + '\n')
            # PC <- EA
            self.pc.value = ea
            txt.insert(INSERT, 'PC <- EA :\t\t\t' + self.pc.value + '\n\n')
        # RFS:
        elif op == 13:
            # R[0] <- Immed
            self.gpr0.value = immed
            txt.insert(INSERT, 'GPR0 <- Immed :\t\t\t' + self.gpr0.value + '\n')
            # PC <- R[3]
            # if R[3].len > pc.size: pc=c(r3)[-pc.size:]
            self.pc.value = str(int(self.gpr3.value[-self.pc.size:]))
            txt.insert(INSERT, 'PC <- GPR3 :\t\t\t' + self.pc.value + '\n\n')
        # SOB: c(R)=c(R)-1; PC=EA if C(R)>0 else PC++
        elif op == 14:
            # R[GPR] --
            gpr.value = self.alu.arithmetic_cal('-', gpr.value, '1')
            # the real decimal result of subtraction
            gpr_value = self.alu.value
            txt.insert(INSERT, gpr.label + '-- = ' + str(gpr_value) + '\t\t\t')
            if gpr_value > 0:
                txt.insert(INSERT, '> 0\n')
                self.pc.value = ea
                txt.insert(INSERT, 'PC <- EA : \t\t\t' + self.pc.value + '\n\n')
            else:
                txt.insert(INSERT, '<= 0\n')
                self.pc.next()
                txt.insert(INSERT, 'PC++ : \t\t\t' + self.pc.value + '\n\n')
        # JGE: PC=EA if c(R)>=0 else PC++
        elif op == 15:
            txt.insert(INSERT, gpr.label + ' = ' + str(int(gpr.value)) + '\t\t\t')
            if int(gpr.value, 2) >= 0:
                txt.insert(INSERT, '>= 0\n')
                self.pc.value = ea
                txt.insert(INSERT, 'PC <- EA : \t\t\t' + self.pc.value + '\n\n')
            else:
                txt.insert(INSERT, '< 0\n')
                self.pc.next()
                txt.insert(INSERT, 'PC++ : \t\t\t' + self.pc.value + '\n\n')
        # MLT: Rx, Rx+1=c(Rx)*(Ry)
        elif op == 16:
            if int(word.rx, 2) not in [0, 2] or int(word.ry, 2) not in [0, 2]:
                txt.insert(INSERT, "Rx, Ry must be 0 or 2\n")
            else:
                txt.insert(INSERT,
                           rx.label + ' * ' + ry.label + ' :\t\t\t' + rx.get_value() + ' * ' + ry.get_value() + '\n')
                res = self.alu.arithmetic_cal('*', rx.value, ry.value).zfill(32)
                # IRR = Higher bits of Rx * Ry
                irr.value = res[:16]
                txt.insert(INSERT, "IRR <- High(Rx * Ry)\t\t\t" + irr.value + '\n')
                # Rx = IRR
                rx.value = irr.value
                txt.insert(INSERT, rx.label + ' <- IRR\t\t\t' + rx.value + '\n\n')
                # IRR = Lower bits of Rx * Ry
                irr.value = res[16:]
                txt.insert(INSERT, "IRR <- Low(Rx * Ry)\t\t\t" + irr.value + '\n')
                # Rx+1 = IRR
                rxx = self.gprs[int(word.rx, 2) + 1]
                rxx.value = irr.value
                txt.insert(INSERT, rxx.label + ' <- IRR\t\t\t' + rxx.value + '\n\n')
                # CC state
                txt.insert(INSERT, 'CC State:\t\t\t' + self.cc.state + '\n')
        # DVD: Rx, Rx+1=c(Rx)/(Ry)
        elif op == 17:
            if int(word.rx, 2) not in [0, 2] or int(word.ry, 2) not in [0, 2]:
                txt.insert(INSERT, "Rx, Ry must be 0 or 2\n")
            else:
                txt.insert(INSERT,
                           rx.label + ' / ' + ry.label + ' :\t\t\t' + rx.get_value() + ' / ' + ry.get_value() + '\n')
                # Ry = 0 -> cc = DIVZERO
                if int(ry.value, 2) == 0:
                    self.cc.set_state('DIVZERO')
                    # CC state
                    txt.insert(INSERT, 'CC State:\t\t\t' + self.cc.state + '\n')
                else:
                    # Rx+1 <- Rx % Ry
                    irr.value = self.alu.arithmetic_cal('%', rx.value, ry.value)
                    txt.insert(INSERT, "IRR <- Rx % Ry\t\t\t" + irr.value + '\n')
                    # Rxx = IRR
                    rxx = self.gprs[int(word.rx, 2) + 1]
                    rxx.value = irr.value
                    txt.insert(INSERT, rxx.label + ' <- IRR\t\t\t' + rxx.value + '\n\n')
                    # IRR = Rx / Ry
                    irr.value = self.alu.arithmetic_cal('/', rx.value, ry.value)
                    txt.insert(INSERT, "IRR <- Rx / Ry\t\t\t" + irr.value + '\n')
                    # Rx = IRR
                    rx.value = irr.value
                    txt.insert(INSERT, rx.label + ' <- IRR\t\t\t' + rx.value + '\n\n')
        # TRR: cc(4)=1 if c(Rx)=c(Ry) else cc(r)=0
        elif op == 18:
            if int(rx.value, 2) == int(ry.value, 2):
                txt.insert(INSERT,
                           rx.label + ' = ' + ry.label + ' :\t\t\t' + rx.get_value() + ' = ' + ry.get_value() + '\n')
                self.cc.set_state('EQUALORNOT')
                txt.insert(INSERT, 'CC State:\t\t\t' + self.cc.state + '\n')
            else:
                txt.insert(INSERT,
                           rx.label + ' != ' + ry.label + ' :\t\t\t' + rx.get_value() + ' != ' + ry.get_value() + '\n')
                self.cc.reset()
                txt.insert(INSERT, 'CC State:\t\t\t' + self.cc.state + '\n')
        # AND: c(Rx)=c(Rx) AND c(Ry)
        elif op == 19:
            txt.insert(INSERT, rx.label + ' :\t\t\t' + rx.value + '\n')
            txt.insert(INSERT, ry.label + ' :\t\t\t' + ry.value + '\n')
            # IRR = Rx & Ry
            irr.value = self.alu.logic_cal('&', rx.value, ry.value)
            txt.insert(INSERT, 'IRR = Rx & Ry :\t\t\t' + irr.value.zfill(irr.size) + '\n')
            # Rx = IRR
            rx.value = irr.value
            txt.insert(INSERT, rx.label + ' <- IRR\t\t\t' + rx.value + '\n\n')
        # ORR: c(Rx)=c(Rx) OR c(Ry)
        elif op == 20:
            txt.insert(INSERT, rx.label + ' :\t\t\t' + rx.value + '\n')
            txt.insert(INSERT, ry.label + ' :\t\t\t' + ry.value + '\n')
            # IRR = Rx | Ry
            irr.value = self.alu.logic_cal('|', rx.value, ry.value)
            txt.insert(INSERT, 'IRR = Rx | Ry :\t\t\t' + irr.value.zfill(irr.size) + '\n')
            # Rx = IRR
            rx.value = irr.value
            txt.insert(INSERT, rx.label + ' <- IRR\t\t\t' + rx.value + '\n\n')
        # NOT: c(Rx)=NOT c(Rx)
        elif op == 21:
            txt.insert(INSERT, rx.label + ' :\t\t\t' + rx.value + '\n')
            # IRR = ~ Rx
            irr.value = self.alu.logic_cal('~', rx.value)
            txt.insert(INSERT, 'IRR = NOT Rx  :\t\t\t' + irr.value.zfill(irr.size) + '\n')
            # Rx = IRR
            rx.value = irr.value
            txt.insert(INSERT, rx.label + ' <- IRR\t\t\t' + rx.value + '\n\n')
        # Trap
        elif op == 24:
            # trap_code = int(word.trap_code, 2)
            # self.pc.next()
            # self.cache.set(2, self.pc.value)
            # txt.insert(INSERT, self.cache.msg)
            # self.pc.value = self.cache.get(0)
            # txt.insert(INSERT, f'Address of Routine Table : {self.pc.get_value()}\n')
            # self.pc.add_10(trap_code)
            # txt.insert(INSERT, f'Address of Routine {trap_code} :\t\t\tPC = {self.pc.get_value()}\n')
            # self.pc.value = self.cache.get(int(self.pc.value, 2))
            # txt.insert(INSERT, f'Set to address :\t\t\t PC = {self.pc.get_value()}\n\n')
            self.reader.read_file(self.text_dir)
            self.content = list(self.reader.content[0])
            for i, character in enumerate(self.content):
                self.cache.set(1100+i, bin(ord(character))[2:])
            self.printer.write_paragraph(self.reader.content[0])
            output.configure(state='normal')
            output.delete(1.0, END)
            output.insert(INSERT, self.printer.read_content())
            output.yview_moveto('1.0')
            output.configure(state='disabled')
            self.pc.next()

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
            lr = 'left' if l_r == 1 else 'right'
            al = 'logically' if a_l == 1 else 'arithmetically'
            txt.insert(INSERT, gpr.label + ' is rotated ' + lr + ' ' + al + '\n')
            gpr.value = self.alu.rotate(gpr.value.zfill(gpr.size), count, l_r, a_l)
            txt.insert(INSERT, gpr.label + ' :\t\t\t' + gpr.value + '\n')
            txt.insert(INSERT, 'CC State:\t\t\t' + self.cc.state + '\n')
        # FADD
        elif op == 27:
            # MBR <- MEM[MAR]
            self.mbr.value = self.cache.get(int(self.mar.value, 2)).zfill(16)
            txt.insert(INSERT, f'MBR <- {self.cache.msg}')
            # IRR <- FPR + MBR
            irr.value = self.alu.fp_cal('+', fpr.value, self.mbr.value).zfill(16)
            txt.insert(INSERT, f'IRR <- {fpr.label} + MBR:\t\t\t{irr.value}\n')
            txt.insert(INSERT, f'{round(fpr.update(), 1)} + {round(self.translate(self.mbr.value), 1)}:'
                               f'\t\t\t{round(self.alu.value, 1)}\n')
            # FPR <- IRR
            fpr.value = irr.value
            txt.insert(INSERT, f'{fpr.label} <- IRR :\t\t\t{fpr.value}\n')
            # set CC
            if self.cc.value[0] == '1':
                txt.insert(INSERT, 'OVERFLOWED')
        # FSUB
        elif op == 28:
            # MBR <- MEM[MAR]
            self.mbr.value = self.cache.get(int(self.mar.value, 2)).zfill(16)
            txt.insert(INSERT, f'MBR <- {self.cache.msg}')
            # IRR <- FPR - MBR
            irr.value = self.alu.fp_cal('-', fpr.value, self.mbr.value).zfill(16)
            txt.insert(INSERT, f'IRR <- {fpr.label} + MBR:\t\t\t{irr.value}\n')
            txt.insert(INSERT, f'{round(fpr.update(), 1)} - {round(self.translate(self.mbr.value), 1)}:'
                               f'\t\t\t{round(self.alu.value, 1)}\n')
            # FPR <- IRR
            fpr.value = irr.value
            txt.insert(INSERT, f'{fpr.label} <- IRR :\t\t\t{fpr.value}\n')
            # set CC
            if self.cc.value[1] == '1':
                txt.insert(INSERT, 'UNDERFLOWED')
        # VADD
        elif op == 29:
            v1_start = int(self.cache.get(int(self.mar.value, 2)), 2)
            txt.insert(INSERT, f'Vector 1 starts from {v1_start}\n')
            v2_start = int(self.cache.get(int(self.mar.value, 2) + 1), 2)
            txt.insert(INSERT, f'Vector 2 starts from {v2_start}\n')
            step = int(fpr.value, 2)
            txt.insert(INSERT, f'Length of the vector is {step}\n')
            for i in range(step):
                v1 = self.cache.get(v1_start + i).zfill(16)
                v2 = self.cache.get(v2_start + i).zfill(16)
                irr.value = self.alu.fp_cal('+', v1, v2)
                txt.insert(INSERT, f'V1[{i+1}] <- V1[{i+1}] + V2[{i+1}]:\t\t\t')
                txt.insert(INSERT, f'{round(self.translate(v1), 1)} + {round(self.translate(v2), 1)} = '
                                   f'{round(self.alu.value, 1)}\n')
                self.cache.set(v1_start + i, irr.value)
        # VSUB
        elif op == 30:
            v1_start = int(self.cache.get(int(self.mar.value, 2)), 2)
            txt.insert(INSERT, f'Vector 1 starts from {v1_start}\n')
            v2_start = int(self.cache.get(int(self.mar.value, 2) + 1), 2)
            txt.insert(INSERT, f'Vector 2 starts from {v2_start}\n')
            step = int(fpr.value, 2)
            txt.insert(INSERT, f'Length of the vector is {step}\n')
            for i in range(step):
                v1 = self.cache.get(v1_start + i).zfill(16)
                v2 = self.cache.get(v2_start + i).zfill(16)
                irr.value = self.alu.fp_cal('-', v1, v2)
                txt.insert(INSERT, f'V1[{i+1}] <- V1[{i+1}] - V2[{i+1}]:\t\t\t')
                txt.insert(INSERT, f'{round(self.translate(v1), 1)} - {round(self.translate(v2), 1)} = '
                                   f'{round(self.alu.value, 1)}\n')
                self.cache.set(v1_start + i, irr.value)
        # CNVRT
        elif op == 31:
            flag = int(fpr.value, 2)
            # MBR <- MEM[MAR]
            self.mbr.value = self.cache.get(int(self.mar.value, 2)).zfill(16)
            txt.insert(INSERT, f'MBR <- {self.cache.msg}')
            fpr.value = self.mbr.value
            # convert to a fixed number
            if flag == 0:
                v = fpr.update()
                fpr.value = fpr.convert(v)
                txt.insert(INSERT, f'{round(v, 2)} converted to {fpr.value}\n')
            # convert to a floating point and store in fr0
            else:
                v = fpr.reverse_convert(fpr.value)
                self.fpr0.value = fpr.encode(v)
                fpr.value = '1'
                txt.insert(INSERT, f'{round(v, 2)} converted to {self.fpr0.value}\n')
        # LDX
        elif op == 33:
            # MBR <- MEM[MAR]
            self.mbr.value = self.cache.get(int(self.mar.value, 2))
            txt.insert(INSERT, 'MBR <- ' + self.cache.msg)
            # IRR <- MBR
            irr.value = self.mbr.value
            txt.insert(INSERT, 'IRR <- MBR :\t\t\t' + irr.value + '\n')
            # X[IXR] <- IRR
            ixr.value = irr.value
            txt.insert(INSERT, ixr.label + ' <- IRR :\t\t\t' + ixr.value + '\n')
        # STX
        elif op == 34:
            # IRR <- X[IXR]
            irr.value = ixr.value
            txt.insert(INSERT, 'IRR <- ' + ixr.label + ' :\t\t\t' + irr.value + '\n')
            # MBR <- IRR
            self.mbr.value = irr.value
            txt.insert(INSERT, 'MBR <- IRR :\t\t\t' + self.mbr.value + '\n')
            # MEM[MAR] <- MBR
            self.cache.set(int(self.mar.value, 2), self.mbr.value)
            txt.insert(INSERT, self.cache.msg)
        # LDFR
        elif op == 40:
            # MBR <- MEM[MAR]
            self.mbr.value = self.cache.get(int(self.mar.value, 2)).zfill(16)
            txt.insert(INSERT, f'MBR <- {self.cache.msg}')
            # IRR <- MBR
            irr.value = self.mbr.value
            txt.insert(INSERT, f'IRR <- MBR :\t\t\t{irr.value}\n')
            # FPR <- IRR
            fpr.value = irr.value
            txt.insert(INSERT, f'{fpr.label} <- IRR :\t\t\t{fpr.value}\n')
        # STFR
        elif op == 41:
            # IRR <- R[GPR]
            irr.value = gpr.value
            txt.insert(INSERT, f'IRR <- {gpr.label} :\t\t\t{irr.value}\n')
            # MBR <- IRR
            self.mbr.value = irr.value
            txt.insert(INSERT, 'MBR <- IRR :\t\t\t{self.mbr.value}\n')
            # MEM[MAR] <- MBR
            self.cache.set(int(self.mar.value, 2), self.mbr.value)
            txt.insert(INSERT, self.cache.msg)
        # IN: R[GPR] <- In
        elif op == 49:
            # keyboard
            if devid == 0:
                txt.insert(INSERT, 'Please input')
                if self.keyboard.write(input):
                    gpr.reset()
                    character = self.keyboard.read()
                    if self.pnum == 1:
                        gpr.add_10(int(character))
                    else:
                        gpr.add_10(ord(character))
                    txt.insert(INSERT, gpr.label + f' <- {character} :\t\t\t' + gpr.label + ' = ' + gpr.get_value() + '\n')
                else:
                    txt.insert(INSERT, 'Invalid Input\n')
                    gpr.reset()
            elif devid == 2:
                character = self.content.pop(0)
                txt.insert(INSERT, f"Read '{character}'\n")
                gpr.value = bin(ord(character))[2:]
                txt.insert(INSERT, f'{gpr.label} <- Read :\t\t\t{gpr.value}\n')

        # OUT: Out <- R[GPR]
        elif op == 50:
            self.printer.write_line(self.pnum, gpr.get_value())
            output.configure(state='normal')
            output.delete(1.0, END)
            output.insert(INSERT, self.printer.read_content())
            output.yview_moveto('1.0')
            output.configure(state='disabled')
            txt.insert(INSERT, f'Output <- {gpr.label} :\t\t\tOutput {self.printer.read_line()}\n')
        # CHK
        elif op == 51:
            # reader: check if file is existed
            if devid == 2:
                self.reader.reset()
                self.reader.read_file(self.text_dir)
                self.content = list(self.reader.content[0])
                txt.insert(INSERT, self.reader.msg)
                gpr.value = self.reader.flag
                txt.insert(INSERT, f'{gpr.label} set by status :\t\t\t{gpr.value}')

    def translate(self, fp):
        fp = fp.zfill(16)
        s = int(fp[0], 2)
        e = int(fp[1:8], 2) - 63
        m = 1
        for id, i in enumerate(fp[8:]):
            m += int(i) * (1 / (2 ** (id + 1)))
        value = ((-1) ** s) * m * (2 ** e)
        return value

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
        # EA Compute: for some operation 'x' and 'i' are ignored, which means no EA needed
        if op not in [6, 7, 13, 16, 17, 18, 19, 20, 21, 25, 26, 49, 50, 51]:
            self.__locate(txt, word)
        # Execute and Deposit
        self.__execute_deposit(txt, word, input, output)
        # PC++: for some operation, pc++ is not needed
        if op not in [8, 9, 10, 11, 12, 14, 15, 24]:
            self.pc.next()
            txt.insert(INSERT, '\nPC++ :\t\t\tPC = ' + self.pc.value + '\n\n')

    def test_ins(self, ins, txt, input, output):
        """This function implements testing of input instructions
        It's called in GUI.func_test
        """
        i = Instruction()
        msg = i.decode_test(ins)
        txt.insert(INSERT, msg)
        if msg == 'Decoding Complete\n\n':
            # for some operation 'x' and 'i' are ignored, which means no EA needed
            if int(i.opcode, 2) not in [6, 7, 13, 16, 17, 18, 19, 20, 21, 24, 25, 26, 49, 50, 51]:
                self.__locate(txt, i)
            self.__execute_deposit(txt, i, input, output)
