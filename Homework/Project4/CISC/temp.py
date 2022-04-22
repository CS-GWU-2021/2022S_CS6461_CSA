import ioDevice as io
reader = io.Reader()
reader.read_file('test.txt')
content = list(reader.content[0])
cache = [None]*200
for i, character in enumerate(content):
    cache[i] = bin(ord(character))[2:]
print(cache)

dict_opcode = {0: 'HLT', 1: 'LDR', 2: 'STR', 3: 'LDA', 4: 'AMR',
                    5: 'SMR', 6: 'AIR', 7: 'SIR', 8: 'JZ', 9: 'JNE',
                    10: 'JCC', 11: 'JMA', 12: 'JSR', 13: 'RFS', 14: 'SOB',
                    15: 'JGE', 16: 'MLT', 17: 'DVD', 18: 'TRR', 19: 'AND',
                    20: 'ORR', 21: 'NOT', 24: 'TRAP', 25: 'SRC', 26: 'RRC',
                    33: 'LDX', 34: 'STX', 49: 'IN', 50: 'OUT', 51: 'CHK'}

'''
0: 1000                 # address of sub-routine table
6: trap 0               # trap to sub-routine 0
1000: 1016              # address of sub-routine 0
1001: 1040              # address of sub-routine 1
1016: LDX x1 0 0        # 1016,1017 load address of sb0 into x1
1017: LDX x1 0 0
1018: JMA 1 0 9         # jump to process
1019: 6                 # number of sentences of the paragraph
1020: 1100              # start of the paragraph in the memory
1021: 1100              # end of the paragraph
1024:                   # return address to main routine
1025: CHK r3 2          # check if file is exist
1026: JNE r3 x1 0 12    # Halt if False and Jump if Ture
1027: HALT
1028: LDR r0 x1 0 3     # r0 <- number of sentences
1029: LDR r3 0 0 2      # 1029, 1030 record return address
1030: STR r3 1 0 8
1031: LDX x3 0 0        # 1031, 1032 load start of paragraph in memory into x3
1032: LDX x3 0 20
1033: LDR r3 x1 0 5     # load end of paragraph in memory into r3
1034: SOB r0 x1 0 21    # loop of reading sentences
1035: STR r3 x1 0 5     # update end of paragraph in memory
1036: JMA x1 1 8        # return to main routine
1037: TRAP 1            # trap to sub-routine 1
1038: JMA x1 0 18       # continue loop
1040: LDX x2 0 0        # 1040, 1041 load address of sb1 into x2
1041: LDX x2 0 1
1042: JMA x2 0 10       # jump to process
1043: 46                # ASCII of '.'
1044: 33                # ASCII of '!'
1045: 63                # ASCII of '?'
1049: JMA x1 0 22       # return to trap 0
1050: IN r1 2           # read a character
1051: STR r1 x3 0 0     # store the character into memory
1052: AIR r3 1
1053: SMR r1 x2 0 3     # 1053, 1054 return if character is '.'
1054: JZ r1 x2 0 9
1055: LDR r1 x3 0 0     # 1055, 1056, 1057 return if '!'
1056: SMR r1 x2 0 4
1057: JZ r1 x2 0 9
1058: LDR r1 x3 0 0     # 1058, 1059, 1060 return if '?'
1059: SMR r1 x2 0 5
1060: JZ r1 x2 0 9
1061: LDX x3 0 1        # store location move on
1062: JMA x2 0 10       # continue loop
'''

