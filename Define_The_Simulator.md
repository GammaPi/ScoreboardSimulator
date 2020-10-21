# Ver 1.0 (Work In Progress, Please change)

## Expectations

The goal of version 1.0 is to meet the minimum course requirement. Remeber, the goal of this project is to show our understanding of scoreboarding. We should only implement necessary functions and all related functions as simple as possible.

## Definition

### Hardware
No pipeline

Integer ~~Adder~~ *2 (📝 suitable for any kinds of operations on integers)

Float Adder *1

Float Multipier *1

📝 Float Divider *1

A stack (❓what is its function)


---

~~The hardware is fixd & unconfigurable.~~

Hanmei 📝 I think it's better to make the hardware configurable. There are 2 ways:

1st: The number of function units (FU) and the number of clock cycles can be configured before the insturctions in the input file using the following format:

```
.[FU type] [number of FUs] [number of clock cycles]
```

2nd: Add a configure module in our scripts.

❓Which one do you prefer? I think the second one is more convenient.

### Instruction Set

Hanmei 📝 I modified most of them to make it compatible to the test cases from the Internet. Also, "ADDI" seems to be an immediate instruction and not suitable for adding data from two registers. 

❓So should we support immediate instruction?

| Instruction | dest | src1   | src2 |
| ----------- | ---- | ------ | ---- |
| L.D         | F4   | 10($2) |      |
| S.D         | F6   | 0($5)  |      |
| ADDI        | F2   | F2     | 1    |
| SUBI        | F3   | F6     | 7    |
| ADD.D       | F2   | F2     | F1   |
| SUB.D       | F6   | F5     | F4   |
| MULT.D      | F3   | F4     | F2   |
| DIV.D       | F1   | F1     | F1   |
| LW          | $2   | 0($4)  |      |
| SW          | $5   | 8($4)  |      |
| ADDI        | $2   | $2     | 1    |
| SUBI        | $3   | $6     | 7    |
| ADD         | $5   | $2     | $3   |
| SUB         | $5   | $2     | $3   |
| BEQ         | $1   | $2     | -48  |
| BNE         | $2   | $4     | 4    |
| J           | 1231 |        |      |


### Input Format

Input should be defined strictly in the format of Op R1,R2,R3
eg:
```
  ADD R1,R2,R3  // R1=R2+R3
  L.D R1,10($2) // R1=M[R2+10]
```

### Output Format

Final Scoreboarding Instruction Status Table (In Console)

Final Scoreboarding Register Status Table (In Console)

Final Scoreboarding Register Status Table (In Console)

Final memory Dump (In Console)

Final Registers Dump (In Console)

Final Stack Dump (In Console)


### Other Functions



