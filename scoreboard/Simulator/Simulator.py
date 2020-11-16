from Simulator.ControlUnit import ControlUnit
from Simulator.Memory import DictMemory
from Simulator.FunctionUnit import IntFU, FPIntDivFU, FPAdderFU, FPIntMulFU
from Simulator.Registers import IntRegister, FloatRegister, PC, IAR, DAR, IR
from Simulator.AbstractHW import RegType, AbstractFunctionUnit, InternalInst, AbstractRegister, StallInfo, FuStatus
import Simulator.Config as Config
from Simulator.Bus import Bus
from common.bean.frame import Frame
from common.bean.function_unit_status import FunctionUnitStatus
from common.bean.instruction_status import InstructionStatus
from common.bean.instruction import Instruction
from common.bean.function_unit_status import FunctionUnitStatus
from common.bean.function_unit import FunctionUnit
from common.bean.register_status import RegisterStatus
from common.bean.register_value import RegisterValue
from common.bean.stall import stall
from View.bean.ui_data import UIData
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
            self.registerDict[RegType.GP_FLOAT].append(FloatRegister('F' + str(i)))
        for i in range(Config.GP_INT_REG_NUM):
            self.registerDict[RegType.GP_INT].append(IntRegister('R' + str(i)))

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
            fuType: Config.FUType
            for j in range(fuType.quantity):
                fuInstance = fuClass(fuPrefix[i] + str(j), self.dataMemory, self.instrMemory,
                                     self.dataBus, self.instBus, self.registerDict)
                self.funcUnitDict[fuInstance.id] = fuInstance

        # Initialize ControlUnit
        self.controlUnit = ControlUnit(0, self.dataMemory, self.instrMemory, self.dataBus, self.instBus,
                                       self.registerDict,
                                       self.funcUnitDict)
        # Output Frame List
        self.frameList = []

    def tick(self):
        self.controlUnit.tick()
        self._writeLog()

    def _writeLog(self):
        frame = Frame()
        frame.currentCycle = self.controlUnit.cycleCounter - 1
        frame.ProgramCounter = str(self.controlUnit.PC.value)
        # todo: Stall list
        frame.stallList = []

        frame.instructionStatusList = [
        ]

        instrStatusList = []
        for key, unit in self.funcUnitDict.items():
            if unit.fuStatusTable.busy or unit.justWb:
                instrStatusList.append(unit._instruction)
                unit.justWb = False

        for instruction in instrStatusList:

            curStatusName = None
            if instruction.issueStartCycle is not None and instruction.readOpStartCycle is None:
                curStatusName = "issue"
            elif instruction.readOpStartCycle is not None and instruction.execStartCycle is None:
                curStatusName = "read"
            elif instruction.execStartCycle is not None and instruction.wbStartCycle is None:
                curStatusName = "execute"
            elif instruction.wbStartCycle is not None:
                curStatusName = "wb"
            else:
                assert False
            if instruction.fu.status in [FuStatus.WAR, FuStatus.RAW]:
                curStatusName = "stall"

            # todo: Am I wrong for (address field)

            if instruction.instrType in [Config.InstrType.BEQ, Config.InstrType.BNE, Config.InstrType.BEQZ,
                                         Config.InstrType.BNEZ]:
                frame.instructionStatusList.append(
                    InstructionStatus.newInstructionStatus(
                        Instruction.newInstruction(issueCycle=instruction.issueStartCycle, tag="",
                                                   address=str(instruction.address),
                                                   name=instruction.instrType.opName,
                                                   format=instruction.instrType.instFormat.uiName,
                                                   operandLeftName=instruction.src1Reg.name,
                                                   operandRightName=instruction.src2Reg.name if instruction.src1Reg else "",
                                                   destinationName=str(instruction.immed)), curStatusName))
            if instruction.instrType.instFormat in [Config.InstrFormat.I_FORMAT, Config.InstrFormat.FI_FORMAT]:
                frame.instructionStatusList.append(
                    InstructionStatus.newInstructionStatus(
                        Instruction.newInstruction(issueCycle=instruction.issueStartCycle, tag="",
                                                   address=str(instruction.address),
                                                   name=instruction.instrType.opName,
                                                   format=instruction.instrType.instFormat.uiName,
                                                   operandLeftName=instruction.src1Reg.name,
                                                   operandRightName=str(instruction.immed),
                                                   destinationName=instruction.dstReg.name if instruction.dstReg else ""),
                        curStatusName))

            elif instruction.instrType.instFormat in [Config.InstrFormat.R_FORMAT, Config.InstrFormat.FR_FORMAT]:

                frame.instructionStatusList.append(
                    InstructionStatus.newInstructionStatus(
                        Instruction.newInstruction(issueCycle=instruction.issueStartCycle, tag="",
                                                   address=str(instruction.address),
                                                   name=instruction.instrType.opName,
                                                   format=instruction.instrType.instFormat.uiName,
                                                   operandLeftName=instruction.src1Reg.name,
                                                   operandRightName=instruction.src2Reg.name,
                                                   destinationName=instruction.dstReg.name if instruction.dstReg else ""),
                        curStatusName))
            elif instruction.instrType.instFormat in [Config.InstrFormat.J_FORMAT]:
                InstructionStatus.newInstructionStatus(
                    Instruction.newInstruction(issueCycle=instruction.issueStartCycle, tag="",
                                               address=str(instruction.address),
                                               name=instruction.instrType.opName,
                                               format=instruction.instrType.instFormat.uiName,
                                               operandLeftName='',
                                               operandRightName=str(instruction.immed),
                                               destinationName=instruction.dstReg.name if instruction.dstReg else ""),
                    curStatusName)
            elif instruction.instrType.instFormat in [Config.InstrFormat.SPECIAL]:
                frame.instructionStatusList.append(
                    InstructionStatus.newInstructionStatus(
                        Instruction.newInstruction(issueCycle=instruction.issueStartCycle, tag="",
                                                   address=str(instruction.address),
                                                   name=instruction.instrType.opName,
                                                   format=instruction.instrType.instFormat.uiName,
                                                   operandLeftName='',
                                                   operandRightName='',
                                                   destinationName=''), curStatusName))
            else:
                assert False

        functionUnitList = []

        for key, val in self.controlUnit.funcUnitDict.items():
            val: AbstractFunctionUnit
            fuStatusTable = val.fuStatusTable
            # todo: des?!!?
            functionUnitList.append(FunctionUnit.newFunctionUnit(name=key,
                                                                 busy=str(fuStatusTable.busy),
                                                                 op=str(fuStatusTable.operator),
                                                                 des="",
                                                                 fi=str(fuStatusTable.fi),
                                                                 fj=str(fuStatusTable.fj),
                                                                 fk=str(fuStatusTable.fk),
                                                                 qj=str(fuStatusTable.qj),
                                                                 qk=str(fuStatusTable.qk),
                                                                 rj=str(fuStatusTable.rj),
                                                                 rk=str(fuStatusTable.rk)))

        frame.functionUnitStatus = FunctionUnitStatus.newFunctionUnitStatus(functionUnitList)

        frame.registerStatusList = []
        for key, val in self.controlUnit.regStatusTable.items():
            frame.registerStatusList.append(RegisterStatus.newRegisterStatus(key, str(val)))

        registerValueList = []
        for reg in self.controlUnit.registerDict[RegType.GP_INT]:
            registerValueList.append(RegisterValue.newRegisterValue(reg.name, str(reg.read())))
        for freg in self.controlUnit.registerDict[RegType.GP_FLOAT]:
            registerValueList.append(RegisterValue.newRegisterValue(freg.name, str(freg.read())))
        frame.registerValueList = registerValueList
        frame.log = ""

        stallList = []
        for stallInfo in self.controlUnit.stallList:
            if stallInfo.stallType == StallInfo.Type.STRUCTURAL:
                stallList.append(
                    stall.newStall(type=stallInfo.stallType.name,
                                   dependToRegister=str(stallInfo.depTo)+"(FU)",
                                   dependFromRegister=str(stallInfo.depFrom)+"(instr addr)"))
            else:
                stallList.append(
                    stall.newStall(type=stallInfo.stallType.name,
                                   dependToRegister=str(stallInfo.depTo) + "(Reg)",
                                   dependFromRegister=str(stallInfo.depFrom) + "(Reg)"))
        frame.stallList = stallList

        self.frameList.append(frame)

    def finished(self):
        return self.controlUnit.execFinished


def finished(self):
    return self.controlUnit.execFinished
