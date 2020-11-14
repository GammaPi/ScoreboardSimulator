class Instruction:

    @staticmethod
    def newInstruction(issueCycle: int, tag: str, address: str, name: str, format: str, operandLeftName: str, operandRightName: str, destinationName: str):
        newInstruction = Instruction()
        newInstruction.issueCycle = issueCycle
        newInstruction.tag = tag
        newInstruction.address = address
        newInstruction.name = name
        newInstruction.format = format
        newInstruction.operandLeftName = operandLeftName
        newInstruction.operandRightName = operandRightName
        newInstruction.destinationName = destinationName
        return newInstruction

    issueCycle: int  # as id
    tag: str  # for example : loop
    address: str
    name = None
    format: str
    operandLeftName: str = None
    operandRightName: str = None
    destinationName: str = None