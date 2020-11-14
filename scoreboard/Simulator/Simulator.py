from Simulator.ControlUnit import ControlUnit
from Simulator.Memory import DictMemory
from Simulator.FunctionUnit import IntFU, FPIntDivFU, FPAdderFU, FPIntMulFU
from Simulator.Registers import IntRegister, FloatRegister, PC, IAR, DAR, IR
from Simulator.AbstractHW import RegType, AbstractFunctionUnit
import Simulator.Config as Config
from Simulator.Bus import Bus
import common.bean.instruction

from enum import Enum


class Simulator:
    def __init__(self):
        """
        Initialize Simulator
        """

        # Wire components to control unit

        # Initialize Bus
        self.dataBus = Bus('DataBus', Config.DATA_BUS_WIDTH)  # Data Bus Component
        self.instBus = Bus('InstructionBus', Config.INST_BUS_WIDTH)  # Instruction Bus Component

        # Initialize data, instruction memory
        self.dataMemory = DictMemory('DataMemory', Config.DATA_MEM_SIZE)  # Data Memory Component (2560*4=10240 Bytes)
        self.instrMemory = DictMemory('InstructionMemory',
                                      Config.INSTR_MEM_SIZE)  # Instruction Memory Component  (256*4=1024 Bytes)

        self.registerDict = {}

        # Initialize General Purpose Registers
        self.registerDict[RegType.GP_FLOAT] = []
        self.registerDict[RegType.GP_INT] = []
        for i in range(Config.GP_FLOAT_REG_NUM):
            self.registerDict[RegType.GP_FLOAT].append(FloatRegister('F' + str(i), i))
        for i in range(Config.GP_INT_REG_NUM):
            self.registerDict[RegType.GP_INT].append(IntRegister('R' + str(i), i))

        # Initialize Special Purpose Registers
        self.registerDict[RegType.SP_PC] = PC('PC')
        self.registerDict[RegType.SP_IAR] = IAR('IAR')
        self.registerDict[RegType.SP_DAR] = DAR('DAR')
        self.registerDict[RegType.SP_IR] = IR('IR')

        # Initialize Function units
        self.funcUnitDict = {}
        fuClasses = [IntFU, FPIntDivFU, FPAdderFU, FPIntMulFU]
        fuPrefix = ['Int', 'FPDiv', 'FPAdd', 'FPMul']
        for i, fuClass in enumerate(fuClasses):
            fuType = fuClass._type  # We just want to get the type of fuClass.We have to access it through an instance.
            fuType:Config.FUType
            for j in range(fuType.quantity):
                fuInstance = fuClass(fuPrefix[i] + str(j),self.dataMemory, self.instrMemory,
                 self.dataBus, self.instBus, self.registerDict)
                self.funcUnitDict[fuInstance.id] = fuInstance

        # Initialize ControlUnit
        self.controlUnit = ControlUnit(0, self.dataMemory, self.instrMemory, self.dataBus, self.instBus,
                                       self.registerDict,
                                       self.funcUnitDict)
