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

    def __init__(self, fuType: Config.FUType, id, dataMemory: AbstractMemory, instrMemory: AbstractMemory,
                 dataBus: AbstractBus, instrBus: AbstractBus, registerDict: dict):

        super().__init__(fuType, id, dataMemory, instrMemory, dataBus, instrBus, registerDict)
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

    _type=Config.FUType.INT

    def __init__(self, id, dataMemory: AbstractMemory, instrMemory: AbstractMemory,
                 dataBus: AbstractBus, instrBus: AbstractBus, registerDict: dict):
        """
        See PsedoFunctionUnit for more info.

        :param id: Identifier for this function unit
        """
        super().__init__(Config.FUType.INT, id, dataMemory, instrMemory, dataBus, instrBus, registerDict)
        self.A = None  # A port
        self.B = None  # B port

    def tick(self):
        def fromMemToReg(dstReg: AbstractRegister, address):
            self.DAR.write(address)
            # Fetch memory and put result into data bus
            self.dataBus.write(self.dataMemory.read(self.DAR.read()))
            # Put databus value into detRegister
            dstReg.write(self.dataBus.read())

        def fromRegToMem(srcReg: AbstractRegister, destAddress):
            self.DAR.write(destAddress)
            # Fetch register value and put result into data bus
            self.dataBus.write(srcReg.read())
            # Put databus value into memory
            self.dataMemory.write(self.DAR.read(), self.dataBus.read())

        def fromALUToReg(dstReg: AbstractRegister, rltValue):
            # Write output from alu output port to databus
            self.dataBus.write(rltValue)
            # Write databus value to register
            dstReg.write(self.dataBus.read())

        def branchTaken(targetAddress):
            self.PC.write(targetAddress)

        finished = super().tick()

        # Psedo calculation in the last cycle based on opCode
        if finished == True:
            if self.instruction.instrType == Config.InstrType.LW:
                # ALU calculate destination
                self._outputVal = self.A + self.B  # imm + src1
                fromMemToReg(self.instruction.dstReg, self._outputVal)
            elif self.instruction.instrType == Config.InstrType.SW:
                # ALU calculate destination
                self._outputVal = self.A + self.B  # imm + dst
                fromRegToMem(self.instruction.src1Reg, self._outputVal)
            elif self.instruction.instrType == Config.InstrType.L_D:
                self._outputVal = self.A + self.B  # imm + src1
                fromMemToReg(self.instruction.dstReg, self._outputVal)
            elif self.instruction.instrType == Config.InstrType.S_D:
                self._outputVal = self.A + self.B  # imm + dst
                fromRegToMem(self.instruction.src1Reg, self._outputVal)
            elif self.instruction.instrType == Config.InstrType.DADD:
                self._outputVal = self.A + self.B  # src1 + src2
                # Store value from reg file
                fromALUToReg(self.instruction.dstReg, self._outputVal)
            elif self.instruction.instrType == Config.InstrType.DADDI:
                self._outputVal = self.A + self.B  # src1+immed
                fromALUToReg(self.instruction.dstReg, self._outputVal)
            elif self.instruction.instrType == Config.InstrType.DSUB:
                self._outputVal = self.A - self.B  # src1+src2
                fromALUToReg(self.instruction.dstReg, self._outputVal)
            elif self.instruction.instrType == Config.InstrType.DSUBI:
                self._outputVal = self.A - self.B  # src1-immed
                fromALUToReg(self.instruction.dstReg, self._outputVal)
            elif self.instruction.instrType == Config.InstrType.BEQ:
                self._outputVal = int(self.A == self.B)  # src1==src2?
                if bool(self._outputVal) == True:
                    branchTaken(self.instruction.immed)
            elif self.instruction.instrType == Config.InstrType.BNE:
                self._outputVal = int(self.A != self.B)  # src1!=src2?
                if bool(self._outputVal) == True:
                    branchTaken(self.instruction.immed)
            elif self.instruction.instrType == Config.InstrType.BEQZ:
                self._outputVal = int(self.A == self.B)  # src1==0?
                if bool(self._outputVal) == True:
                    branchTaken(self.instruction.immed)
            elif self.instruction.instrType == Config.InstrType.BNEZ:
                self._outputVal = int(self.A != self.B)  # src1!=0?
                if bool(self._outputVal) == True:
                    branchTaken(self.instruction.immed)
            else:
                assert False

        return finished


class FPAdderFU(PsedoFunctionUnit):
    '''
     	Float Point Adder
    '''

    _type=Config.FUType.FP_ADDER

    def __init__(self, id, dataMemory: AbstractMemory, instrMemory: AbstractMemory,
                 dataBus: AbstractBus, instrBus: AbstractBus, registerDict: dict):
        """
        See PsedoFunctionUnit for more info.

        :param id: Identifier for this function unit
        """
        super().__init__(Config.FUType.FP_ADDER, id, dataMemory, instrMemory, dataBus, instrBus, registerDict)
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

    _type=Config.FUType.FP_INT_MUL

    def __init__(self, id, dataMemory: AbstractMemory, instrMemory: AbstractMemory,
                 dataBus: AbstractBus, instrBus: AbstractBus, registerDict: dict):
        """
        See PsedoFunctionUnit for more info.

        :param id: Identifier for this function unit
        """
        super().__init__(Config.FUType.FP_INT_MUL, id, dataMemory, instrMemory, dataBus, instrBus, registerDict)
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
    _type=Config.FUType.FP_INT_DIV

    def __init__(self, id, dataMemory: AbstractMemory, instrMemory: AbstractMemory,
                 dataBus: AbstractBus, instrBus: AbstractBus, registerDict: dict):
        """
        See PsedoFunctionUnit for more info.

        :param id: Identifier for this function unit
        """
        super().__init__(Config.FUType.FP_INT_DIV, id, dataMemory, instrMemory, dataBus, instrBus, registerDict)
        self.A = None  # A port
        self.B = None  # B port

    def tick(self):
        finished = super().tick()

        # Psedo calculation in the last cycle based on opCode
        if finished == True:
            if self.instruction.instrType == Config.InstrType.DIV_D:
                self._outputVal = self.A // self.B  # src1 / src2
            elif self.instruction.instrType == Config.InstrType.DDIV:
                self._outputVal = self.A / self.B  # src1 / src2
            else:
                assert False
        return finished
