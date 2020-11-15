from Simulator import Config
from Simulator.AbstractHW import AbstractRegister, AbstractFunctionUnit, AbstractMemory, AbstractBus, RegType, \
    InternalInst, Instruction
from Simulator.FunctionUnit import IntFU, FPIntMulFU, FPIntDivFU, FPAdderFU
import Simulator.Config as Config
from Simulator.StateMachine import MultiCycleDFA
from abc import ABCMeta, abstractmethod


class RegStatusTableEntry:
    def __init__(self):
        self.fuId = None


class ControlUnit:

    def __init__(self, entryPoint: int, dataMemory: AbstractMemory, instrMemory: AbstractMemory, dataBus: AbstractBus,
                 instrBus: AbstractBus, registerDict: dict, funcUnitDict: dict):
        """
        Wiring components to Control Unit
        :param entryPoint: The starting point of instruction in instruction memory.
        :param dataMemory: Data Memory
        :param instrMemory: Instruction Memory
        :param dataBus: Data bus
        :param instrBus: Instruction bus
        :param registerDict: A dict for register whose key is RegType. eg: R10=registerDict[RegType.GP_INT][10] PC=registerDict[RegType.SP_PC]
        :param funcUnitDict: A dict for function unit whose key is FUType. eg:intFU1=funcUnitDict['INT1'] intFU2=funcUnitDict[INT2]
        """
        self.dataMemory = dataMemory
        self.instrMemory = instrMemory
        self.dataBus = dataBus
        self.instrBus = instrBus

        # Store these registers for convinience.
        self.PC = registerDict[RegType.SP_PC]
        self.IAR = registerDict[RegType.SP_IAR]
        self.IR = registerDict[RegType.SP_IR]
        self.DAR = registerDict[RegType.SP_DAR]
        self.fltRegs = registerDict[RegType.GP_FLOAT]
        self.intRegs = registerDict[RegType.GP_INT]

        self.PC.write(entryPoint)  # Set PC to entry position.

        self.funcUnitDict = funcUnitDict

        # Initialize Register Table
        self.regStatusTable = {}
        for intReg in self.intRegs:
            self.regStatusTable[intReg.name] = RegStatusTableEntry()
        for fltReg in self.fltRegs:
            self.regStatusTable[fltReg.name] = RegStatusTableEntry()

        # Initialize Instruction Status Tracker (This is for output purposes)
        self.instrStates = {}

        # Initialize cycle counter
        self.cycleCounter = 1

        self.execFinished = False

        self._outputVal = None

    def tick(self):
        '''
        Simulate a clock cycle
        '''

        def canIssue(instr: InternalInst, funcUnit: AbstractFunctionUnit):
            """
            If (!Busy[FU] AND !Result[dst]) , then return an avaiable function unit.
            If not, return None
            :param instr:
            :param funcUnit:
            :return:
            """
            return (instr.fu == funcUnit.type and (not funcUnit.fuStatusTable.busy) and (
                not self.regStatusTable[instr.dstReg.name]))

        def issue(newInstr: InternalInst, funcUnit: AbstractFunctionUnit):
            curFuTableEntry = self.fuStatusTable[funcUnit.id]

            # No need to check! It's control unit's duty to check if that
            # current FN is available, we can issue an instruction

            # 1.set Busy status
            curFuTableEntry.busy = True  # Busy[FU] ← Yes;

            # 2.set the Operation type
            self.operator = curFuTableEntry.operator = newInstr.instrType  # Op[FU] ← op;

            # 3.set fi, fj, fk
            self.fi, self.fj, self.fk = newInstr.dstReg, newInstr.src1Reg, newInstr.src2Reg  # Fi[FU] ← dst; Fj[FU] ← src1; Fk[FU] ← src2;

            # 4.set qj, qk, rj, rk (the 1nd operand can be None eg: load / store )
            index = self.regStatusTable[newInstr.src1Reg.name] if newInstr.src1Reg else None
            if index != None and self.regStatusTable[index]:
                self.qj = self.regStatusTable[index]
                self.rj = False
            # the 2nd operand can be None eg:ALUi
            index = self.regStatusTable[newInstr.src2Reg.name] if newInstr.src2Reg else None
            if index != None and self.regStatusTable[index]:
                self.qk = self.regStatusTable[index]
                self.rk = False

            # 5.set RegisterStatus (dst can be None. eg: J)
            index = self.regStatusTable[newInstr.dstReg.name] if newInstr.dstReg else None
            if index != None:
                self.regStatusTable[index] = funcUnit.id

        def fetchInstr():
            # Lock Instruction Bus
            self.instrBus.BUSY = True

            # Put PC's address to Instruction Address Register
            self.IAR.write(self.PC.read())
            # Get instruction from instrMemory. Address is specified by IAR.
            temp = self.instrMemory.read(self.IAR.read())
            # Put this value to instruction bus.
            self.instrBus.write(temp)

            # Fetch instruction from instruction bus
            memoryInst: Instruction = self.instrBus.read()
            return InternalInst(memoryInst)

        if self.execFinished:
            # Execution already finished. Don't restart
            return

        # Read the next instruction.
        curInstr: InternalInst = fetchInstr()
        assert curInstr != None

        if curInstr.instrType == Config.InstrType.HALT:
            self.execFinished = True
            return
        elif curInstr.instrType == Config.InstrType.NOP:
            pass
        else:
            # See if we can find one available function unit that can execute curInstr. If so, issue it.
            for unit in self.funcUnitDict.values():
                if canIssue(curInstr, unit):
                    issue(curInstr, unit)
                    # Link fu to this instruction
                    curInstr.fu = unit
                    # Link this instruction to fu
                    unit.newInstruction(curInstr, self.funcUnitDict)

                    self.PC += 1
                    print("==issue==", unit)
                    break
            # Loop busy function units and let them execute a tick
            for unit in self.funcUnitDict.values():
                unit: AbstractFunctionUnit
                if unit.fuStatusTable.busy:
                    unit.tick(self.cycleCounter)
        self.cycleCounter += 1
        print("~~~~~~~~~")
