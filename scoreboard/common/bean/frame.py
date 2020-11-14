from common.bean.function_unit_status import FunctionUnitStatus
from common.bean.function_unit import FunctionUnit
from common.bean.instruction_status import InstructionStatus
from common.bean.instruction import Instruction
from common.bean.register_status import RegisterStatus
from common.bean.register_value import RegisterValue
from common.bean.stall import stall


class Frame:  # input file is in Frame list

    @staticmethod
    def newFrame(entries: dict):
        frame = Frame()

        frame.currentCycle = entries.get("currentCycle")

        frame.ProgramCounter = entries.get("ProgramCounter")

        frame.stallList = []
        stallList = entries.get("stallList")
        for ST in stallList:
            frame.stallList.append(stall.newStall(ST["type"], ST["dependToRegister"], ST["dependFromRegister"]))

        frame.instructionStatusList = []
        instructionStatusList = entries.get("instructionStatusList")
        for IS in instructionStatusList:
            frame.instructionStatusList.append(InstructionStatus.newInstructionStatus(
                Instruction.newInstruction(IS["instruction"]["issueCycle"], IS["instruction"]["tag"],
                                           IS["instruction"]["address"], IS["instruction"]["name"],
                                           IS["instruction"]["format"], IS["instruction"]["operandLeftName"],
                                           IS["instruction"]["operandRightName"], IS["instruction"]["destinationName"]),
                IS["stage"]))

        frame.functionUnitStatus = FunctionUnitStatus.newFunctionUnitStatus([])
        functionUnitList = entries.get("functionUnitStatus").get("functionUnitList")
        for FU in functionUnitList:
            frame.functionUnitStatus.functionUnitList.append(
                FunctionUnit.newFunctionUnit(FU["name"], FU["busy"], FU["op"], FU["des"], FU["fi"], FU["fj"], FU["fk"], FU["qj"], FU["qk"], FU["rj"], FU["rk"])
            )

        frame.registerStatusList = []
        registerStatusList = entries.get("registerStatusList")
        for RS in registerStatusList:
            frame.registerStatusList.append(RegisterStatus.newRegisterStatus(RS["registerName"], RS["functionUnitName"]))

        frame.registerValueList = []
        registerValueList = entries.get("registerValueList")
        for RV in registerValueList:
            frame.registerValueList.append(RegisterValue.newRegisterValue(RV["name"], RV["value"]))

        frame.log = entries.get("log")
        return frame

    currentCycle: int
    ProgramCounter: str
    stallList: list  # stalls happened in current cycle
    instructionStatusList: list  # InstructionStatus list  only updated instruction in current cycle
    functionUnitStatus: FunctionUnitStatus
    registerStatusList: list  # RegisterStatus list
    registerValueList: list  # RegisterValue list
    log: str
