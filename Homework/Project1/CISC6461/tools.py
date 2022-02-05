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
    else:
        return 'VAL'
def decode_gpr(gpr):
    gpr = int(gpr,2)
    return 'R'+str(gpr)
def print_ins(txt):
    return decode_opcode(txt[0:6]) +' '+ decode_gpr(txt[6:8]) + ' ' + txt[8:10] +' ' +txt[10:11] +' '+ str(int(txt[11:16],2))
def print_value(txt):
    return txt[0:6] +' '+ txt[6:8] + ' ' + txt[8:10] +' ' +txt[10:11] +' '+ txt[11:16]

# sample
def sample():
    line = '0008 000A 0009 0100 000A 84A8 000B 84C9 000C 0428 000D 0029 000E 0E00 000F 0A10 0010 FFFF 0100 0008'
    line = line.split(' ')
    for i in range (1,len(line),2):
        add, value = str(int(line[i-1],16)), bin(int(line[i],16))
        value = value[2:]
        value = value.zfill(16)
        print('Line-----------------------------------------------')
        print('add: '+ bin(int(add))[2:] + '\tvalue: ' + print_value(value))
        print('add: '+ add + '\t\tvalue: ' + print_ins(value))