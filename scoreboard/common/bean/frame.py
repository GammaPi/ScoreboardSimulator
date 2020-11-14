from common.bean.function_unit_status import FunctionUnitStatus

class Frame:  # input file is in Frame list
    currentCycle: int
    ProgramCounter: str
    stallList: list  # stalls happened in current cycle
    instructionStatusList: list  # InstructionStatus list  only updated instruction in current cycle
    functionUnitStatus: FunctionUnitStatus
    registerStatusList: list  # RegisterStatus list
    registerValueList: list  # RegisterValue list
    log: str
