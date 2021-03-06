from Simulator import Config
from Simulator.AbstractHW import AbstractRegister, AbstractFunctionUnit, AbstractMemory, AbstractBus, RegType, \
    InternalInst, Instruction, StallInfo
from Simulator.FunctionUnit import IntFU, FPIntMulFU, FPIntDivFU, FPAdderFU
import Simulator.Config as Config
from Simulator.StateMachine import MultiCycleDFA
from abc import ABCMeta, abstractmethod


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
        self.registerDict = registerDict

        self.PC.write(entryPoint)  # Set PC to entry position.

        self.funcUnitDict = funcUnitDict

        # Initialize Register Table
        self.regStatusTable = {}
        for intReg in self.intRegs:
            self.regStatusTable[intReg.name] = None
        for fltReg in self.fltRegs:
            self.regStatusTable[fltReg.name] = None

        # Initialize Instruction Status Tracker (This is for output purposes)
        self.instrStates = {}

        # Initialize cycle counter
        self.cycleCounter = 1

        self.execFinished = False

        self.halt = False

        self.branch=False

        self._outputVal = None

        self.stallList = []  # (Stall Type, From, To)

    def tick(self):
        '''
        Simulate a clock cycle
        '''

        def canIssue(instr: InternalInst):
            """
            If (!Busy[FU] AND !Result[dst]) , then return an avaiable function unit.
            If not, return None
            :param instr: New Instructoin
            :return: Return funcitonUnit if canIssue, other wise return None
            """

            availableFu = None
            strHazardFU = []  # All busy FUs that cause structural hazard
            # if there's one avaiable FU, then even if other fu are busy we can still issue.
            # This list will be empty if availableFu!=None)

            for funcUnit in self.funcUnitDict.values():
                if instr.instrType.funcUnit == funcUnit.type:
                    if not funcUnit.fuStatusTable.busy:
                        availableFu = funcUnit
                        strHazardFU = []
                        break
                    else:
                        strHazardFU.append(funcUnit)
            wawHazard=False
            if instr.dstReg:
                wawHazard = self.regStatusTable[instr.dstReg.name] is not None

            rltCanIssue = (availableFu != None and not wawHazard)

            if not rltCanIssue:
                # Add analysis to stallList
                if availableFu is None:
                    # Structural Hazard
                    for problemFu in strHazardFU:
                        self.stallList.append(StallInfo(stallType=StallInfo.Type.STRUCTURAL,
                                                        depFrom=instr,
                                                        depFromInstr=None,
                                                        depTo=problemFu,
                                                        depToInstr=None))

                if wawHazard:
                    # The id of function unit executing that conflict instruction
                    fuIdWAW = self.regStatusTable[instr.dstReg.name]
                    conflictInstr = self.funcUnitDict[fuIdWAW]._instruction
                    self.stallList.append(StallInfo(stallType=StallInfo.Type.WAW,
                                                    depFrom=instr.dstReg,
                                                    depFromInstr=instr,
                                                    depTo=conflictInstr.dstReg,
                                                    depToInstr=conflictInstr))
                return None
            else:
                # Can Issue, return corresponding fu
                return availableFu

        def issue(newInstr: InternalInst, funcUnit: AbstractFunctionUnit):
            # No need to check! It's control unit's duty to check if that
            # current FN is available, we can issue an instruction
            # 1.set Busy status
            funcUnit.fuStatusTable.busy = True  # Busy[FU] ← Yes;

            # 2.set the Operation type
            funcUnit.fuStatusTable.operator = newInstr.instrType.opName  # Op[FU] ← op;

            # 3.set fi, fj, fk
            funcUnit.fuStatusTable.fi, funcUnit.fuStatusTable.fj, funcUnit.fuStatusTable.fk = newInstr.dstReg, newInstr.src1Reg, newInstr.src2Reg  # Fi[FU] ← dst; Fj[FU] ← src1; Fk[FU] ← src2;

            # 4.set qj, qk, rj, rk (the 1nd operand can be None eg: load / store )
            if newInstr.src1Reg:
                funcUnit.fuStatusTable.qj = self.regStatusTable[newInstr.src1Reg.name]
                funcUnit.fuStatusTable.rj = funcUnit.fuStatusTable.qj is None
            # the 2nd operand can be None eg:ALUi
            if newInstr.src2Reg:
                funcUnit.fuStatusTable.qk = self.regStatusTable[newInstr.src2Reg.name]
                funcUnit.fuStatusTable.rk = funcUnit.fuStatusTable.qk is None

            # 5.set RegisterStatus (dst can be None. eg: J)
            if newInstr.dstReg:
                self.regStatusTable[newInstr.dstReg.name] = funcUnit.id

        def fetchInstr():
            # Put PC's address to Instruction Address Register
            self.IAR.write(self.PC.read())
            # Get instruction from instrMemory. Address is specified by IAR.
            instrAddress = self.IAR.read()
            temp = self.instrMemory.read(instrAddress)
            # Put this value to instruction bus.
            self.instrBus.write(temp)

            # Fetch instruction from instruction bus
            memoryInst: Instruction = self.instrBus.read()
            internalInstr = InternalInst(memoryInst, address=instrAddress)
            if memoryInst.dstReg:
                internalInstr.dstReg = self.registerDict[memoryInst.dstReg.type][int(memoryInst.dstReg.name[1:])]
            if memoryInst.src1Reg:
                internalInstr.src1Reg = self.registerDict[memoryInst.src1Reg.type][int(memoryInst.src1Reg.name[1:])]
            if memoryInst.src2Reg:
                internalInstr.src2Reg = self.registerDict[memoryInst.src2Reg.type][int(memoryInst.src2Reg.name[1:])]

            return internalInstr

        if self.execFinished:
            # Execution already finished. Don't restart
            return
        print('==========================================')
        print('Cycle', self.cycleCounter)
        print()

        self.stallList = []  # Clean stall states

        # Read the next instruction.
        curInstr = None
        if not self.halt and not self.branch:
            curInstr: InternalInst = fetchInstr()
            assert curInstr != None

        if curInstr and curInstr.instrType == Config.InstrType.HALT:
            self.halt = True
        if curInstr and curInstr.instrType == Config.InstrType.NOP:
            self.PC.write(self.PC.read() + 1)
        else:
            # See if we can find one available function unit that can execute curInstr. If so, issue it.
            # If we meet HALT or branch, we shouldn't issue new instruction
            if not self.halt and not self.branch:
                avaiableFu = canIssue(curInstr)
                if avaiableFu:
                    issue(curInstr, avaiableFu)
                    # Link fu to this instruction
                    curInstr.fu = avaiableFu
                    # Link this instruction to fu
                    avaiableFu.newInstruction(curInstr, self)

                    self.PC.write(self.PC.read() + 1)
                    print("==issue==", curInstr)

            # Loop busy function units and let them execute a tick
            for unit in self.funcUnitDict.values():
                if unit.fuStatusTable.busy:
                    unit.tick(self.cycleCounter)

            for unit in self.funcUnitDict.values():
                # Perform simultaneous updates to fuTable
                try:
                    unit.fuStatusTable = unit.fuStatusTableNew
                    del unit.fuStatusTableNew
                except Exception as e:
                    pass

                # Perform simultaneous updates to register status table
                try:
                    self.regStatusTable = self.regStatusTableNew
                    del self.regStatusTableNew
                except Exception as e:
                    pass

            #Remove BUSY FLAG
            if self.dataBus.BUSY:
                self.dataBus.BUSY=False

        # Add stallInfo from all function units to this stall list.
        for unit in self.funcUnitDict.values():
            self.stallList.extend(unit.stallList)

        print('RegStatus:', self.getRegisterStatus(), '\n')
        print('Function Unit Status:\n')
        for key, value in self.getFuTable().items():
            print(key, value)
        print()

        if len(self.getInstrStatusTable()) > 0:
            print('Active instruction:')
            for instr in self.getInstrStatusTable():
                print(instr)

            if len(self.stallList) > 0:
                print('STALL:')
                for stallInfo in self.stallList:
                    print(str(stallInfo))

        if self.halt:
            self.execFinished = True
            instrStatusList = []
            for unit in self.funcUnitDict.values():
                if unit.fuStatusTable.busy:
                    self.execFinished = False

        self.cycleCounter += 1

    def currentStalls(self):
        return self.stallList

    def getRegisterStatus(self):
        return self.regStatusTable

    def getFuTable(self):
        fuTable = {}
        for unit in self.funcUnitDict.values():
            fuTable[unit.id] = str(unit.fuStatusTable)
        return fuTable

    def getInstrStatusTable(self):
        instrStatusList = []
        for unit in self.funcUnitDict.values():
            unit: AbstractFunctionUnit
            if unit.fuStatusTable.busy:
                instrStatusList.append(unit._instruction)
        return instrStatusList
