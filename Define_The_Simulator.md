# ECE 668 Simulator definition
[toc]

## Expectations

The goal of version 1.0 is to meet the minimum course requirement. Remember, the goal of this project is to show our understanding of score-boarding. We should only implement necessary functions and all related functions as simple as possible.

## Hardware

The following hardware is configurable

| Function Unit    | Description| Parameter  |
| -------- |-------- |-------- |
| Integer          | suitable for any kinds of operations on integers. eg: Integer ALU,Branch |Number,Latency (in Cycles)|
| Float Adder      | word 32 bits word                                            |Number,Latency (in Cycles)|
| Float Multiplier | Handles                           |Number,Latency (in Cycles)|
| Float Divider | word 64 bits floating-point                                  |Number,Latency (in Cycles)|

## Assembler Directives


| Directives |  Description|
| ----------- | ------ |
| .data       | start of data segment   |
| NAME: .word  10| word 32 bits word |
| NAME: .double 10.5| word 64 bits floating-point |
| .code         | start of code segment |
| tag:         | mark source code location. Can be used as a immediate number |

## Instruction Sets

| Instruction | Example | Description|
| ----------- | ---- | ------ |
| LW reg,imm(reg)|LW F2,0(R4)|load 32-bit word|
| SW reg,imm(reg)|SW R5 8(R4)|store 32-bit word|
| L.D freg,imm(reg) |L.D F4,10(R2)|load 64-bit floating-point|
| S.D freg,imm(reg)|S.D F6,0(R5)|store 64-bit floating-point|
| ADD.D freg,freg,freg| ADD.D F2,F2,F1  |add floating-point|
| SUB.D freg,freg,freg | SUB.D F6,F5,F4 |subtract floating-point|
| MUL.D freg,freg,freg| MUL.D F3,F4,F2 |multiply floating-point|
| DIV.D freg,freg,freg| DIV.D F1,F1,F1  |divide floating-point|
| DADD reg,reg,reg| DADD R5,R2,3  | add integers|
| DADDI reg,reg,imm| DADDI R2,R2,1 | add immediate|
| DSUB reg,reg,reg| DSUB R5,R2,R3 | subtract integers|
| DSUBI reg,reg,imm| DSUBI R3,R6,7 | subtract immediate|
| BEQ reg,reg,imm| BEQ R1,R2,-48  |branch if pair of registers are not equal|
| BNE reg,reg,imm| BNE R2,R4,4  |branch if pair of registers are not equal|
| BNEZ reg,imm| BNE R1,loop  |branch if reg is zero|
| J imm | J 1231 | jump to immediate address         |
| NOP | NOP | No operation    |
| HALT | HALT | stops the program    |

### An example
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

