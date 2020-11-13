from Simulator.AbstractHW import AbstractRegister, RegType


class GPReigster(AbstractRegister):
    def __init__(self, name, numOfBits, regType: RegType, regId: int):
        """
        :param name: The name of this reigster
        :param numOfBits: Number of bits of this register
        :param type: Type of this register, should be one of RegType
        :param regId: id of this register. Used to find the corresponding reigster.
        """
        super().__init__(name, numOfBits, regType)
        self.regId = regId
        self.value = 0

    def read(self):
        return self.value

    def write(self, value):
        self.value = value


class IntRegister(GPReigster):
    def __init__(self, name, regId):
        super().__init__(name, 32, RegType.GP_INT, regId)


class FloatRegister(GPReigster):
    def __init__(self, name, regId):
        super().__init__(name, 32, RegType.GP_FLOAT, regId)


class SPReigster(AbstractRegister):
    def __init__(self, name, numOfBits, regType: RegType):
        super().__init__(name, numOfBits, regType)
        self.value = 0


class PC(SPReigster):
    def __init__(self, name):
        super().__init__(name, 32, RegType.SP_PC)
        self.type = RegType.SP_PC


class IAR(SPReigster):
    def __init__(self, name):
        super().__init__(name, 32, RegType.SP_IAR)
        self.type = RegType.SP_IAR


class DAR(SPReigster):
    def __init__(self, name):
        super().__init__(name, 32, RegType.SP_DAR)
        self.type = RegType.SP_DAR


class IR(SPReigster):
    def __init__(self, name):
        super().__init__(name, 32, RegType.SP_IR)
        self.type = RegType.SP_IR
