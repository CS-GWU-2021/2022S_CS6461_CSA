# Project 1
## 1. Objective
Design and implement the basic machine architecture
 - Implement a simple memory
 - Execute **Load** and **Store** instructions
 - Build initial user interface to simulator
 
## 2. Submission
 - An executable file
 - User instruction
 - Source code (with header comments for each module and comments of code)
 - Design notes

## 3. Language & Module
- Python 3.7.8
- tkinter

## 4. Description
Project should be able to:
- Enter data into any of R0-R3 and IX1-IX3
- Enter data into memory via switches
- Enter the various Load and Store Instructions into memory
- Enter address into PC and press **Single Step** to execute the instruction at that address
- Pressing **IPL** should pre load a program that allows user to hit either **RUN** or **Single Step**

## 5. Notes
The simulated machine has the following characteristics:  
Memory of 2048 words, expandable to 4096 words

Instructions/words format:
|Opcode|R|IX|I|Address|
|------|-|--|-|-------|
|6 bits|2 bits|2 bits|1 bit|5 bits|  

The front panel has the following registers:  
|Register|Size|Description|
|--------|----|-----------|
|PC|12 bits|Program Counter|
|MAR|12 bits|Memory Address Register|
|MBR|16 bits|Memory Buffer Register|
|CC|4 bits|Condition Code|
|MFR|4 bits|Machine Fault Register|
|IR|16 bits|Instruction Register|
|GPR 0-3|16 bits|General Purpose Registers|
|IXR 1-3|16 bits|Index Register|

Load/Store Instruction:  
|OpCode_8|Instruction|Example|Encoded Instruction|Description|
|--------|-----------|-------|-------------------|-----------|
|01|LDR r, x, address|LDR 3,0,31|000001 11 00 0 11111|Load GPR3 with the contents of the memory 31|
|02|STR r, x, address|STR 2,0,16|000002 10 00 0 10000|Store GPR2 with the contents of the memory 16|

User Interface Foresight:
![UI](https://github.com/CS-GWU-2021/2022S_CS6461_CSA/blob/main/Homework/Project1/user%20interface.png)
