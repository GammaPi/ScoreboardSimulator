from Simulator import Config
from Simulator.StateMachine import MultiCycleDFA
from Simulator.AbstractHW import AbstractFunctionUnit, AbstractMemory, AbstractBus, AbstractRegister, InternalInst, \
    RegType, FuStatusTableEntry, FuStatus, StallInfo
from enum import Enum
import copy

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

    def newInstruction(self, newInstruction, contolUnit):
        self._instruction: InternalInst = newInstruction
        self.contolUnit = contolUnit

        self.status = FuStatus.NORMAL

        # Create new state machine for each stages. This is used in tick function

        # This state machine should be removed. We should let issue readop exec wb function control those stage because an acutal machine don't record each stage take how much time. It just naturally execute stage after stage.
        # self.instrStateMachine = MultiCycleDFA(
        #     [(InstrState.START, InstrState.ISSUE, 1),
        #      (InstrState.ISSUE, InstrState.READOP, self._instruction.issueCycles),
        #      (InstrState.READOP, InstrState.EXEC, self._instruction.readOpCycles),
        #      (InstrState.EXEC, InstrState.WB, self._instruction.execCycles),
        #      (InstrState.WB, InstrState.FINISH, self._instruction.wbCycles)], initialState=InstrState.START)

        self.currentStage = InstrState.START
        self.nextStage = InstrState.ISSUE

        # Use state mache to simulate step-by-step execution for issue,readop,exec,wb
        self.issueStateMachine = MultiCycleDFA(
            [(False, True, self._instruction.issueCycles)], initialState=False)
        self.readOpStateMachine = MultiCycleDFA(
            [(False, True, self._instruction.readOpCycles)], initialState=False)
        self.execStateMachine = MultiCycleDFA(
            [(False, True, self._instruction.execCycles)], initialState=False)
        self.wbStateMachine = MultiCycleDFA(
            [(False, True, self._instruction.wbCycles)], initialState=False)

        self.prevState = InstrState.ISSUE

    def _issue(self, curCycle):
        pass

    def _readOp(self, curCycle):
        pass

    def _execute(self, curCycle):
        pass

    def _writeBack(self, curCycle):
        pass

    def tick(self, curCycle: int):
        self.stallList = []
        if self.currentStage != self.nextStage:
            # curState here is previous stage. This if statement determines whether we can switch to a new stage based on scoreboarding criteria
            # If a state change can happen. We'll change state to the next state. And this if will set correct status ahead of the first cycle in that stage.
            if self.nextStage == InstrState.ISSUE:
                self.currentStage = self.nextStage  # We can always issue. canIssue has already been examined.
            elif self.nextStage == InstrState.READOP:
                # Issue(Prev) -> ReadOP(Next)
                if self.fuStatusTable.rj and self.fuStatusTable.rk:
                    # Scoreborading ReadOP (Should execute before the first cycle)
                    self.currentStage = self.nextStage
                else:
                    self.status = FuStatus.RAW
                    if not self.fuStatusTable.rj:
                        fuRj = self.contolUnit.funcUnitDict[self.fuStatusTable.qj]  # Fu that will write to Rj
                        conflictInstr = fuRj._instruction
                        # See issue() in Control unit. rj corresponds to srcReg1
                        self.stallList.append(StallInfo(stallType=StallInfo.Type.RAW,
                                                        depFrom=self._instruction.src1Reg,
                                                        depFromInstr=self._instruction,
                                                        depTo=conflictInstr.dstReg,
                                                        depToInstr=conflictInstr))

                    if not self.fuStatusTable.rk:
                        fuRk = self.contolUnit.funcUnitDict[self.fuStatusTable.qk]  # Fu that will write to Rj
                        conflictInstr = fuRk._instruction
                        # See issue() in Control unit. rk corresponds to srcReg2
                        self.stallList.append(StallInfo(stallType=StallInfo.Type.RAW,
                                                        depFrom=self._instruction.src2Reg,
                                                        depFromInstr=self._instruction,
                                                        depTo=conflictInstr.dstReg,
                                                        depToInstr=conflictInstr))

                    return  # Don't switch to new stage. This FU will Stall one cycle.
            elif self.nextStage == InstrState.EXEC:
                # ReadOP(Prev) -> EXEC(Next)
                self.currentStage = self.nextStage  # Exec can always proceed after ReadOP
            elif self.nextStage == InstrState.WB:
                # EXEC -> WB
                canWB = True
                for otherFU in self.contolUnit.funcUnitDict.values():
                    if otherFU.id != self.id:
                        # ∀f {(Fj[f]≠Fi[FU] OR Rj[f]=No) AND (Fk[f]≠Fi[FU] OR Rk[f]=No)
                        otherFuRjDontNeedReadDst = (
                                otherFU.fuStatusTable.fj != self.fuStatusTable.fi or otherFU.fuStatusTable.rj == False)  # If dst is other fu's rj and reading is not complete
                        otherFuRkDontNeedReadDst = (
                                otherFU.fuStatusTable.fk != self.fuStatusTable.fi or otherFU.fuStatusTable.rk == False)  # If dst is other fu's rk and reading is not complete

                        if (otherFuRjDontNeedReadDst and otherFuRkDontNeedReadDst):
                            pass
                        else:
                            canWB = False

                            # Record this RAW stall to stallList
                            if not otherFuRjDontNeedReadDst:
                                conflictInstr: InternalInst = otherFU._instruction
                                # See issue() in Control unit. rj corresponds to srcReg1
                                self.stallList.append(StallInfo(stallType=StallInfo.Type.WAR,
                                                                depFrom=self._instruction.dstReg,
                                                                depFromInstr=self._instruction,
                                                                depTo=conflictInstr.src1Reg,
                                                                depToInstr=conflictInstr))
                            if not otherFuRkDontNeedReadDst:
                                conflictInstr: InternalInst = otherFU._instruction
                                # See issue() in Control unit. rk corresponds to srcReg2
                                self.stallList.append(StallInfo(stallType=StallInfo.Type.WAR,
                                                                depFrom=self._instruction.dstReg,
                                                                depFromInstr=self._instruction,
                                                                depTo=conflictInstr.src2Reg,
                                                                depToInstr=conflictInstr))

                if self.dataBus.BUSY == True:
                    canWB = False
                    # print('WB structural hazard')
                    self.stallList.append(StallInfo(stallType=StallInfo.Type.STRUCTURAL,
                                                    depFrom=self._instruction,
                                                    depFromInstr=None,
                                                    depTo=self.dataBus,
                                                    depToInstr=None))
                if canWB:
                    # Scoreborading Write Back
                    self.currentStage = self.nextStage
                else:
                    self.status = FuStatus.WAR
                    return  # This FU will Stall one cycle.

        # If we come to this place, it means we need to execute a cycle, and there are no more hazard
        # Execute a cycle based on currentState.
        self.status = FuStatus.NORMAL
        if self.currentStage == InstrState.ISSUE:
            self._issue(curCycle)
        elif self.currentStage == InstrState.READOP:
            self._readOp(curCycle)
            # Mark the last cycle for Read Operator. Change related table.
        elif self.currentStage == InstrState.EXEC:
            self._execute(curCycle)
            # Mark the last cycle for Execution. Change related table.
        elif self.currentStage == InstrState.WB:
            self._writeBack(curCycle)
            # Mark the last cycle for Write Back. Change related table.

        # Modify status table at the end of READOP and WB cycle
        if self.currentStage != self.nextStage:
            revInThisCycle = {}

            # Shallow copy fuStatusTable
            try:
                self.fuStatusTableNew
            except Exception as e:
                self.fuStatusTableNew = copy.copy(self.fuStatusTable)

            # Do update on the new fuStatusTable
            if self.currentStage is InstrState.READOP:
                # This is the last cycle for ReadOP
                self.fuStatusTableNew.rj = False
                self.fuStatusTableNew.rk = False

            elif self.currentStage is InstrState.WB:
                # This is the last cycle for WB
                for unit in self.contolUnit.funcUnitDict.values():
                    # Update the new table
                    try:
                        unit.fuStatusTableNew
                    except Exception as e:
                        unit.fuStatusTableNew = copy.copy(unit.fuStatusTable)

                    # if Qj[f]=FU then Rj[f] ← Yes;
                    if unit.fuStatusTable.qj == self.id:
                        unit.fuStatusTableNew.rj = True
                        unit.fuStatusTableNew.qj = None
                    # if Qk[f]=FU then Rk[f] ← Yes;
                    if unit.fuStatusTable.qk == self.id:
                        unit.fuStatusTableNew.rk = True
                        unit.fuStatusTableNew.qk = None

                try:
                    self.contolUnit.regStatusTableNew
                except Exception as e:
                    self.contolUnit.regStatusTableNew = copy.copy(self.contolUnit.regStatusTable)

                # self.contolUnit.regStatusTableNew[self.fuStatusTable.fi.name] = None

                # self.fuStatusTableNew.clear()

                # self.justWb = True
                # print('Note: Finished exec:', self._instruction, '\n')

                # self.status = FuStatus.IDLE

            if self.nextStage is None:
                if self.fuStatusTable.fi:
                    self.contolUnit.regStatusTableNew[self.fuStatusTable.fi.name] = None

                self.fuStatusTableNew.clear()
                self.justWb = True
                print('Note: Finished exec:', self._instruction, '\n')

                self.status = FuStatus.IDLE

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
        # Clear branch flag. Let CU issue instr from this new place
        self.contolUnit.branch = False


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

    def _issue(self, curCycle):
        # Update issue cycle
        if not self._instruction.issueStartCycle:
            self._instruction.issueStartCycle = curCycle

        finished = self.issueStateMachine.next()
        if finished:
            # Update issue cycle
            self._instruction.issueFinishCycle = curCycle

            self.nextStage = InstrState.READOP  # Let tick execute readOp next time. Since issue already finished.

            if self._instruction.instrType == Config.InstrType.J:
                self.nextStage = InstrState.EXEC  # J don't need read operator
                # Mark branch flag. Let CU stop issue another instruction until directoin is known.

            if self._instruction.instrType in [Config.InstrType.BEQ, Config.InstrType.BNE, Config.InstrType.BEQZ,
                                               Config.InstrType.BNEZ, Config.InstrType.J]:
                self.contolUnit.branch = True

    def _readOp(self, curCycle):
        # Update readop cycle
        if not self._instruction.readOpStartCycle:
            self._instruction.readOpStartCycle = curCycle

        finished = self.readOpStateMachine.next()
        if finished:
            self._instruction.readOpFinishCycle = curCycle

            self.nextStage = InstrState.EXEC  # Let tick execute EXEC next time. Since issue already finished.

            # Execute actual logic in the last cycle. (Pretend these instructions are executed during the past cycles)

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
            elif self._instruction.instrType in [Config.InstrType.DADDI, Config.InstrType.DSUBI]:
                # self._outputVal = self.A + self.B  # src1+immed
                self.A, self.B = self._instruction.src1Reg.read(), self._instruction.immed
            elif self._instruction.instrType in [Config.InstrType.BEQZ, Config.InstrType.BNEZ]:
                # self._outputVal = int(self.A == 0)  # src1==0?
                self.A, self.B = self._instruction.src1Reg.read(), 0

    def _execute(self, curCycle):
        # Update exec cycle
        if not self._instruction.execStartCycle:
            self._instruction.execStartCycle = curCycle

        finished = self.execStateMachine.next()
        if finished:
            self._instruction.execFinishCycle = curCycle

            self.nextStage = InstrState.WB  # Let tick execute WB next time. Since issue already finished.

            # Execute actual logic in the last cycle. (Pretend these instructions are executed during the past cycles)

            # Psedo calculation in the last cycle based on opCode
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
                self.nextStage = None  # Branch don't have WB stage.
            elif self._instruction.instrType == Config.InstrType.BNE:
                self._outputVal = int(self.A != self.B)  # src1!=src2?
                if bool(self._outputVal) == True:
                    self._branchTaken(self._instruction.immed)
                self.nextStage = None  # Branch don't have WB stage.
            elif self._instruction.instrType == Config.InstrType.BEQZ:
                self._outputVal = int(self.A == self.B)  # src1==0?
                if bool(self._outputVal) == True:
                    self._branchTaken(self._instruction.immed)
                self.nextStage = None  # Branch don't have WB stage.
            elif self._instruction.instrType == Config.InstrType.BNEZ:
                self._outputVal = int(self.A != self.B)  # src1!=0?
                if bool(self._outputVal) == True:
                    self._branchTaken(self._instruction.immed)
                self.nextStage = None  # Branch don't have WB stage.
            elif self._instruction.instrType == Config.InstrType.J:
                self._branchTaken(self._instruction.immed)
                self.nextStage = None
            else:
                assert False

    def _writeBack(self, curCycle):
        self.dataBus.BUSY = True
        # Update wb cycle
        if not self._instruction.wbStartCycle:
            self._instruction.wbStartCycle = curCycle

        finished = self.wbStateMachine.next()
        if finished:
            self._instruction.wbFinishCycle = curCycle
            self.nextStage = None  # Tell tick this execution has finished. And there's no next stage

            # Execute actual logic in the last cycle. (Pretend these instructions are executed during the past cycles)

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

    def _issue(self, curCycle):
        # Update issue cycle
        if not self._instruction.issueStartCycle:
            self._instruction.issueStartCycle = curCycle

        finished = self.issueStateMachine.next()
        if finished:
            self._instruction.issueFinishCycle = curCycle

            self.nextStage = InstrState.READOP  # Let tick execute readOp next time. Since issue already finished.

    def _readOp(self, curCycle):
        if not self._instruction.readOpStartCycle:
            self._instruction.readOpStartCycle = curCycle

        finished = self.readOpStateMachine.next()
        if finished:
            self._instruction.readOpFinishCycle = curCycle

            self.nextStage = InstrState.EXEC  # Let tick execute EXEC next time. Since issue already finished.

            # Execute actual logic in the last cycle. (Pretend these instructions are executed during the past cycles)

            # FP Adder
            if self._instruction.instrType in [Config.InstrType.ADD_D, Config.InstrType.SUB_D]:
                # self._outputVal = self.A + self.B  # src1 + src2
                self.A, self.B = self._instruction.src1Reg.read(), self._instruction.src2Reg.read()

    def _execute(self, curCycle):
        # Update exec cycle
        if not self._instruction.execStartCycle:
            self._instruction.execStartCycle = curCycle

        finished = self.execStateMachine.next()
        if finished:
            self._instruction.execFinishCycle = curCycle

            self.nextStage = InstrState.WB  # Let tick execute WB next time. Since issue already finished.

            # Execute actual logic in the last cycle. (Pretend these instructions are executed during the past cycles)

            # Psedo calculation in the last cycle based on opCode
            if finished == True:
                if self._instruction.instrType == Config.InstrType.ADD_D:
                    self._outputVal = self.A + self.B  # src1 + src2
                elif self._instruction.instrType == Config.InstrType.SUB_D:
                    self._outputVal = self.A - self.B  # src1 - src2
                else:
                    print('WARNING: Instruction %s \'s execution code undefined' % (self._instruction.instrType.name))
                #     assert False

    def _writeBack(self, curCycle):
        if not self._instruction.wbStartCycle:
            self._instruction.wbStartCycle = curCycle

        finished = self.wbStateMachine.next()
        if finished:
            self._instruction.wbFinishCycle = curCycle

            self.nextStage = None  # Tell tick this execution has finished. And there's no next stage

            # Execute actual logic in the last cycle. (Pretend these instructions are executed during the past cycles)

            if self._instruction.instrType == Config.InstrType.ADD_D:
                self._fromALUToReg(self._instruction.dstReg, self._outputVal)
            elif self._instruction.instrType == Config.InstrType.SUB_D:
                self._fromALUToReg(self._instruction.dstReg, self._outputVal)
            else:
                print('WARNING: Instruction %s \'s writeback code undefined' % (self._instruction.instrType.name))
                #     assert False


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

    def _issue(self, curCycle):
        # Update issue cycle
        if not self._instruction.issueStartCycle:
            self._instruction.issueStartCycle = curCycle

        finished = self.issueStateMachine.next()
        if finished:
            self._instruction.issueFinishCycle = curCycle

            self.nextStage = InstrState.READOP  # Let tick execute readOp next time. Since issue already finished.

    def _readOp(self, curCycle):
        if not self._instruction.readOpStartCycle:
            self._instruction.readOpStartCycle = curCycle

        finished = self.readOpStateMachine.next()
        if finished:
            self._instruction.readOpFinishCycle = curCycle

            self.nextStage = InstrState.EXEC  # Let tick execute EXEC next time. Since issue already finished.

            # Execute actual logic in the last cycle. (Pretend these instructions are executed during the past cycles)

            # FP/INT MUL
            if self._instruction.instrType in [Config.InstrType.MUL_D, Config.InstrType.DMUL]:
                # self._outputVal = self.A * self.B  # src1 * src2
                self.A, self.B = self._instruction.src1Reg.read(), self._instruction.src2Reg.read()

    def _execute(self, curCycle):
        # Update exec cycle
        if not self._instruction.execStartCycle:
            self._instruction.execStartCycle = curCycle

        finished = self.execStateMachine.next()
        if finished:
            self._instruction.execFinishCycle = curCycle

            self.nextStage = InstrState.WB  # Let tick execute WB next time. Since issue already finished.

            # Execute actual logic in the last cycle. (Pretend these instructions are executed during the past cycles)

            # Psedo calculation in the last cycle based on opCode
            if finished == True:
                if self._instruction.instrType == Config.InstrType.MUL_D:
                    self._outputVal = self.A * self.B  # src1 * src2
                elif self._instruction.instrType == Config.InstrType.DMUL:
                    self._outputVal = self.A * self.B  # src1 * src2
                else:
                    print('WARNING: Instruction %s \'s execution code undefined' % (self._instruction.instrType.name))
                #     assert False
            return finished

    def _writeBack(self, curCycle):
        if not self._instruction.wbStartCycle:
            self._instruction.wbStartCycle = curCycle

        finished = self.wbStateMachine.next()
        if finished:
            self._instruction.wbFinishCycle = curCycle

            self.nextStage = None  # Tell tick this execution has finished. And there's no next stage

            # Execute actual logic in the last cycle. (Pretend these instructions are executed during the past cycles)

            if self._instruction.instrType == Config.InstrType.MUL_D:
                self._fromALUToReg(self._instruction.dstReg, self._outputVal)
            elif self._instruction.instrType == Config.InstrType.DMUL:
                self._fromALUToReg(self._instruction.dstReg, self._outputVal)
            else:
                print('WARNING: Instruction %s \'s writeback code undefined' % (self._instruction.instrType.name))
            #     assert False


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

    def _issue(self, curCycle):
        # Update issue cycle
        if not self._instruction.issueStartCycle:
            self._instruction.issueStartCycle = curCycle

        finished = self.issueStateMachine.next()
        if finished:
            self._instruction.issueFinishCycle = curCycle

            self.nextStage = InstrState.READOP  # Let tick execute readOp next time. Since issue already finished.

    def _readOp(self, curCycle):
        if not self._instruction.readOpStartCycle:
            self._instruction.readOpStartCycle = curCycle

        finished = self.readOpStateMachine.next()
        if finished:
            self._instruction.readOpFinishCycle = curCycle

            self.nextStage = InstrState.EXEC  # Let tick execute EXEC next time. Since issue already finished.

            # Execute actual logic in the last cycle. (Pretend these instructions are executed during the past cycles)

            # FP/INT DIV
            if self._instruction.instrType in [Config.InstrType.DIV_D, Config.InstrType.DDIV]:
                # self._outputVal = self.A * self.B  # src1 * src2
                self.A, self.B = self._instruction.src1Reg.read(), self._instruction.src2Reg.read()

    def _execute(self, curCycle):
        # Update exec cycle
        if not self._instruction.execStartCycle:
            self._instruction.execStartCycle = curCycle

        finished = self.execStateMachine.next()
        if finished:
            self._instruction.execFinishCycle = curCycle

            self.nextStage = InstrState.WB  # Let tick execute WB next time. Since issue already finished.

            # Execute actual logic in the last cycle. (Pretend these instructions are executed during the past cycles)

            # Psedo calculation in the last cycle based on opCode
            if finished == True:
                if self._instruction.instrType == Config.InstrType.DIV_D:
                    self._outputVal = self.A // self.B  # src1 / src2
                elif self._instruction.instrType == Config.InstrType.DDIV:
                    self._outputVal = self.A / self.B  # src1 / src2
                else:
                    print('WARNING: Instruction %s \'s execution code undefined' % (self._instruction.instrType.name))
                #     assert False
        return finished

    def _writeBack(self, curCycle):
        if not self._instruction.wbStartCycle:
            self._instruction.wbStartCycle = curCycle

        finished = self.wbStateMachine.next()
        if finished:
            self._instruction.wbFinishCycle = curCycle

            self.nextStage = None  # Tell tick this execution has finished. And there's no next stage

            if self._instruction.instrType == Config.InstrType.DIV_D:
                self._fromALUToReg(self._instruction.dstReg, self._outputVal)
            elif self._instruction.instrType == Config.InstrType.DDIV:
                self._fromALUToReg(self._instruction.dstReg, self._outputVal)
            else:
                print('WARNING: Instruction %s \'s writeback code undefined' % (self._instruction.instrType.name))
            #     assert False
