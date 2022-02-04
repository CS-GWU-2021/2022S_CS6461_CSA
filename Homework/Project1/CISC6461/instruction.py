#-------------------------------------------------------
# @Author       Tenphun0503; Jimmy;
# this is the class for instruction
#------------------------------------------------------
import tools

class Instruction:
    def __init__(self, value = '0' * 16):
        if len(value) < 16:
            value = value.zfill(16)
        self.value = value
        self.update()

    def update(self):
        self.opcode = self.value[:6]
        self.gpr_index = self.value[6:8]
        self.ixr_index = self.value[8:10]
        self.indirect = self.value[10:11]
        self.address = self.value[11:]