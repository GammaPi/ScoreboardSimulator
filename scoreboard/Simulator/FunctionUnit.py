from Simulator import Config
from Simulator.StateMachine import MultiCycleDFA
from Simulator.AbstractHW import AbstractFunctionUnit, AbstractMemory, AbstractBus, AbstractRegister, InternalInst, \
    RegType, FuStatusTableEntry, FuStatus
from enum import Enum

'''
Function unit is a sub-component inside ControlUnit.
'''


class InstrState(Enum):
    START = 0  # Haven't been issued
    ISSUE = 1
    READOP = 2
    EXEC = 3
    WB = 4


class PsedoFunctionUnit(AbstractFunctionUnit):
    '''
    This Function Unit don't perform actual binary calculation.
    It only maintains execution states for a certain amount of cycles according to simulator definition, and perform
    one calculation in the last cycle to simulate result.
    :param id: Identifier for this function unit
    '''

    def __init__(self, fuType: Config.FUType, id, dataMemory: AbstractMemory, instrMemory: AbstractMemory,
                 dataBus: AbstractBus, instrBus: AbstractBus, registerDict: dict):
        super().__init__(fuType, id, dataMemory, instrMemory, dataBus, instrBus, registerDict)

    def newInstruction(self, newInstruction, allFuDict):
        self._instruction: InternalInst = newInstruction
        self.allFuDict = allFuDict

        self.status = FuStatus.NORMAL

        # Create new state machine for each stages. This is used in tick function
        # This state machine should be removed. We should let issue readop exec wb function control those stage because an acutal machine don't record each stage take how much time. It just naturally execute stage after stage.
        # self.instrStateMachine = MultiCycleDFA(
        #     [(InstrState.START, InstrState.ISSUE, 1),
        #      (InstrState.ISSUE, InstrState.READOP, self._instruction.instrType.issueCycles),
        #      (InstrState.READOP, InstrState.EXEC, self._instruction.instrType.readOpCycles),
        #      (InstrState.EXEC, InstrState.WB, self._instruction.instrType.execCycles),
        #      (InstrState.WB, InstrState.FINISH, self._instruction.instrType.wbCycles)], initialState=InstrState.START)

        self.currentStage=InstrState.START
        self.nextStage=InstrState.ISSUE

        # Use state mache to simulate step-by-step execution for issue,readop,exec,wb
        self.issueStateMachine = MultiCycleDFA(
            [(False, True, self._instruction.instrType.issueCycles)], initialState=False)
        self.readOpStateMachine = MultiCycleDFA(
            [(False, True, self._instruction.instrType.readOpCycles)], initialState=False)
        self.execStateMachine = MultiCycleDFA(
            [(False, True, self._instruction.instrType.execCycles)], initialState=False)
        self.wbStateMachine = MultiCycleDFA(
            [(False, True, self._instruction.instrType.wbCycles)], initialState=False)

        self.prevState = InstrState.ISSUE

    def _issue(self):
        pass

    def _readOp(self):
        pass

    def _execute(self):
        pass

    def _writeBack(self):
        pass

    def tick(self, curCycle: int):

        if self.instrStateMachine.curState != self.instrStateMachine.peek():
            # curState here is previous stage. This if statement determines whether we can switch to a new stage based on scoreboarding criteria
            # If a state change can happen. We'll change state to the next state. And this if will set correct status ahead of the first cycle in that stage.
            if self.instrStateMachine.peek() == InstrState.ISSUE:
                self.instrStateMachine.next()  # We can always issue. canIssue has already been examined.
                self._instruction.issueStartCycle = curCycle  # This is the first issue cycle
            elif self.instrStateMachine.peek() == InstrState.READOP:
                # Issue(Prev) -> ReadOP(Next)
                if self.fuStatusTable.rj and self.fuStatusTable.rk:
                    # Scoreborading ReadOP (Should execute before the first cycle)
                    self.instrStateMachine.next()
                    self._instruction.readOpStartCycle = curCycle  # This is the first readOP cycle
                else:
                    self.status = FuStatus.RAW
                    return  # Don't switch to new stage. This FU will Stall one cycle.
            elif self.instrStateMachine.peek() == InstrState.EXEC:
                # ReadOP(Prev) -> EXEC(Next)
                self.instrStateMachine.next()  # Exec can always proceed after ReadOP
                self._instruction.execStartCycle = curCycle  # This is the first EXEC cycle
            elif self.instrStateMachine.peek() == InstrState.WB:
                # EXEC -> WB
                canWB = True
                for otherFU in self.allFuDict.values():
                    if otherFU.id != self.id:
                        # ∀f {(Fj[f]≠Fi[FU] OR Rj[f]=No) AND (Fk[f]≠Fi[FU] OR Rk[f]=No)
                        if ((otherFU.fuStatusTable.fj != self.fuStatusTable.fi or otherFU.fuStatusTable.rj == False) and
                                (otherFU.fuStatusTable.fk != self.fuStatusTable.fi or otherFU.fuStatusTable.rk == False)
                        ):
                            pass
                        else:
                            canWB = False
                if canWB:
                    # Scoreborading Write Back
                    self.instrStateMachine.next()
                    self._instruction.wbStartCycle = curCycle  # This is the first WB cycle
                else:
                    self.status = FuStatus.WAR
                    return  # This FU will Stall one cycle.

        # If we come to this place, it means we need to execute a cycle, and there are no more hazard
        # Execute a cycle based on currentState.
        self.status = FuStatus.NORMAL
        if self.instrStateMachine.curState == InstrState.ISSUE:
            self._issue()
            # Mark the last cycle for Issue. Change related table.
            if self.instrStateMachine.peek() is InstrState.READOP:
                self._instruction.issueFinishCycle = curCycle
        elif self.instrStateMachine.curState == InstrState.READOP:
            self._readOp()
            # Mark the last cycle for Read Operator. Change related table.
            if self.instrStateMachine.peek() is InstrState.EXEC:
                self.fuStatusTable.rj = False
                self.fuStatusTable.rk = False
                self._instruction.readOpFinishCycle = curCycle
        elif self.instrStateMachine.curState == InstrState.EXEC:
            self._execute()
            # Mark the last cycle for Execution. Change related table.
            if self.instrStateMachine.peek() is InstrState.WB:
                self._instruction.execFinishCycle = curCycle
        elif self.instrStateMachine.curState == InstrState.WB:
            self._writeBack()
            # Mark the last cycle for Write Back. Change related table.
            if self.instrStateMachine.peek() is None:
                self._instruction.wbFinishCycle = curCycle

                # Clear
                for unit in self.allFuDict.values():
                    # if Qj[f]=FU then Rj[f] ← Yes;
                    if unit.fuStatusTable.qj == self.id:
                        unit.rj = True
                        unit.qj = None
                    # if Qk[f]=FU then Rk[f] ← Yes;
                    if unit.qk == self.id:
                        unit.rk = True
                        unit.qk = None
                self.fuStatusTable.clear()

                # Unbind
                self.instrStateMachine = None

                self.status = FuStatus.IDLE
        else:
            assert False

    def _fromMemToReg(self, dstReg: AbstractRegister, address):
        self.DAR.write(address)
        # Fetch memory and put result into data bus
        self.dataBus.write(self.dataMemory.read(self.DAR.read()))
        # Put databus value into detRegister
        dstReg.write(self.dataBus.read())

    def _fromRegToMem(self, srcReg: AbstractRegister, destAddress):
        self.DAR.write(destAddress)
        # Fetch register value and put result into data bus
        self.dataBus.write(srcReg.read())
        # Put databus value into memory
        self.dataMemory.write(self.DAR.read(), self.dataBus.read())

    def _fromALUToReg(self, dstReg: AbstractRegister, rltValue):
        # Write output from alu output port to databus
        self.dataBus.write(rltValue)
        # Write databus value to register
        dstReg.write(self.dataBus.read())

    def _branchTaken(self, targetAddress):
        self.PC.write(targetAddress)


class IntFU(PsedoFunctionUnit):
    '''
     	Suitable for any kinds of operations on integers. eg: Integer Add/SUB ,Branch. Load and Stores
    '''

    _type = Config.FUType.INT

    def __init__(self, id, dataMemory: AbstractMemory, instrMemory: AbstractMemory,
                 dataBus: AbstractBus, instrBus: AbstractBus, registerDict: dict):
        """
        See PsedoFunctionUnit for more info.

        :param id: Identifier for this function unit
        """
        super().__init__(Config.FUType.INT, id, dataMemory, instrMemory, dataBus, instrBus, registerDict)
        self.A = None  # A port
        self.B = None  # B port

    def _readOp(self):
        if self._instruction.instrType in [Config.InstrType.LW, Config.InstrType.L_D]:
            # self._outputVal = self.A + self.B  # imm + src1
            self.A, self.B = self._instruction.immed, self._instruction.src1Reg.read()
        elif self._instruction.instrType in [Config.InstrType.SW, Config.InstrType.S_D]:
            # self._outputVal = self.A + self.B  # imm + dst
            self.A, self.B = self._instruction.immed, self._instruction.dstReg.read()
        elif self._instruction.instrType in [Config.InstrType.DADD,
                                             Config.InstrType.DSUB,
                                             Config.InstrType.BEQ,
                                             Config.InstrType.BNE]:
            # self._outputVal = self.A + self.B  # src1 + src2
            self.A, self.B = self._instruction.src1Reg.read(), self._instruction.src2Reg.read()
        elif self._instruction.instrType == [Config.InstrType.DADDI, Config.InstrType.DSUBI]:
            # self._outputVal = self.A + self.B  # src1+immed
            self.A, self.B = self._instruction.src1Reg.read(), self._instruction.immed
        elif self._instruction.instrType in [Config.InstrType.BEQZ, Config.InstrType.BNEZ]:
            # self._outputVal = int(self.A == 0)  # src1==0?
            self.A, self.B = self._instruction.src1Reg.read(), 0

    def _execute(self):
        # Psedo calculation in the last cycle based on opCode
        if finished == True:
            if self._instruction.instrType == Config.InstrType.LW:
                # ALU calculate destination
                self._outputVal = self.A + self.B  # imm + src1
            elif self._instruction.instrType == Config.InstrType.SW:
                # ALU calculate destination
                self._outputVal = self.A + self.B  # imm + dst
            elif self._instruction.instrType == Config.InstrType.L_D:
                self._outputVal = self.A + self.B  # imm + src1
            elif self._instruction.instrType == Config.InstrType.S_D:
                self._outputVal = self.A + self.B  # imm + dst
            elif self._instruction.instrType == Config.InstrType.DADD:
                self._outputVal = self.A + self.B  # src1 + src2
            elif self._instruction.instrType == Config.InstrType.DADDI:
                self._outputVal = self.A + self.B  # src1+immed
            elif self._instruction.instrType == Config.InstrType.DSUB:
                self._outputVal = self.A - self.B  # src1+src2
            elif self._instruction.instrType == Config.InstrType.DSUBI:
                self._outputVal = self.A - self.B  # src1-immed
            elif self._instruction.instrType == Config.InstrType.BEQ:
                self._outputVal = int(self.A == self.B)  # src1==src2?
                if bool(self._outputVal) == True:
                    self._branchTaken(self._instruction.immed)
            elif self._instruction.instrType == Config.InstrType.BNE:
                self._outputVal = int(self.A != self.B)  # src1!=src2?
                if bool(self._outputVal) == True:
                    self._branchTaken(self._instruction.immed)
            elif self._instruction.instrType == Config.InstrType.BEQZ:
                self._outputVal = int(self.A == self.B)  # src1==0?
                if bool(self._outputVal) == True:
                    self._branchTaken(self._instruction.immed)
            elif self._instruction.instrType == Config.InstrType.BNEZ:
                self._outputVal = int(self.A != self.B)  # src1!=0?
                if bool(self._outputVal) == True:
                    self._branchTaken(self._instruction.immed)
            else:
                assert False

        return finished

    def _writeBack(self):
        super()._writeBack()
        if self._instruction.instrType == Config.InstrType.LW:
            # ALU calculate destination
            self._fromMemToReg(self._instruction.dstReg, self._outputVal)
        elif self._instruction.instrType == Config.InstrType.SW:
            # ALU calculate destination
            self._fromRegToMem(self._instruction.src1Reg, self._outputVal)
        elif self._instruction.instrType == Config.InstrType.L_D:
            self._fromMemToReg(self._instruction.dstReg, self._outputVal)
        elif self._instruction.instrType == Config.InstrType.S_D:
            self._fromRegToMem(self._instruction.src1Reg, self._outputVal)
        elif self._instruction.instrType == Config.InstrType.DADD:
            self._fromALUToReg(self._instruction.dstReg, self._outputVal)
        elif self._instruction.instrType == Config.InstrType.DADDI:
            self._fromALUToReg(self._instruction.dstReg, self._outputVal)
        elif self._instruction.instrType == Config.InstrType.DSUB:
            self._fromALUToReg(self._instruction.dstReg, self._outputVal)
        elif self._instruction.instrType == Config.InstrType.DSUBI:
            self._fromALUToReg(self._instruction.dstReg, self._outputVal)
        else:
            assert False


class FPAdderFU(PsedoFunctionUnit):
    '''
     	Float Point Adder
    '''

    _type = Config.FUType.FP_ADDER

    def __init__(self, id, dataMemory: AbstractMemory, instrMemory: AbstractMemory,
                 dataBus: AbstractBus, instrBus: AbstractBus, registerDict: dict):
        """
        See PsedoFunctionUnit for more info.

        :param id: Identifier for this function unit
        """
        super().__init__(Config.FUType.FP_ADDER, id, dataMemory, instrMemory, dataBus, instrBus, registerDict)
        self.A = None  # A port
        self.B = None  # B port

    def _readOp(self):
        # FP Adder
        if self._instruction.instrType in [Config.InstrType.ADD_D, Config.InstrType.SUB_D]:
            # self._outputVal = self.A + self.B  # src1 + src2
            self.A, self.B = self._instruction.src1Reg.read(), self._instruction.src2Reg.read()

    def _execute(self):
        finished = super()._execute()

        # Psedo calculation in the last cycle based on opCode
        if finished == True:
            if self._instruction.instrType == Config.InstrType.ADD_D:
                self._outputVal = self.A + self.B  # src1 + src2
            elif self._instruction.instrType == Config.InstrType.SUB_D:
                self._outputVal = self.A - self.B  # src1 - src2
            else:
                assert False
        return finished

    def _writeBack(self):
        super()._writeBack()
        if self._instruction.instrType == Config.InstrType.ADD_D:
            fromALUToReg(self, self._instruction.dstReg, self._outputVal)
        elif self._instruction.instrType == Config.InstrType.SUB_D:
            fromALUToReg(self, self._instruction.dstReg, self._outputVal)
        else:
            assert False


class FPIntMulFU(PsedoFunctionUnit):
    '''
     	Float Point or Integer Multiplier
    '''

    _type = Config.FUType.FP_INT_MUL

    def __init__(self, id, dataMemory: AbstractMemory, instrMemory: AbstractMemory,
                 dataBus: AbstractBus, instrBus: AbstractBus, registerDict: dict):
        """
        See PsedoFunctionUnit for more info.

        :param id: Identifier for this function unit
        """
        super().__init__(Config.FUType.FP_INT_MUL, id, dataMemory, instrMemory, dataBus, instrBus, registerDict)
        self.A = None  # A port
        self.B = None  # B port

    def _readOp(self):
        # FP/INT MUL
        if self._instruction.instrType in [Config.InstrType.MUL_D, Config.InstrType.DMUL]:
            # self._outputVal = self.A * self.B  # src1 * src2
            self.A, self.B = self._instruction.src1Reg.read(), self._instruction.src2Reg.read()

    def _execute(self):
        finished = super()._execute()

        # Psedo calculation in the last cycle based on opCode
        if finished == True:
            if self._instruction.instrType == Config.InstrType.MUL_D:
                self._outputVal = self.A * self.B  # src1 * src2
            elif self._instruction.instrType == Config.InstrType.DMUL:
                self._outputVal = self.A * self.B  # src1 * src2
            else:
                assert False
        return finished

    def _writeBack(self):
        super()._writeBack()
        if self._instruction.instrType == Config.InstrType.MUL_D:
            fromALUToReg(self, self._instruction.dstReg, self._outputVal)
        elif self._instruction.instrType == Config.InstrType.DMUL:
            fromALUToReg(self, self._instruction.dstReg, self._outputVal)
        else:
            assert False


class FPIntDivFU(PsedoFunctionUnit):
    '''
     	Float Point or Integer Divider
    '''
    _type = Config.FUType.FP_INT_DIV

    def __init__(self, id, dataMemory: AbstractMemory, instrMemory: AbstractMemory,
                 dataBus: AbstractBus, instrBus: AbstractBus, registerDict: dict):
        """
        See PsedoFunctionUnit for more info.

        :param id: Identifier for this function unit
        """
        super().__init__(Config.FUType.FP_INT_DIV, id, dataMemory, instrMemory, dataBus, instrBus, registerDict)
        self.A = None  # A port
        self.B = None  # B port

    def _readOp(self):
        # FP/INT DIV
        if self._instruction.instrType in [Config.InstrType.DIV_D, Config.InstrType.DDIV]:
            # self._outputVal = self.A * self.B  # src1 * src2
            self.A, self.B = self._instruction.src1Reg.read(), self._instruction.src2Reg.read()

    def _execute(self):
        finished = super()._execute()

        # Psedo calculation in the last cycle based on opCode
        if finished == True:
            if self._instruction.instrType == Config.InstrType.DIV_D:
                self._outputVal = self.A // self.B  # src1 / src2
            elif self._instruction.instrType == Config.InstrType.DDIV:
                self._outputVal = self.A / self.B  # src1 / src2
            else:
                assert False
        return finished

    def _writeBack(self):
        super()._writeBack()

        if self._instruction.instrType == Config.InstrType.DIV_D:
            fromALUToReg(self, self._instruction.dstReg, self._outputVal)
        elif self._instruction.instrType == Config.InstrType.DDIV:
            fromALUToReg(self, self._instruction.dstReg, self._outputVal)
        else:
            assert False
