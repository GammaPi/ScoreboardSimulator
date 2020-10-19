# 668project

The whole development process can be seperated into four stages. However, if we have time and interests, we could iterate this process.

1. Requirement Analysis (Finished)
2. Define the simulator **(Ver1.0 By October 25th)**
3. System Design (Seperate Modules and define interfaces so that we can work together) **(By October 31th)**
4. Implementation (Coding) **(Planning, After October 31th)**

## Requirement Analysis

(Finished, Link to our proposal [China](https://drive.xtno1.top/s/xS5kc3kJNLY5DZF),[US](https://drive.xttech.tech/s/xS5kc3kJNLY5DZF))

**We'll use python to implement a simple mips simulator with scoreborading support**. We will only use winmips64 as a reference.

## Define our simulator

This project can be very trivial or very complex. For example, if we use C/C++ arithmetic operator to simulate mul/add/sub it will be quite easy to implement. If we only use bit-wise adder to implement all ALU (add/subtract/divide) operations like a real CPU, then that will be more complex. Another example, if we ignore all underflow/overflow error/arithmetic errors(divide by zero) then it's simple. If we need to tacle all of them, then it's complex. 

So, defining all those behaviors before implementation is vital.

## Current task (Sorted by priority)
1. **Define the simulator** We first need to define the behaviors of our simulator. Please define all simulator behavior you can think of in **Define_The_Simulator.md** using natural language.
2. **Understand scoreboarding implementation** We need to understand every implementation details of scoreborading algorithm. Given an existing scoreboarding implementation, we should understand all of its code. If you have time, please implement a scoreboarding algithm that is able to output Instruction status table without performing actual calculation and compare results with existing code.
3. **System Design** We need to think about how to seperate modules and design interfaces. At the end of this week, we should **at least** have some ideas about how to seperate our simulator modules. We must finalize our system design by October 31th. 

Note: If you don't have a clear idea about 1. and 3., you could check mips64's source as a reference.

## Notes:

Please feel free to comment/make changes if there's any unclearity. But be sure to notify others if it's an important change.
