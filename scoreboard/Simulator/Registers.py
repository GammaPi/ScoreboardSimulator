import enum
from abc import ABCMeta, abstractmethod
from enum import Enum


class RegType(Enum):
    GP_FLOAT = 1
    GP_INT = 2
    SP_PC = 3
    SP_IR = 5
    SP_IAR = 7
    SP_DAR = 8


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


class GPReigster(AbstractRegister):
    def __init__(self, name, numOfBits):
        super().__init__(name, numOfBits)
        self.value = 0

    def read(self):
        return self.value

    def write(self, value):
        self.value = value


class IntRegister(GPReigster):
    def __init__(self, name):
        super().__init__(name, 32)
        self.type = RegType.GP_INT


class FloatRegister(GPReigster):
    def __init__(self, name):
        super().__init__(name, 32)
        self.type = RegType.GP_FLOAT


class SPReigster(AbstractRegister):
    def __init__(self, name, numOfBits):
        super().__init__(name, numOfBits)
        self.value = 0


class PC(SPReigster):
    def __init__(self, name):
        super().__init__(name, 32)
        self.type = RegType.SP_PC


class IAR(SPReigster):
    def __init__(self, name):
        super().__init__(name, 32)
        self.type = RegType.SP_IAR


class DAR(SPReigster):
    def __init__(self, name):
        super().__init__(name, 32)
        self.type = RegType.SP_DAR


class IR(SPReigster):
    def __init__(self, name):
        super().__init__(name, 32)
        self.type = RegType.SP_IR
