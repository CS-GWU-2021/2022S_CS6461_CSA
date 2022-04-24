# Project 4
## 1.Objective
### Floating Point and Vector Operations
Design and implement the modules for:
- floating point 
- vector operations
- simple pipelining  

Write a simple program 3 that demonstrates:
- floating point add/subtract
- vector add/subtract
- floating point conversion

Extend the user interface.

## 2.Submission
- Executable file, running program 1, 2 and 3
- Machine code of program 1, 2 and 3
- Updated documentation of the simulator
- Additional design notes
- Source code

## 3.Description
### 1. Program 1
A program that reads 20 numbers (int) from the keyboard, prints the numbers to the console printer.
Requests a number from the user, and searches the 20 numbers read in for the number closest to that number.
Range of the number should be 0 ... 65,535.

### 2. Program 2
A program that reads a set of a paragraph of 6 sentences from a file into memory. 
It prints the sentences on the console printer. It then asks the user for a word. 
It searches the paragraph to see if it contains the word. 
If so, it prints out the word, the sentence number, and the word number in the sentence.

### 3. Floating Point Instructions / Vector Operations
#### a. New registers `FR0` and `FR1`
Each has 16 bits in length and the format as below:

| S         | Exponent    | Mantissa     |
|-----------|-------------|--------------|
| 0(1 bit)  | 1-7(8 bits) | 8-15(8 bits) |

#### b. Instructions
| OpCode      | FR          | XR          | Indirect  | Add           |
|-------------|-------------|-------------|-----------|---------------|
| 0-5(6 bits) | 6-7(2 bits) | 8-9(2 bits) | 10(1 bit) | 11-15(5 bits) |

| Opcode | Instruction | Name                               | Example            | Description                                                                                        |
|--------|-------------|------------------------------------|--------------------|----------------------------------------------------------------------------------------------------|
| 27     | FADD        | Floating Add Memory to Register    | FADD fr x i add    | c(fr)=c(fr)+c(EA), OVERFLOW may be set                                                             |
| 28     | FSUB        | Floating Sub Memory From Register  | FSUB fr x i add    | c(fr)=c(fr)-c(EA), UNDERFLOW may be set                                                            |
| 29     | VADD        | Vector Add                         | VADD fr x i add    | V1=MEM(MEM(c(EA))) V2=MEM(MEM(c(EA)+1))) V1[i]=V1[i]+V2[i], i=1..c(fr)                             |
| 30     | VSUB        | Vector Sub                         | VSUB fr x i add    | V1=MEM(MEM(c(EA))) V2=MEM(MEM(c(EA)+1))) V1[i]=V1[i]-V2[i], i=1..c(fr)                             |
| 31     | CNVRT       | Convert to Fixed/Floating Point    | CNVRT fr x i add   | convert c(EA) to a fixed point number and stor in fr if fr=0 else convert to a FP and store in fr0 |
| 50     | LDFR        | Load Floating Register From Memory | LDFR fr x i add    | c(fr)=c(EA), c(EA+1)                                                                               |                                                                            |
| 51     | STFR        | Store Floating Register to Memory  | Store fr x i add   | c(EA),c(EA+1) = c(fr)                                                                              |                                                                             |
## 4.Notes