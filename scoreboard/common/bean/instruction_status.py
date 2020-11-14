from common.bean.instruction import Instruction


class InstructionStatus:

    @staticmethod
    def newInstructionStatus(instruction: Instruction, stage: str):
        newInstructionStatus = InstructionStatus()
        newInstructionStatus.instruction = instruction
        newInstructionStatus.stage = stage
        return newInstructionStatus

    instruction: Instruction = None
    stage: str = None


