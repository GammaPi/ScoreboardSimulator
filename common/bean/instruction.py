class Instruction:
    issueCycle: int  # as id
    tag: str  # for example : loop
    address: str
    name = None
    format: str
    operandLeftName: str = None
    operandRightName: str = None
    destinationName: str = None