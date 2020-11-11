from common.bean.function_unit_status import FunctionUnitStatus


class UIData:
    instructionFullStatusList: list  # InstructionFullStatus list  todo needs status update
    functionUnitStatus: FunctionUnitStatus
    registerStatusList: list  # RegisterStatus list
    registerValueList: list  # RegisterValue list
    instructionExtendList: list  # InstructionExtend   todo needs operationCode translation
    stallList: list  # stalls happened in current cycle
    log: str
