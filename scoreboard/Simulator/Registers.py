from Simulator import Config
from Simulator.AbstractHW import AbstractRegister, RegType
import re


class GPReigster(AbstractRegister):
    def __init__(self, name, numOfBits, regType: RegType):
        """
        :param name: The name of this reigster
        :param numOfBits: Number of bits of this register
        :param type: Type of this register, should be one of RegType
        :param regId: id of this register. Used to find the corresponding reigster.
        """
        super().__init__(name, numOfBits, regType)
        self.value = 0

    def read(self):
        return self.value

    def write(self, value):
        self.value = value


class IntRegister(GPReigster):
    def __init__(self, name):
        super().__init__(name, 32, RegType.GP_INT)
        assert re.fullmatch(r'R\d+', name) is not None
        assert 0 <= int(name[1:]) <= Config.GP_INT_REG_NUM

    def read(self):
        return super().read()

    def write(self, value):
        return super().write(value)


class FloatRegister(GPReigster):
    def __init__(self, name):
        super().__init__(name, 32, RegType.GP_FLOAT)
        assert re.fullmatch(r'F\d+', name) is not None
        assert 0 <= int(name[1:]) <= Config.GP_FLOAT_REG_NUM

    def read(self):
        return super().read()

    def write(self, value):
        return super().write(value)


class SPReigster(AbstractRegister):
    def __init__(self, name, numOfBits, regType: RegType):
        super().__init__(name, numOfBits, regType)
        self.value = 0

    def read(self):
        return self.value

    def write(self, value):
        self.value=value


class PC(SPReigster):
    def __init__(self, name):
        super().__init__(name, 32, RegType.SP_PC)
        self.type = RegType.SP_PC

    def read(self):
        return super().read()

    def write(self, value):
        return super().write(value)


class IAR(SPReigster):
    def __init__(self, name):
        super().__init__(name, 32, RegType.SP_IAR)
        self.type = RegType.SP_IAR

    def read(self):
        return super().read()

    def write(self, value):
        return super().write(value)


class DAR(SPReigster):
    def __init__(self, name):
        super().__init__(name, 32, RegType.SP_DAR)
        self.type = RegType.SP_DAR

    def read(self):
        return super().read()

    def write(self, value):
        return super().write(value)


class IR(SPReigster):
    def __init__(self, name):
        super().__init__(name, 32, RegType.SP_IR)
        self.type = RegType.SP_IR

    def read(self):
        return super().read()

    def write(self, value):
        return super().write(value)
