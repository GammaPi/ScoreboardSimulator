import os
from common.bean.instruction import Instruction


def numberToBinaryInLength(number: int, length: int) -> str:
    binary = bin(number)[2:]
    binaryInLength = binary.rjust(length, '0')
    return binaryInLength


def opOP(name: str) -> str:
    if name == "":
        return "000000"
    switch = {
        "NOP":      60,
        "HALT":     61,
        "LW":       20,
        "SW":       21,
        "L.D":      40,
        "S.D":      41,
        "ADD.D":    30,
        "SUB.D":    31,
        "MUL.D":    32,
        "DIV.D":    33,
        "DADD":     10,
        "DADDI":    22,
        "DSUB":     11,
        "DSUBI":    23,
        "DMUL":     12,
        "DDIV":     13,
        "BEQ":      24,
        "BNE":      25,
        "BNEZ":     26,
        "J":        50
    }
    number = switch.get(name)
    if number is None:
        print("Unknown instruction name...Aborting")
        os.abort()
    return numberToBinaryInLength(number, 6)


def opRD(name: str) -> str:
    if str == "":
        return "00000"
    number = int("".join(filter(str.isdigit, name)))
    return numberToBinaryInLength(number, 5)


def opRS(name: str) -> str:
    return opRD(name)


def opRT(name: str) -> str:
    return opRD(name)


def opShamt() -> str:
    return "00000"


def opFunc() -> str:
    return "000000"


def opIImmediate(name: str) -> str:
    if str == "":
        return "0000000000000000"
    number = int("".join(filter(str.isdigit, name)))
    return numberToBinaryInLength(number, 16)


def opJImmediate(name: str) -> str:
    if str == "":
        return "00000000000000000000000000"
    number = int("".join(filter(str.isdigit, name)))
    return numberToBinaryInLength(number, 26)


def opcodesOf(instruction: Instruction) -> str:
    opcodes = str()
    if instruction.format == "R" or instruction.format == "FR":
        opcodes += opOP(instruction.name)
        opcodes += opRD(instruction.destinationName)
        opcodes += opRS(instruction.operandLeftName)
        opcodes += opRT(instruction.operandRightName)
        opcodes += opShamt()
        opcodes += opFunc()
    elif instruction.format == "I" or instruction.format == "FI":
        opcodes += opOP(instruction.name)
        opcodes += opRD(instruction.destinationName)
        opcodes += opRS(instruction.operandLeftName)
        opcodes += opIImmediate(instruction.operandRightName)
    elif instruction.format == "J" or instruction.format == "S":
        opcodes += opOP(instruction.name)
        opcodes += opJImmediate(instruction.operandLeftName)
    else:
        print("Unknown Instruction Format...Aborting")
        os.abort()
    if len(opcodes) != 32:
        print("opcodes incorrect: "+opcodes+" Aborting")
        os.abort()
    return opcodes
