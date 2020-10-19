# 668project
## Proposal

The whole development process can be seperated into three stages:

1. Requirement Analysis (Finished, [Link to our proposal](https://drive.xttech.top/s/xS5kc3kJNLY5DZF))
 - **We'll use python to implement a simple mips simulator with scoreborading support**. We will use winmips64 only as a reference.

2. System Design (Seperate Modules/Design interfaces so that we can work together) **(By October 31th)**

3. Implementation (Coding) **(After October 31th)**

We should implement the core functionality of a simulator:
 - Implement the whole instruction set (ALU operation (ADD SUB MUL DIV) / memory storage / Branch .etc.).
 - Implement Scoreboarding dynamic scheduling.
 
 
## Current task:
1. We first need to collect some opensource python implementation of scoreboarding. At the end of this week, we should already understand all implementation details of scoreboarding.
2. We need to finalize our supported instruction set by October 31th.
3. We need to think about how to desgin the software architecture. At the end of this week, we should **at least** have some ideas about how to seperate our simulator modules. We must finalize our design by October 31th. If you don't have a clear idea about how to design, you should check mips64's source as a reference.

## Notes:
The task can be very trivial or very complex. For example, if we use C/C++ arithmetic operator to simulate mul/add/sub it will be quite easy to implement. If we only use bit-wise adder to implement all ALU (add/subtract/divide) operations like a real CPU, then that will be more complex. If we simply ignore all underflow/overflow error/arithmetic errors(divide by zero) then it's simple. So we should define all those behaviors before implementation (or unfortunately while implementation). (by Steven)
