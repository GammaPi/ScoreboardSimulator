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
    def reset(self):
        pass

    @abstractmethod
    @property
    def curState(self):
        pass

    @abstractmethod
    @curState.setter
    def curState(self, newState, curCounter=0):
        pass


class Instruction:
    '''
    A representation of instruction that can be executed by the simulator
    We use it to store representation of all kinds of instructions thanks to python's flexible variable type.
    '''

    def __init__(self, instrType: Config.InstrType, dstReg: AbstractRegister, src1Reg: AbstractRegister,
                 src2Reg: AbstractRegister, immed,
                 stateMachine: AbstractStateMachine):
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
        self.stateMachine = stateMachine


class AbstractFunctionUnit(metaclass=ABCMeta):
    def __init__(self, type: Config.FUType, id, instruction: Instruction):
        self.type = type
        self.id = id
        self.ENABLE = False  # Enable Signal
        self._val = None
        self.instruction: Instruction = instruction  # The instruction representation this FU is executing.

    @abstractmethod
    def tick(self):
        """
        To perform correct calculation. CU has to set opCode and ENABLE attribute first!!!
        :return Return a boolean to indicate if execution has finished. Return None if not enabled.
        """
        pass

    @abstractmethod
    @property
    def val(self):
        return self._val

    @val.setter
    def val(self):
        raise AttributeError('Cannot set val because it is readonly')


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
