#-----------------------------------------------------------------
# @Author :     Tenphun0503
# This file implements the main logic of the system
#-----------------------------------------------------------------
import time
from GUI import *
from CPU.registers import *
from memory import *
from instruction import *

class System:
    def __init__(self):
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

        # for refreshing
        self.registers = [self.gpr0, self.gpr1, self.gpr2, self.gpr3, self.x1, self.x2, self.x3,
                            self.pc, self.mar, self.mbr, self.ir, self.mfr, self.cc]
        self.gprs = [self.gpr0, self.gpr1, self.gpr2, self.gpr3]
        self.xs = [self.x1, self.x2, self.x3]

    def reset(self):
        """This function resets the system
        It's called in GUI.resets
        """
        self.mem.reset_memory()
        for reg in self.registers:
            reg.reset()
        self.ins.reset()

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
        txt.insert(INSERT, 'MBR = MEM[' + str(int(self.mar.value, 2)
                                              ) + '] = ' + str(int(self.mbr.value)) + '\n')

    def store(self, txt):
        """MEM[MAR] <- MBR
        It's called in GUI.fun_store
        """
        txt.insert(INSERT, 'MEM[MAR] <- MBR:\n')
        self.mbr.store_to_mem(self.mar, self.mem)
        txt.insert(INSERT, 'MEM[' + str(int(self.mar.value, 2)) + '] = '
                   + str(int(self.mem.memory[int(self.mar.value, 2)])) + '\n')

    def st_plus(self, txt):
        """MEM[MAR] <- MBR; MAR++
        It's called in GUI.fun_st_plus
        """
        txt.insert(INSERT, 'MEM[MAR] <- MBR:\n')
        self.mbr.store_to_mem(self.mar, self.mem)
        txt.insert(INSERT, 'MEM[' + str(int(self.mar.value, 2)) + '] = '
                   + str(int(self.mem.memory[int(self.mar.value, 2)])) + '\n\n')

        txt.insert(INSERT, 'MAR++:\n')
        self.mar.add_10(1)
        txt.insert(
            INSERT, 'MAR = ' + str(int(self.mar.value)) + '\n')

    def load_file(self, txt_ipl_info, txt_step_info):
        """Pre-load the file
        It's called in GUI.fun_ipl
        """
        file_dir = './ipl.txt'
        pc_default = '1010'
        try:
            with open(file_dir, 'r') as f:
                lines = f.readlines()
            f.close()
        except FileNotFoundError:
            txt_ipl_info.insert(INSERT, file_dir + 'does not exist')
            return

        for i in lines:
            # ipl_info update
            txt_ipl_info.insert(INSERT, i)
            # mem[add] <- value
            temp = i.split(' ')
            add, value = int(temp[0], 16), bin(int(temp[1][0:4], 16))[2:]
            self.mem.set_to_memory(add, value)
            # step_info update
            txt_step_info.insert(
                INSERT, 'MEM[' + str(add) + '] = ' + value + '\n')

        # set pc by default
        self.pc.value = pc_default
        txt_step_info.insert(INSERT, 'PC has been set to ' + self.pc.value)

    def __fetch(self, txt):
        """Fetching of instruciton"""
        txt.insert(INSERT, 'Fetch Instruction \n')
        # MAR <- PC
        self.mar.get_from_PC(self.pc)
        txt.insert(INSERT, 'MAR <- PC :\t\t\tMAR = ' + self.mar.value + '\n')
        # MBR <- mem[MAR]
        self.mbr.load_from_mem(self.mar, self.mem)
        txt.insert(INSERT, 'MBR <- MEM[' + str(int(self.mar.value, 2)
                                               ) + '] :\t\t\tMBR = ' + self.mbr.value + '\n')
        # IR <- MBR
        self.ir.get_from_MBR(self.mbr)
        txt.insert(INSERT, 'IR <- MBR :\t\t\tIR = ' + self.ir.value + '\n\n')

    def __decode(self, txt):
        """Decoding of instruciton"""
        txt.insert(INSERT, 'Decode Instruction \n')
        return Instruction(self.ir.value)

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
            iar.add_2(ixr.value)
            txt.insert(INSERT, 'IAR += ' + ixr.label + ' :\t\t\tIAR = ' + iar.value + '\n')
        # IAR <- MEM[IAR] if I = 1
        if int(word.indirect,2) == 1:
            add = int(iar.value,2)
            iar.value = self.mem.get_from_memory(add)
            txt.insert(INSERT, 'IAR <- MEM[' + str(add) + '] :\t\t\tIAR = ' + iar.value + '\n')
        # MAR <- IAR
        self.mar.value = iar.value
        txt.insert(INSERT, 'MAR <- IAR :\t\t\tMAR = ' + self.mar.value + '\n\n')

    def __execute_deposit(self, txt, word):
        """The execution and depostion"""
        txt.insert(INSERT, 'Excute and Deposit Result \n')
        op = int(word.opcode, 2)
        gpr = self.gprs[int(word.gpr_index, 2)]
        ixr = self.xs[int(word.ixr_index,2)-1]
        irr = Register(16,'IRR')
        ea = self.mar.value

        c_r = int(gpr.value,2)
        c_ea = int(self.mem.get_from_memory(int(ea,2)),2)
        # LDR
        if op == 1:
            # MBR <- MEM[MAR]
            self.mbr.load_from_mem(self.mar,self.mem)
            txt.insert(INSERT, 'MBR <- MEM['+ str(int(self.mar.value,2)) + '] :\t\t\tMBR = ' + self.mbr.value + '\n')
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
            txt.insert(INSERT, 'MEM['+ str(int(self.mar.value,2)) + '] <- MBR :\t\t\tMEM['+ str(int(self.mar.value,2)) + '] = ' + self.mem.memory[int(self.mar.value,2)] + '\n')
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
            txt.insert(INSERT, gpr.label + ' = ' + str(int(gpr.value)) + '\n')
            txt.insert(INSERT, 'MEM['+ str(int(ea,2)) + '] = '  + str(int(self.mem.memory[int(ea,2)])) + '\n')
            gpr.value = bin(c_r + c_ea)[2:]
            txt.insert(INSERT, gpr.label + ' = ' + gpr.label + ' + MEM['+ str(int(ea,2)) + ']: \t\t\t' + gpr.label +' = ' + gpr.value + '\n')

        # SMR: R=c(R)-c(EA)
        elif op == 5:
            pass
        # AIR: R=c(R)+Immed
        elif op == 6:
            pass
        # SIR: R=c(R)-Immed
        elif op == 7:
            pass
        # JZ: PC=EA if c(R)=0 else PC++
        elif op == 8:
            txt.insert(INSERT, gpr.label +  ' = ' + str(int(gpr.value)) + '\t\t\t')
            if int(gpr.value,2) == 0:
                txt.insert(INSERT, gpr.label + ' == 0\n')
                self.pc.value = ea
                txt.insert(INSERT, 'PC <- EA :\t\t\tPC = ' + self.pc.value + '\n')
            else:
                txt.insert(INSERT, gpr.label + ' != 0\n')
                self.pc.next()
                txt.insert(INSERT, 'PC ++ :\t\t\tPC = ' + self.pc.value + '\n')
        # JNE: PC=EA if c(R)!=0 else PC++
        elif op == 9:
            txt.insert(INSERT, gpr.label +  ' = ' + str(int(gpr.value)) + '\t\t\t')
            if int(gpr.value,2) != 0:
                txt.insert(INSERT, gpr.label + ' != 0\n')
                self.pc.value = ea
                txt.insert(INSERT, 'PC <- EA :\t\t\tPC = ' + self.pc.value + '\n')
            else:
                txt.insert(INSERT, gpr.label + ' == 0\n')
                self.pc.next()
                txt.insert(INSERT, 'PC ++ :\t\t\tPC = ' + self.pc.value + '\n')
        # JCC: PC=EA if CC bit=1 else PC++  CC判定有待修改
        elif op == 10:
            self.cc.value = word.gpr_index
            txt.insert(INSERT, 'CC = ' + self.cc.value + '\t\t\t')
            if int(self.cc.value) == 1:
                txt.insert(INSERT, 'CC == 1\n')
                self.pc.value = ea
                txt.insert(INSERT, 'PC <- EA :\t\t\tPC = ' + self.pc.value + '\n')
            else:
                txt.insert(INSERT, 'CC != 1\n')
                self.pc.next()
                txt.insert(INSERT, 'PC ++ :\t\t\tPC = ' + self.pc.value + '\n')
        # JMA:  PC=EA
        elif op == 11:
            self.pc.value = ea
            txt.insert(INSERT, 'PC <- EA :\t\t\tPC = ' + self.pc.value + '\n')
        # JSR: R3=PC+1; PC=EA
        elif op == 12:
            pass
        # RFS: R0=Immed; PC=c(R3)
        elif op == 13:
            immed = word.address
            self.gpr0.value = immed
            txt.insert(INSERT, 'GPR0 <- Immed :\t\t\tGPR0 = ' + self.gpr0.value + '\n')
            self.pc.value = str(int(self.gpr3.value))
            txt.insert(INSERT, 'PC <- GPR3 :\t\t\tPC = ' + self.pc.value + '\n')
        # SOB: R=c(R)-1; PC=EA if C(R)>0 else PC++ 小于0会有错
        elif op == 14:
            gpr.add_10(-1)
            txt.insert(INSERT, gpr.label + ' -- :\t\t\t' + gpr.label + ' = ' + gpr.value + '\n')
            if int(gpr.value,2) > 0:
                txt.insert(INSERT, gpr.label + ' > 0\n')
                self.pc.value = ea
                txt.insert(INSERT, 'PC <- EA : \t\t\tPC = ' + self.pc.value + '\n')
            else:
                txt.insert(INSERT, gpr.label + ' <= 0\n')
                self.pc.next()
                txt.insert(INSERT, 'PC ++ : \t\t\tPC = ' + self.pc.value + '\n')
        # JGE: PC=EA if c(R)>=0 else PC++ 这玩意儿能小于0？
        elif op == 15:
            txt.insert(INSERT, gpr.label +  ' = ' + str(int(gpr.value)) + '\t\t\t')
            if int(gpr.value,2) >= 0:
                txt.insert(INSERT, gpr.label + ' >= 0\n')
                self.pc.value = ea
                txt.insert(INSERT, 'PC <- EA : \t\t\tPC = ' + self.pc.value + '\n')
            else:
                txt.insert(INSERT, gpr.label + ' < 0\n')
                self.pc.next()
                txt.insert(INSERT, 'PC ++ : \t\t\tPC = ' + self.pc.value + '\n')
        # MLT: Rx, Rx+1=c(Rx)*(Ry)
        elif op == 16:
            pass
        # DVD: Rx, Rx+1=c(Rx)/(Ry)
        elif op == 17:
            pass
        # TRR: cc(4)=1 if c(Rx)=c(Ry) else cc(r)=0
        elif op == 18:
            pass
        # AND: c(Rx)=c(Rx) AND c(Ry)
        elif op == 19:
            pass
        # ORR: c(Rx)=c(Rx) OR c(Ry)
        elif op == 20:
            pass
        # NOT: c(Rx)=NOT c(Rx)
        elif op == 21:
            pass
        # SRC: c(R) is shifted left(L/R=1) or right(L/R=0) either logically(A/L=1) or arithmetically(A/L=0)
        elif op == 25:
            pass
        # RRC: c(R) is Rotated left(L/R=1) or right(L/R=0) either logically(A/L=1)
        elif op == 26:
            pass
        # LDX
        elif op == 33:
            # MBR <- MEM[MAR]
            self.mbr.load_from_mem(self.mar,self.mem)
            txt.insert(INSERT, 'MBR <- MEM[' + str(int(self.mar.value,2)) + '] :\t\t\tMBR = ' + self.mbr.value + '\n')
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
            txt.insert(INSERT, 'MEM['+ str(int(self.mar.value,2)) + '] <- MBR :\t\t\tMEM['+ str(int(self.mar.value,2)) + '] = ' + self.mem.memory[int(self.mar.value,2)] + '\n')
        # IN
        elif op == 49:
            pass
        # OUT
        elif op == 50:
            pass

    def single_step(self, txt):
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
            txt.insert(INSERT, 'OpCode is 0, Program is done\n\n')
            return 'HALT'
        txt.insert(INSERT, 'Instruction :\t\t\t' + word.print_out() + '\n\n')
        # EA Compute
        self.__locate(txt, word)
        # Excute and Deposit
        self.__execute_deposit(txt, word)
        # PC++
        self.pc.next()
        txt.insert(INSERT, '\nPC++ :\t\t\tPC = ' + self.pc.value + '\n\n')

    def test_ins(self, ins, txt):
        """This function implements testing of input instrucitons
        It's called in GUI.func_test
        """
        i = Instruction()
        msg = i.decode_test(ins)
        if msg == 'NUMERROR':
            txt.insert(INSERT, 'Args Number Error\nPlease input again (e.g. LDR 1 0 0 31)\n\n')
            return
        elif msg =='OPERROR':
            txt.insert(INSERT, 'Operation ERROR\nPlease input again\n\n')
            return
        elif msg =='GPRERROR':
            txt.insert(INSERT, 'GPR ERROR\nGPR should be 0, 1, 2 or 3\n\n')
            return
        elif msg =='IXRERROR':
            txt.insert(INSERT, 'IXR ERROR\nIXR should be 0, 1, 2, or 3\n\n')
            return
        elif msg =='IERROR':
            txt.insert(INSERT, 'Indirect ERROR\nIndirect should be 1 or 0\n\n')
            return
        txt.insert(INSERT, 'Valid Instruction detected\n')
        txt.insert(INSERT, 'Decoded\n\n')
        # for some operation x, i are ignored, which means no EA needed
        if int(i.opcode,2) not in [6, 7, 13]:
            self.__locate(txt, i)
        self.__execute_deposit(txt, i)
