from abc import ABCMeta, abstractmethod
from enum import Enum

from Simulator import Config


class AbstractRegister(metaclass=ABCMeta):
    def __init__(self, name, numOfBits):
        self.numOfBits = numOfBits
        self.name = name

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def write(self, value):
        pass


class RegType(Enum):
    GP_FLOAT = 1
    GP_INT = 2
    SP_PC = 3
    SP_IR = 5
    SP_IAR = 7
    SP_DAR = 8


class AbstractFunctionUnit(metaclass=ABCMeta):
    def __init__(self, type: Config.FUType, id):
        self.type = type
        self.id = id
        self.ENABLE = False  # Enable Signal
        self._val = None
        self.opCode: int = None  # FU will perform corresponding calculation based on opCode

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