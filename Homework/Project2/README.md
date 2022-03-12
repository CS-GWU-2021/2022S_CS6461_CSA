# Project 2
## 1.Objective
- Design and implement the modules for enhanced memory and cache operation.
- Show how the cache works via a GUI panel display of the cache.
- Implement all instruction except for: CHK; Floating Point/Vector operatons; Trap
- Extend the user interface, allowing to test instructions
- Demostrate 1st program running on the simulator

## 2. Submission
- An executable file, running program 1
- File containing program 1 as machine code
- Demonstration that program 1 works
- Demostration that individual instructions work
- User instructin
- Design notes
- Source code

## 3. Description
### 1. Cache
Cache sits between memory and the rest of the processor
- cache line
- a simple FIFO algorithm to replace cache lines
- number of cache line (e.g. 16 cahce for 2048)
- demonstrate that cache works (e.g. tracing data)
### 2. Program 1
A program that reads 20 numbers (integers) from the keyboard, prints the numbers to the console printer, requests
a number from the user, and searches the 20 numbers read in for the number closest to the number entered by the 
user. Print the number entered by the user and the number closest to that number.
- Number range from (0, 65535)
### 3. More Load&Store Instructions
|OpCode|Instruction|Name|Example|Description|Comment|
|------|-----------|----|-------|-----------|-------|
|8|JZ|Jump If Zero|JZ r x i add|PC=EA if c(R)=0 else PC++|
|9|JNE|Jump If Not Equal|JNE r x i add|PC=EA if c(R)!=0 else PC++|
|10|JCC|Jump If Condition Code|JCC cc x i add|PC=EA if CC bit=1 else PC++|
|11|JMA|Unconditional Jump To Add|JMA x i add|PC=EA|r is ignored|
|12|JSR|Jump and Save Return Add|JSR x i add|R3=PC+1; PC=EA|r0 should contain pointer to arguments, and argument list should end with -1 (all 1s)|
|13|RFS|Return From Subroutine|RFS Immed|R0=Immed; PC=c(R3)|x, i are ignored; Immed is stored in the instruction's address field|
|14|SOB|Subtract One and Branch|SOB r x i add|R=c(R)-1; PC=EA if C(R)>0 else PC++|
|15|JGE|Jump Greater Than or Equal To|JGR r x i add|PC=EA if c(R)>=0 else PC++|
### 4. Arithmetic and Logical Instructions
|OpCode|Instruction|Name|Example|Description|Comment|
|------|-----------|----|-------|-----------|-------|
|4|AMR|Add Memory to Register|AMR r x i add|R=c(R)+c(EA)|
|5|SMR|Subtract Memory from Register|SMR r x i add|R=c(R)-c(EA)|
|6|AIR|Add Immediate to Register|AIR r immed|R=c(R)+Immed|x, i are ignored; do nothing if Immed=0; load r1 with Immed if c(r)=0|
|7|SIR|Subtract Immediate to Register|SIR r immed|R=c(R)-Immed|x, i are ignored; do nothing if Immed=0; load r1 with -Immed if c(r)=0|
### 5. Arithmetic and Logical Instructions (Register to Register)
OpCode format
|OpCode|Rx|Ry|Ignored|
|------|--|--|-------|
|6 bits|2 bits|2 bits|6 bits|

|OpCode|Instruction|Name|Example|Description|Comment|
|------|-----------|----|-------|-----------|-------|
|16|MLT|Multiply Register by Register|MLT rx ry|Rx, Rx+1=c(Rx)\*(Ry)|Rx, Ry must be 0 or 2; Rx contains the high oder bits, Rx+1 contains the low order bits; Set OVERFLOW if overflow
|17|DVD|Devide Register by Register|DVD rx ry|Rx, Rx+1=c(Rx)/(Ry)|Rx, Ry must be 0 or 2; Rx contains the quotient; Rx+1 contains the ramainder; Set DIVZERO if c(Ry)=0|
|18|TRR|Test the Equality Of Register and Register|TRR rx ry|cc(4)=1 if c(Rx)=c(Ry) else cc(r)=0|
|19|AND|Logical And of Register and Register|AND rx ry|c(Rx)=c(Rx) AND c(Ry)|
|20|ORR|Logical Or of Register and Register|ORR rx ry|c(Rx)=c(Rx) OR c(Ry)|
|21|NOT|Logical Not of Register to Register|NOT rx|c(Rx)=NOT c(Rx)|
### 6. Shift/Rotate Instructions
OpCode format
|OpCode|R|A/L|L/R|Ignored|Count|
|------|-|---|---|-------|-----|
|6 bits|2 bits|1 bit|1 bit|2 bits|4 bits|

|OpCode|Instruction|Name|Example|Description|Comment|
|------|-----------|----|-------|-----------|-------|
|25|SRC|Shift Register by Count|SRC r count L/R A/L|c(R) is shifted left(L/R=1) or right(L/R=0) either logically(A/L=1) or arithmetically(A/L=0)|No shift occurs if Count=0|
|26|RRC|Rotate Register by Count|RRC r count L/R A/L|c(R) is Rotated left(L/R=1) or right(L/R=0) either logically(A/L=1)|No rotate occurs if Count=0|
### 7. I/O Instructions
OpCode format
|OpCode|R|Ignored|DevID|
|------|-|-------|-----|
|6 bits|2 bits|3 bits|5 bits|

DevID 
|DevID|Device|
|-----|------|
|0|Console Keyboard|
|1|Console Printer|
|2|Card Reader|
|3-31|Console Register, switches, etc|

|OpCode|Instruction|Name|Example|
|------|-----------|----|-------|
|49|IN|Input Character to Regisgter from Device|IN r devid|
|50|OUT|Output Character to Device from Register|OUT r devid|

## 4. Notes
cc: Condition code, which has four 1-bit elements:
|element|symbol|
|-------|------|
|overflow|cc(0)|
|uderflow|cc(1)|
|division by zero|cc(2)|
|equal-or-not|cc(3)|

For immediate instructions, the Address portion is considered to be the Immediate Value.
(The maximum absolute value of the Immediate Value is 31. (5 bits without sign))

### types of instructions format
#### 1. HLT
|Opcode|Ignored|
|------|-------|
|0-5(6)|6-15(10)|
#### 2. TRAP
|Opcode|Ignored|Trap Code|
|------|-------|---------|
|0-5(6)|6-15(10)|12-15(4)|
#### 3. Load/Store
|Opcode|R|IX|I|Address|
|------|-|--|-|-------|
|0-5(6)|6-7(2)|8-9(2)|10(1)|11-15(5)|
#### 4. Arithmetic and Logical Instructions (Register to Register)
|OpCode|Rx|Ry|Ignored|
|------|--|--|-------|
|0-5(6)|6-7(2)|8-9(2)|10-15(6)|
#### 5. Shift/Rotate Instructions
|OpCode|R|A/L|L/R|Ignored|Count|
|------|-|---|---|-------|-----|
|0-5(6)|6-7(2)|(8(1)|9(1)|10-11(2)|12-15(4)|
