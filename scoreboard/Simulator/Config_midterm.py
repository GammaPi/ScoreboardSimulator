from enum import Enum
from collections import namedtuple

'''
Simulator Hardware configuration
'''


class FUType(Enum):
    '''
    Function Units
    '''
    # (#quantity,#clockcycles)
    INT = (2, 1)
    FP_INT_MUL = (2, 10)
    FP_ADDER = (2, 2)
    FP_INT_DIV = (0, 40)

    def __init__(self, quantity, clock_cycles):
        self.quantity = quantity
        self.clock_cycles = clock_cycles


class InstrFormat(Enum):
    # (id,UIName)
    R_FORMAT = (1, 'R')  # 1*
    I_FORMAT = (2, 'I')  # 2*
    FR_FORMAT = (3, 'FR')  # 3*
    FI_FORMAT = (4, 'FI')  # 4*
    J_FORMAT = (5, 'J')  # 5*
    SPECIAL = (6, 'S')  # 6*

    def __init__(self, id, uiName):
        self.id = id
        self.uiName = uiName


GP_FLOAT_REG_NUM = 15
GP_INT_REG_NUM = 15

DATA_BUS_WIDTH = 32  # Data bus 32 bits
INST_BUS_WIDTH = 32  # Instruction bus 32 bits

DATA_MEM_SIZE = 2560
INSTR_MEM_SIZE = 256


class InstrType(Enum):
    '''
    Instruction Type Representation.

    Usage:
        Each object contains 4 information. Take InstrType.LW as an example:
        1.If you want to know which function unit can execute LW command :  InstrType.LW.funcUnit
        2.If you want to know what's the format of LW : InstrType.LW.instFormat
        3.If you want to know what's the op code of LW : InstrType.LW.opCode
        4.If you want to know what's the op name of LW : InstrType.LW.opName (Which should of-course be the enum value LW)

        You can construct any InstrType object using it's property:
        1.If you want to construct InstrType USING op name (Perfect for type comparison) : InstrType.LW
        2.If you want to construct InstrType FROM op name (Perfect for parsing op name) : InstrType['LW']
        3.If you want to construct InstrType using op code (Perfect for parsing op code) : InstrType[0x01]

        If there's a point in op name, you have to replace it with _ when constructing InstrType USING op name
        eg: You could only use InstrType.L_D
        But you could construct InstrType FROM the actual op name InstrType[L.D]

        op name is case-insensitive
    '''
    # Add new op as (OPNAME=(funcUnitType, instFormat, issueCycles, readOpCycles,execCycles, wbCycles, opCode,[opName]))
    NOP = (None, InstrFormat.SPECIAL, 1, 0, 0, 0, 60)
    HALT = (None, InstrFormat.SPECIAL, 1, 0, 0, 0, 61)

    LW = (FUType.INT, InstrFormat.I_FORMAT, 1, 1, 1, 1, 20)
    SW = (FUType.INT, InstrFormat.I_FORMAT, 1, 1, 1, 1, 21)
    L_D = (FUType.INT, InstrFormat.FI_FORMAT, 1, 1, 2, 1, 40, 'L.D')
    S_D = (FUType.INT, InstrFormat.FI_FORMAT, 1, 1, 4, 1, 41, 'S.D')

    ADD_D = (FUType.FP_ADDER, InstrFormat.FR_FORMAT, 1, 1, 4, 1, 30, 'ADD.D')
    SUB_D = (FUType.FP_ADDER, InstrFormat.FR_FORMAT, 1, 1, 4, 1, 31, 'SUB.D')
    MUL_D = (FUType.FP_INT_MUL, InstrFormat.FR_FORMAT, 1, 1, 7, 1, 32, 'MUL.D')
    DIV_D = (FUType.FP_INT_MUL, InstrFormat.FR_FORMAT, 1, 1, 10, 1, 33, 'DIV.D')

    DADD = (FUType.INT, InstrFormat.R_FORMAT, 1, 1, 1, 1, 10)
    DADDI = (FUType.INT, InstrFormat.I_FORMAT, 1, 1, 1, 1, 22)
    DSUB = (FUType.INT, InstrFormat.R_FORMAT, 1, 1, 1, 1, 11)
    DSUBI = (FUType.INT, InstrFormat.I_FORMAT, 1, 1, 1, 1, 23)
    DMUL = (FUType.FP_INT_MUL, InstrFormat.R_FORMAT, 1, 1, 10, 1, 12)
    DDIV = (FUType.FP_INT_MUL, InstrFormat.R_FORMAT, 1, 1, 40, 1, 13)

    BEQ = (FUType.INT, InstrFormat.I_FORMAT, 1, 1, 1, 0, 24)
    BNE = (FUType.INT, InstrFormat.I_FORMAT, 1, 1, 1, 0, 25)
    BEQZ = (FUType.INT, InstrFormat.I_FORMAT, 1, 1, 1, 0, 26)
    BNEZ = (FUType.INT, InstrFormat.I_FORMAT, 1, 1, 1, 0, 27)

    J = (FUType.INT, InstrFormat.J_FORMAT, 1, 0, 1, 0, 50)

    def __init__(self, funcUnit, instFormat, issueCycles, readOpCycles, execCycles, wbCycles, opCode, opName=None):
        self.funcUnit = funcUnit
        self.instFormat = instFormat
        self.issueCycles = issueCycles
        self.readOpCycles = readOpCycles
        self.execCycles = execCycles
        self.wbCycles = wbCycles
        self.opCode = opCode
        if opName is None:
            # Use Enum name
            self.opName = self.name.upper()
        else:
            # Use Specified name
            self.opName = opName.upper()

    def __new__(cls, *values):
        '''
        A hack that enable this calss to create instance by opCode
        (ignoring details won't prohibit the usage of this class)
        '''
        obj = object.__new__(cls)
        if values[6] in cls._member_map_:
            raise TypeError('Attempted to reuse opcode: %r' % values[-1])
        # link opcode with InstrType object
        cls._member_map_[values[6]] = obj
        if len(values) == 8:
            cls._member_map_[values[7]] = obj

        # Make output possible
        obj._all_values = values

        return obj

    def __repr__(self):
        '''
            Output correct representation
        '''
        return '<%s.%s: %s>' % (
            self.__class__.__name__,
            self._name_,
            ', '.join([repr(v) for v in self._all_values]),
        )


# [InstrType Related Code Begin]
# Replace InstrType.__class__.__getitem__ in order to automatically uppercase opname
__oriGetItem = InstrType.__class__.__getitem__


def __UpperCaseGetItem(cls, key):
    if type(key) == str:
        key = key.upper()
    return __oriGetItem(cls, key)


InstrType.__class__.__getitem__ = __UpperCaseGetItem
# [InstrType Related Code End]
