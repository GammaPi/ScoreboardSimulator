# Control Unit

The key part of the scoreboard algorithm that manage the whole process. This module has `pc` and `current_cycle` to get the current pc and cycles. In terms of member functions, it contains some functions that are used to determine if it's ok to proceed to the next phase (`can_read_operands()` , `can_execute()` and `can_write_back()`) or fetch the next instruction (`can_issue()`). In addition, it has some functions that execute the instruction, such as `issue()`, `read_operands()`, `execute()` and `write_back()`. These functions will call the functions in class `FunctionUnit`, which are the real executors. 



The core part of this class is `tick()` function, which is called in each cycle. In this function, each function unit is evaluated and will proceed to the next step if they can.



# Assembler

This module is used for parsing the instructions. Given the assembly code file,   it will read each line of code and classify them into 3 types: R type, I type and J type. All the instructions are stored in a buffer called `instructions` that belongs to the `Assembler` class.



# Function Unit

This module defines the function unit, which has the following properties:

* `type`: include **Int Adder**, **FP Adder**, **FP/Integer Multiplier** and **FP/Integer Divider**
* `cycles`: the number of cycles that the function unit will execute in the execution phase
* `remaining_cycles`: the remaining number of cycles that the function unit will execute in the execution phase
* `busy`: whether the function unit is available or not
* `Operation`: the operation that use the current function unit
* `fi` & `fj` & `fk`: the idx of destination registers and source registers
* `qj` & `qk`: the data of the source registers if available
* `rj` & `rk`: whether the data of the source registers is available
* `instruction_idx`: record the index of the issued instruction
* `lock`: to handle the WB collision



This module also includes a lot of functions:

* `clear(self)`: clear the variables used before and make the function unit available again
* `issue(self, instruction, register_status)`: issue the given instruction and initialize some of the properties of function unit
* `read_operands(self)`: read the operands and set `rj` and `rk` to false
* `execute(self)`: execute the instruction based on the data and operand
* `write_back(self, function_units)`: write the calculated data to the destination registers



In a nutshell, class `FunctionUnit` defines a function unit that can perform issue, read operand, execute and write back. After the instruction is completed, it will clear the variables used before and become available again.

