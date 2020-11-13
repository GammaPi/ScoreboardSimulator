from abc import ABCMeta, abstractmethod

from Simulator import Config
from Simulator.StateMachine import MultiCycleDFA
from Simulator.AbstractHW import AbstractFunctionUnit, AbstractMemory, AbstractBus, AbstractRegister, Instruction, \
    RegType

'''
Function unit is a sub-component inside ControlUnit.
'''


class PsedoFunctionUnit(AbstractFunctionUnit):
    '''
    This Function Unit don't perform actual binary calculation.
    It only maintains execution states for a certain amount of cycles according to simulator definition, and perform
    one calculation in the last cycle to simulate result.
    :param id: Identifier for this function unit
    '''

    def __init__(self, fuType: Config.FUType, id):
        super().__init__(fuType, id)
        self.stateMachine = MultiCycleDFA([(False, True, fuType.clock_cycles)],
                                          False)  # Use statemachine to inidicate if an execution has finished

    def tick(self):
        # todo: Do Actual Binary calculation
        if self.ENABLE:
            finished: bool = self.stateMachine.next()
            if finished:
                self.stateMachine.curState = False
            return finished
        else:
            return None


class IntFU(PsedoFunctionUnit):
    '''
     	Suitable for any kinds of operations on integers. eg: Integer Add/SUB ,Branch. Load and Stores
    '''

    def __init__(self, id):
        """
        See PsedoFunctionUnit for more info.

        :param id: Identifier for this function unit
        """
        super().__init__(Config.FUType.INT, id)
        self.A = None  # A port
        self.B = None  # B port

    def tick(self):
        finished = super().tick()

        # Psedo calculation in the last cycle based on opCode
        if finished == True:
            if self.instruction.instrType == Config.InstrType.LW:
                self._outputVal = self.A + self.B  # imm + src1
            elif self.instruction.instrType == Config.InstrType.SW:
                self._outputVal = self.A + self.B  # imm + dst
            if self.instruction.instrType == Config.InstrType.L_D:
                self._outputVal = self.A + self.B  # imm + src1
            elif self.instruction.instrType == Config.InstrType.S_D:
                self._outputVal = self.A + self.B  # imm + dst
            elif self.instruction.instrType == Config.InstrType.DADD:
                self._outputVal = self.A + self.B  # src1 + src2
            elif self.instruction.instrType == Config.InstrType.DADDI:
                self._outputVal = self.A + self.B  # src1+immed
            elif self.instruction.instrType == Config.InstrType.DSUB:
                self._outputVal = self.A - self.B  # src1+src2
            elif self.instruction.instrType == Config.InstrType.DSUBI:
                self._outputVal = self.A - self.B  # src1-src2
            elif self.instruction.instrType == Config.InstrType.BEQ:
                self._outputVal = int(self.A == self.B)  # src1==src2?
            elif self.instruction.instrType == Config.InstrType.BNE:
                self._outputVal = int(self.A != self.B)  # src1!=src2?
            elif self.instruction.instrType == Config.InstrType.BEQZ:
                self._outputVal = int(self.A == self.B)  # src1==0?
            elif self.instruction.instrType == Config.InstrType.BNEZ:
                self._outputVal = int(self.A != self.B)  # src1!=0?
            else:
                assert False

        return finished


class FPAdderFU(PsedoFunctionUnit):
    '''
     	Float Point Adder
    '''

    def __init__(self, id):
        """
        See PsedoFunctionUnit for more info.

        :param id: Identifier for this function unit
        """
        super().__init__(Config.FUType.FP_ADDER, id)
        self.A = None  # A port
        self.B = None  # B port

    def tick(self):
        finished = super().tick()

        # Psedo calculation in the last cycle based on opCode
        if finished == True:
            if self.instruction.instrType == Config.InstrType.ADD_D:
                self._outputVal = self.A + self.B  # src1 + src2
            elif self.instruction.instrType == Config.InstrType.SUB_D:
                self._outputVal = self.A - self.B  # src1 - src2
            else:
                assert False
        return finished


class FPIntMulFU(PsedoFunctionUnit):
    '''
     	Float Point or Integer Multiplier
    '''

    def __init__(self, id):
        """
        See PsedoFunctionUnit for more info.

        :param id: Identifier for this function unit
        """
        super().__init__(Config.FUType.FP_INT_MUL, id)
        self.A = None  # A port
        self.B = None  # B port

    def tick(self):
        finished = super().tick()

        # Psedo calculation in the last cycle based on opCode
        if finished == True:
            if self.instruction.instrType == Config.InstrType.MUL_D:
                self._outputVal = self.A * self.B  # src1 * src2
            elif self.instruction.instrType == Config.InstrType.DMUL:
                self._outputVal = self.A * self.B  # src1 * src2
            else:
                assert False
        return finished


class FPIntDivFU(PsedoFunctionUnit):
    '''
     	Float Point or Integer Divider
    '''

    def __init__(self, id):
        """
        See PsedoFunctionUnit for more info.

        :param id: Identifier for this function unit
        """
        super().__init__(Config.FUType.FP_INT_DIV, id)
        self.A = None  # A port
        self.B = None  # B port

    def tick(self):
        finished = super().tick()

        # Psedo calculation in the last cycle based on opCode
        if finished == True:
            if self.instruction.instrType == Config.InstrType.DIV_D:
                self._outputVal = self.A / self.B  # src1 / src2
            elif self.instruction.instrType == Config.InstrType.DIV:
                self._outputVal = self.A / self.B  # src1 / src2
            else:
                assert False
        return finished


