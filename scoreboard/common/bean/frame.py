from common.bean.function_unit_status import FunctionUnitStatus


class Frame:  # input file is in Frame list

    def __init__(self, entries: dict = None):
        if entries is None:
            entries = {}
        for k, v in entries.items():
            if isinstance(v, dict):
                self.__dict__[k] = Frame(v)
            else:
                self.__dict__[k] = v

    currentCycle: int
    ProgramCounter: str
    stallList: list  # stalls happened in current cycle
    instructionStatusList: list  # InstructionStatus list  only updated instruction in current cycle
    functionUnitStatus: FunctionUnitStatus
    registerStatusList: list  # RegisterStatus list
    registerValueList: list  # RegisterValue list
    log: str
