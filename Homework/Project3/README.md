# Project 3
## 1.Objective
- Execute All Instructions: CHK, TRAP
- Program 2

## 2.Submission
- An executable file, running program 2
- File containing program 2 as machine code
- Demonstration that program 2 works
- User Instruction
- Design notes
- Source code

## 3.Description
### 1.Program 2
A program that reads a set of a paragraph of 6 sentences from a file into memory. It prints the sentences ont he console printer. It then asks the user for a word. It searches the paragraph to see if it contains the word. If so, it prints out the word, the sentence number, and the word number in the sentence.
### 2.TRAP
#### a. Format:
| OpCode      | Ignored      | Trap Code     |
|-------------|--------------|---------------|
| 0-5(6 bits) | 6-11(6 bits) | 12-15(4 bits) |
#### b. Definition
OpCode 24  
TRAP trapCode  
e.g. TRAP 5
#### c. Description
Traps to MEM[0], and stores PC+1 into MEM[2]
MEM[0] contains the address to a table in memory. 
The table can have up to 16 entries of user-specified routines.
e.g. PC<-MEM[0]+TrapCode, execute sub-routine, back to MEM[2]
### 3.CHK
#### a. Format:
| OpCode      | R           | Ignored      | DevID         |
|-------------|-------------|--------------|---------------|
| 0-5(6 bits) | 6-7(2 bits) | 8-10(2 bits) | 11-15(5 bits) |
#### b. Definition
OpCode 51  
CHK r Devid  
e.g. CHK 2 1
#### c. Description
Check Device Status to Register: c(r) <- Device Status
## 4.Notes
