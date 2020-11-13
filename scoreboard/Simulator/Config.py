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
    INT = (1, 1)
    FP_INT_MUL = (2, 10)
    FP_ADDER = (1, 2)
    FP_INT_DIV = (1, 40)

    def __init__(self, quantity, clock_cycles):
        self.quantity = quantity
        self.clock_cycles = clock_cycles


class InstrFormat(Enum):
    R_FORMAT = 1  # 1*
    I_FORMAT = 2  # 2*
    FR_FORMAT = 3  # 3*
    FI_FORMAT = 4  # 4*
    J_FORMAT = 5  # 5*
    SPECIAL = 6  # 6*


GP_FLOAT_REG_NUM = 15
GP_INT_REG_NUM = 15

DATA_BUS_WIDTH = 32  # Data bus 32 bits
INST_BUS_WIDTH = 32  # Instruction bus 32 bits

DATA_MEM_SIZE=2560
INSTR_MEM_SIZE=256


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
    # Add new op as (OPNAME=(funcUnitType, instFormat, opCode,[opName]))
    NOP = (None, InstrFormat.SPECIAL, 60)
    HALT = (None, InstrFormat.SPECIAL, 61)

    LW = (FUType.INT_ADDER, InstrFormat.I_FORMAT, 20)
    SW = (FUType.INT_ADDER, InstrFormat.I_FORMAT, 21)
    L_D = (FUType.FP_ADDER, InstrFormat.FI_FORMAT, 40, 'L.D')
    S_D = (FUType.FP_ADDER, InstrFormat.FI_FORMAT, 41, 'S.D')

    ADD_D = (FUType.FP_ADDER, InstrFormat.FR_FORMAT, 30, 'ADD.D')
    SUB_D = (FUType.FP_ADDER, InstrFormat.FR_FORMAT, 31, 'SUB.D')
    MUL_D = (FUType.FP_INT_MUL, InstrFormat.FR_FORMAT, 32, 'MUL.D')
    DIV_D = (FUType.FP_INT_DIV, InstrFormat.FR_FORMAT, 33, 'DIV.D')

    DADD = (FUType.INT_ADDER, InstrFormat.R_FORMAT, 10)
    DADDI = (FUType.INT_ADDER, InstrFormat.I_FORMAT, 22)
    DSUB = (FUType.INT_ADDER, InstrFormat.R_FORMAT, 11)
    DSUBI = (FUType.INT_ADDER, InstrFormat.I_FORMAT, 23)
    DMUL = (FUType.FP_INT_MUL, InstrFormat.R_FORMAT, 12)
    DDIV = (FUType.FP_INT_DIV, InstrFormat.R_FORMAT, 13)

    BEQ = (FUType.INT_ADDER, InstrFormat.I_FORMAT, 24)
    BNE = (FUType.INT_ADDER, InstrFormat.I_FORMAT, 25)
    BENZ = (FUType.INT_ADDER, InstrFormat.I_FORMAT, 26)

    J = (FUType.INT_ADDER, InstrFormat.J_FORMAT, 50)

    def __init__(self, funcUnit, instFormat, opCode, opName=None):
        self.funcUnit = funcUnit
        self.instFormat = instFormat
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
        if values[2] in cls._member_map_:
            raise TypeError('Attempted to reuse opcode: %r' % values[-1])
        # link opcode with InstrType object
        cls._member_map_[values[2]] = obj
        if len(values) == 4:
            cls._member_map_[values[3]] = obj

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
