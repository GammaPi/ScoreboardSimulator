from View.bean.instruction_extend import InstructionExtend
from View.bean.instruction_full_status import InstructionFullStatus
from View.bean.ui_data import UIData
from View.bean.workflow import Workflow
from common.bean.function_unit import FunctionUnit
from common.bean.stall import stall
from common.bean.function_unit_status import FunctionUnitStatus
from common.bean.instruction import Instruction
from common.bean.register_status import RegisterStatus
from common.bean.register_value import RegisterValue


class UiController:
    def __init__(self):
        self.workflow = Workflow()

    def start(self):  # UI start function, called only in the start phase
        self.workflow.workflow()

    def getFinalDataToCycle(self, cycleNumber):  # return UIData
        return Workflow.toUIData(cycleNumber)


class UiTestController(UiController):
    def getFinalDataToCycle(self, cycleNumber):  # return UIData
        uiData = UIData()

        uiData.registerStatusList = [RegisterStatus.newRegisterStatus("r1", "inter1"),
                                     RegisterStatus.newRegisterStatus("r2", "inter2")]
        uiData.registerValueList = [RegisterValue.newRegisterValue("r1", "1"),
                                    RegisterValue.newRegisterValue("r1", "2")]

        instruction1 = Instruction.newInstruction(1, "tag1", "address1", "name1", "format1", "operandLeftName1",
                                                  "operandRightName1", "destinationName1")
        instruction2 = Instruction.newInstruction(2, "tag2", "address2", "name2", "format2", "operandLeftName2",
                                                  "operandRightName2", "destinationName2")
        instructionFullStatus1 = InstructionFullStatus()
        instructionFullStatus1.instruction = instruction1
        instructionFullStatus1.issueStartCycle = 1
        instructionFullStatus1.readStartCycle = 1
        instructionFullStatus1.exeStartCycle = 1
        instructionFullStatus1.writeResultStartCycle = 1

        instructionFullStatus2 = InstructionFullStatus()
        instructionFullStatus2.instruction = instruction2
        instructionFullStatus2.issueStartCycle = 2
        instructionFullStatus2.readStartCycle = 2
        instructionFullStatus2.exeStartCycle = 2
        instructionFullStatus2.writeResultStartCycle = 2

        instructionExtend1 = InstructionExtend()
        instructionExtend1.instruction = instruction1
        instructionExtend1.operationCode = "operation1"

        instructionExtend2 = InstructionExtend()
        instructionExtend2.instruction = instruction1
        instructionExtend2.operationCode = "operation2"

        uiData.instructionFullStatusList = [instructionFullStatus1, instructionFullStatus2]
        uiData.instructionExtendList = [instructionExtend1, instructionExtend2]

        uiData.functionUnitStatus = FunctionUnitStatus.newFunctionUnitStatus(
            [FunctionUnit.newFunctionUnit("name1", "busy1", "op1", "des1", "fi1", "fj1", "fk1", "qj1", "qk1", "rj1",
                                          "rk1"),
             FunctionUnit.newFunctionUnit("name2", "busy2", "op2", "des2", "fi2", "fj2", "fk2", "qj2", "qk2", "rj2",
                                          "rk2")])

        uiData.stallList = [stall.newStall("type1", "dependToRegister1", "dependFromRegister1"),
                            stall.newStall("type2", "dependToRegister2", "dependFromRegister2")]
        uiData.log = "test log"
        uiData.ProgramCounter = "pc"
        return uiData
