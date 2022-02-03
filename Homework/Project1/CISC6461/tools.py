# generate zeros
def zero_gene(bit_num):
    value=[]
    for i in range(bit_num):
        value.append('0')
    return value


def split_each_bit(str_value):
    value = []
    for i in str_value:
        value.append(i)
    return value

def buqi(str_value):
    length = 16-len(str_value)
    txt = ''.join(['0']*length)
    return txt+str_value

def txt_split(num_txt):
    txt=[]
    part = int(len(num_txt)/4)
    for i in range(part):
        start = i*4
        txt.append(num_txt[start:start+4])
    return ' '.join(txt)

"""
decode file from outside
"""
def decode_opcode(opcode):
    op = int(opcode,2)
    if op == 0:
        return 'HLT'
    elif op == 1:
        return 'LDR'
    elif op == 2:
        return 'STR'
    elif op == 3:
        return 'LDA'
    elif op == 33:
        return 'LDX'
    elif op == 34:
        return 'STX'
def decode_gpr(gpr):
    gpr = int(gpr,2)
    return 'R'+str(gpr)
def print_ins(txt):
    return decode_opcode(txt[0:6]) +' '+ decode_gpr(txt[6:8]) + ' ' + txt[8:10] +' ' +txt[10:11] +' '+ str(int(txt[11:16],2))
def print_value(txt):
    return txt[0:6] +' '+ txt[6:8] + ' ' + txt[8:10] +' ' +txt[10:11] +' '+ txt[11:16]

# sample
def sample():
    line = '0006 040e 0007 080f 0008 844f 0009 8850 000A 0d54 000B 0660 000C 0a74 000D 0000 000E 0014 0014 0028 0028 0050'
    line = line.split(' ')
    for i in range (1,len(line)-1,2):
        add, value = str(int(line[i-1],16)), bin(int(line[i],16))
        value = value[2:]
        value = buqi(value)
        print('Line-----------------------------------------------')
        print('add: '+ bin(int(add))[2:] + '\tvalue: ' + print_value(value))
        print('add: '+ add + '\t\tvalue: ' + print_ins(value))