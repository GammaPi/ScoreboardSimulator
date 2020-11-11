from common.bean.instruction import Instruction


class InstructionFullStatus:
    instruction: Instruction = None
    issueStartCycle: int = None
    readStartCycle: int = None
    exeStartCycle: int = None
    writeResultStartCycle: int = None
