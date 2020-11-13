# ECE 668 Simulator definition
[toc]

## Expectations

The goal of version 1.0 is to meet the minimum course requirement. Remember, the goal of this project is to show our understanding of score-boarding. We should only implement necessary functions and all related functions as simple as possible.

## Hardware

### Function Units

The number of function units is configurable

>  ST: I adjusted Hanmei's implementation to make it consistent with the book and course. (Book Page C-47, Slide Lesson 09, P18 ) 


| Function Unit    | Description| Configurable Parameter |Latency|
| -------- |-------- |-------- |-------- |
| Int Adder    | suitable for any kinds of operations on integers. eg: Integer Add/SUB ,Branch. Load and Stores |Number,Latency (in Cycles)|1|
| FP Adder   | Float Point Adder      |Number,Latency (in Cycles)|2|
| FP/Integer Multiplier | Float Point or Integer Multiplier |Number,Latency (in Cycles)|10|
| FP/Integer Divider | Float Point or Integer Divider  |Number,Latency (in Cycles)|40|

### BUS

32 bit Address

32 bit Data

### Registers

R\*: 32 \* 32-bit General Purpose Register

F\*: 32 \* 32-bit Float Point Register

PC: 1 \* 32-bit Program Counter

IAR: 1 \* 32-bit Instruction Memory Address Register

DAR: 1 \* 32-bit Data Memory Address Register

IR: Instruction Register

### Memory

Little Endian

#### Special Function Registers

1 Instruction Register

1 MAR Register

1 MDRRegister

## Control Signals
### Instruction Fetch

MA=PC

IR=Memory[MA]

### ALU

A=Reg[RS]

B=Reg[RT]

Reg[RD/FD]=OpCode(A,B)

### ALU-Immediate

A=Reg[RS]

B=Immediate (Sign extended)

Reg[RD]=OpCode(A,B)

### Load

A=Reg[RS]

B=Immediate

MA=A+B

Reg[RD]=Memory

### Store

A=Reg[RS]

B=Immediate

MA=A+B

Reg[RD]->Memory

### Unconditional Branch

A=PC

B=Immediate

PC=A+B

## Assembler

### Assembler Directives

Assembler should perform these operations before program execution.


| Directives |  Description|
| ----------- | ------ |
| .data       | start of data segment   |
| NAME: .word  10| word 32 bits word |
| NAME: .double 10.5| word 64 bits floating-point |
| .code         | start of code segment |
| tag:         | mark source code location. Can be used as a immediate number |

### Instruction Sets

> [Reference](https://en.wikibooks.org/wiki/MIPS_Assembly/Instruction_Formats)

Instruction Formats:
- R-Format:  all the data values used by the instruction are located in registers. (Op code range: 0x10-0x1F)
  
  - OP rt, rs, rd
- I-Format:  The instruction must operate on an immediate value and a register value.  (Op code range: 0x20-0x2F)
  - OP rt, IMM(rs)
  - OP  rt, rs, IMM
- FR-Format: Similar to R-Format, but all registers are floatpoint rather than int (Op code range: 0x30-0x3F)
  
  - OP ft, fs, fd
- FI-Format: Similar to I-Format, but all registers are floatpoint rather than int (Op code range: 0x40-0x4F)
  
  - OP ft, fs, IMM
- J-Format: Jump instruction  (Op code range: 0x50-0x5F)
  
  - Opcode Pseudo-Address 
- Single-OP-Format: Only one OP, no parameters   (Op code range: 0x60-0x6F)
  
  - OP


| Instruction | Example | Description|Format|FU|OpCode|
| ----------- | ---- | ------ | ------ |------ |------ |
| LW reg,imm(reg) |LW R2,0(R4)|load 32-bit word|I-Format|INT|20|
| SW reg,imm(reg)|SW R5 8(R4)|store 32-bit word|I-Format|INT|21|
| ||||||
| L.D freg,imm(reg) |L.D F4,10(R2)|load 64-bit floating-point|FI-Format|INT|40|
| S.D freg,imm(reg)|S.D F6,0(R5)|store 64-bit floating-point|FI-Format|INT|41|
| ||||||
| ADD.D freg,freg,freg| ADD.D F2,F2,F1  |add floating-point|FR-Format|FP Adder|30|
| SUB.D freg,freg,freg | SUB.D F6,F5,F4 |subtract floating-point|FR-Format|FP Adder|31|
| MUL.D freg,freg,freg| MUL.D F3,F4,F2 |multiply floating-point|FR-Format|FP/Integer Multiplier|32|
| DIV.D freg,freg,freg| DIV.D F1,F1,F1  |divide floating-point|FR-Format|FP/Integer Divider|33|
| ||||||
| DADD reg,reg,reg| DADD R5,R2,R3 | add integers|R-Format|Integer|10|
| DADDI reg,reg,imm| DADDI R2,R2,1 | add immediate|I-Format|Integer|22|
| DSUB reg,reg,reg| DSUB R5,R2,R3 | subtract integers|R-Format|Integer|11|
| DSUBI reg,reg,imm| DSUBI R3,R6,7 | subtract immediate|I-Format|Integer|23|
| DMUL freg,freg,freg| DMUL R3,R4,R2 |multiply intergers|R-Format|FP/Integer Multiplier|12|
| DDIV freg,freg,freg| DDIV R1,R1,R1  |divide integers|R-Format|FP/Integer Divider|13|
| ||||||
| BEQ reg,reg,imm| BEQ R1,R2,-48  |branch if pair of registers are not equal|I-Format|Integer|24|
| BNE reg,reg,imm| BNE R2,R4,4  |branch if pair of registers are not equal|I-Format|Integer|25|
| BNEZ reg,imm| BNE R1,loop  |branch if reg is zero|I-Format|Integer|26|
| ||||||
| J imm | J 1231 | jump to immediate address         |j-Format|Integer|50|
| ||||||
| NOP | NOP | No operation    | Special ||60|
| HALT | HALT | stops the program    |Special||61|

### A Program example
```
.data
A: .word 10
B: .word 8
C: .double 3.14

.code
loop: 
    L.D F0, 0(R1)
    MUL.D F4,F0,F2
    S.D F4,0(R1)
    DSUBI R1,R1,8
    BENZ R1,loop
halt
```

### Instruction Formats

This is not consistent with MIPS Instruction formats introduce on Lesson 4(Page 10). This design is to make the implementation easier to interpret.

![image-20201110173301611](image-20201110173301611.png)

## Exception Handling

Don't handle exception, execute as is

## Interrupts

Not supported


## I/O Format

Read/Write input from a .s file

Scoreboarding Instruction Status Table (In Window)

Scoreboarding Register Status Table (In Window)

Scoreboarding Register Status Table (In Window)

Memory Dump (In Window)

Final Registers Dump (In Window)

