from abc import ABCMeta, abstractmethod
from enum import Enum

from Simulator import Config

'''
This file stores abstract classes that represents hardware. And some universal classes used by those hardware.
'''


class RegType(Enum):
    GP_FLOAT = 1
    GP_INT = 2
    SP_PC = 3
    SP_IR = 5
    SP_IAR = 7
    SP_DAR = 8


class AbstractRegister(metaclass=ABCMeta):
    def __init__(self, name, numOfBits, regType: RegType):
        self.numOfBits = numOfBits
        self.name = name
        self.type = regType

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def write(self, value):
        pass


class AbstractStateMachine:

    @abstractmethod
    def next(self):
        pass

    @abstractmethod
    def peek(self):
        pass

    @property
    def curState(self):
        pass

    @curState.setter
    def curState(self, newState, curCounter=0):
        pass


class Instruction:
    '''
    A representation of instruction that can be executed by the simulator
    We use it to store representation of all kinds of instructions thanks to python's flexible variable type.
    '''

    def __init__(self, instrType: Config.InstrType, dstReg: AbstractRegister, src1Reg: AbstractRegister,
                 src2Reg: AbstractRegister, immed):
        """
        :param instrType: Type of instruction
        :param dstReg: A tuple of (AbstractHW.RegType,regId). RegId maybe none.
        :param src1Reg: A tuple of (AbstractHW.RegType,regId). RegId maybe none.
        :param src2Reg: A tuple of (AbstractHW.RegType,regId). RegId maybe none.
        :param immed: An immediate number
        :param stateMachine: A statemachine. Useful for recording instruction state. But have no actual benefit for the simulator
        """
        self.instrType = instrType
        self.dstReg = dstReg
        self.src1Reg = src1Reg
        self.src2Reg = src2Reg
        self.immed = immed  # immediate number


class InternalInst(Instruction):
    '''
    A internal representation of instruction in simulator.
    It expands Instruction with some state variables
    '''

    def __init__(self, instrFromMemory: Instruction):
        """
        :param instrType: Type of instruction
        :param dstReg: A tuple of (AbstractHW.RegType,regId). RegId maybe none.
        :param src1Reg: A tuple of (AbstractHW.RegType,regId). RegId maybe none.
        :param src2Reg: A tuple of (AbstractHW.RegType,regId). RegId maybe none.
        :param immed: An immediate number
        :param stateMachine: A statemachine. Useful for recording instruction state. But have no actual benefit for the simulator
        """
        super().__init__(instrFromMemory.instrType, instrFromMemory.dstReg, instrFromMemory.src1Reg,
                         instrFromMemory.src2Reg, instrFromMemory.immed)

        self.fu: AbstractFunctionUnit = None  # Which function unit is executing this instruction

        self.issueStartCycle = None
        self.issueFinishCycle = None
        self.readOpStartCycle = None
        self.readOpFinishCycle = None
        self.execStartCycle = None
        self.execFinishCycle = None
        self.wbStartCycle = None
        self.wbFinishCycle = None


class AbstractMemory(metaclass=ABCMeta):
    def __init__(self, name: str, totalSize: int):
        """
        Initialize simulator
        :param name:Name of the memory unit
        :param totalSize: The size of this memory (In Words, one word is 32 bits)
        """
        self.name = name
        self.totalSize = totalSize

    @abstractmethod
    def read(self, location: int):
        pass

    @abstractmethod
    def write(self, location: int, value):
        pass


class AbstractBus(metaclass=ABCMeta):
    def __init__(self, name, numBits):
        """
        :param name: Bus name
        :param numBits: Bus Width
        """
        self.name = name
        self.numBits = numBits
        self.BUSY = False

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def write(self, value):
        pass


class FuStatusTableEntry:
    def __init__(self):
        self.busy = False
        self.operator: Config.InstrType = None  # operation that use the functional unit
        self.fi = self.fj = self.fk = None
        self.qj = self.qk = None
        self.rj = self.rk = True

    def clear(self):
        """
        Reset the FU after the instruction in use has completed
        """
        self.busy = False
        self.operator: Config.InstrType = None
        self.fi = self.fj = self.fk = None
        self.qj = self.qk = None
        self.rj = self.rk = True


class FuStatus(Enum):
    IDLE = 0
    NORMAL = 1
    RAW = 2
    WAR = 3


class AbstractFunctionUnit(metaclass=ABCMeta):

    def __init__(self, fuType: Config.FUType, id, dataMemory: AbstractMemory, instrMemory: AbstractMemory,
                 dataBus: AbstractBus, instrBus: AbstractBus, registerDict: dict):
        self.type = fuType
        self.id = id
        self._outputVal = None

        self.dataMemory = dataMemory
        self.instrMemory = instrMemory
        self.dataBus = dataBus
        self.instrBus = instrBus

        self.PC = registerDict[RegType.SP_PC]
        self.IAR = registerDict[RegType.SP_IAR]
        self.IR = registerDict[RegType.SP_IR]
        self.DAR = registerDict[RegType.SP_DAR]
        self.fltRegs = registerDict[RegType.GP_FLOAT]
        self.intRegs = registerDict[RegType.GP_INT]

        self.fuStatusTable: FuStatusTableEntry = FuStatusTableEntry()
        self.status = FuStatus.IDLE
        self._instruction: InternalInst = None  # The instruction this FU is executing.

    def _issue(self):
        """
        Read operand
        return: Return a boolean to indicate if readOp has finished. Return None if not enabled.
        """
        pass

    @abstractmethod
    def _readOp(self):
        """
        Read operand
        return: Return a boolean to indicate if readOp has finished. Return None if not enabled.
        """
        pass

    @abstractmethod
    def _execute(self):
        """
        To perform correct calculation. CU has to set instruction and ENABLE attribute first!!!
        This function only performs exec stage. Operands are assigned by CU.
        :return Return a boolean to indicate if execution has finished. Return None if not enabled.
        """
        pass

    @abstractmethod
    def _writeBack(self):
        """
        Perform corresponding operation in write back stage.
        return: Return a boolean to indicate if writeBack has finished. Return None if not enabled.
        """
        pass

    @abstractmethod
    def tick(self, curCycle: int):
        """
        Execute one cycle
        :param curCycle:
        """
        pass

    @abstractmethod
    def newInstruction(self, newInstruction, allFuDict):
        """
        Let this FU execute new instruction
        :param newInstruction: A new instruction from instruction memory
        :param allFuDict: All the fus inside control unit.
        """
        pass
