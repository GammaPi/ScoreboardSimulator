import json
from common.bean.frame import Frame
from common.bean.function_unit_status import FunctionUnitStatus
from common.bean.instruction_status import InstructionStatus
from common.bean.instruction import Instruction
from common.bean.function_unit_status import FunctionUnitStatus
from common.bean.function_unit import FunctionUnit
from common.bean.register_status import RegisterStatus
from common.bean.register_value import RegisterValue
from common.bean.stall import stall
from View.bean.ui_data import UIData


def frame1():
    frame = Frame()

    frame.currentCycle = 1

    frame.ProgramCounter = "0000"

    frame.stallList = [stall.newStall("RAW", "R2", "R1"),
                       stall.newStall("WAW", "R3", "R1"),
                       stall.newStall("WAR", "R4", "R1")]

    frame.instructionStatusList = [InstructionStatus.newInstructionStatus(Instruction.newInstruction(1, "", "0000", "J", "J", "12", "", ""), "issue")]

    frame.functionUnitStatus = FunctionUnitStatus.newFunctionUnitStatus([
        FunctionUnit.newFunctionUnit("FUname", "yes", "", "", "", "", "", "", "", "", ""),
        FunctionUnit.newFunctionUnit("FUname2", "no", "", "", "", "", "", "", "", "", "")
    ])
    frame.registerStatusList = [RegisterStatus.newRegisterStatus("R1", "ADD"), RegisterStatus.newRegisterStatus("R2", "SUB")]
    frame.registerValueList = [RegisterValue.newRegisterValue("R1", "10000"), RegisterValue.newRegisterValue("R2", "20000")]
    frame.log = "hello world"

    return frame


def frame2():
    frame = Frame()

    frame.currentCycle = 2

    frame.ProgramCounter = "0004"

    frame.stallList = []

    frame.instructionStatusList = [
        InstructionStatus.newInstructionStatus(Instruction.newInstruction(1, "", "0000", "J", "J", "12", "", ""), "read"),
        InstructionStatus.newInstructionStatus(Instruction.newInstruction(2, "", "0004", "ADD.D", "R", "r1", "r2", "r3"), "issue"),
        InstructionStatus.newInstructionStatus(Instruction.newInstruction(3, "", "0008", "DADDI", "I", "r12", "100", "r1"), "issue"),
    ]

    frame.functionUnitStatus = FunctionUnitStatus.newFunctionUnitStatus([
        FunctionUnit.newFunctionUnit("FUname", "yes", "", "", "", "", "", "", "", "", ""),
    ])
    frame.registerStatusList = [RegisterStatus.newRegisterStatus("R1", "ADD"), RegisterStatus.newRegisterStatus("R2", "SUB")]
    frame.registerValueList = [RegisterValue.newRegisterValue("R1", "10000"), RegisterValue.newRegisterValue("R2", "20000")]
    frame.log = "hello world 2"

    return frame


def writeTestTmpFile():
    frames = []
    frames.append(frame1())
    frames.append(frame2())
    with open("tmp", 'w') as f:
        json.dump(frames, f, default=lambda obj: obj.__dict__, indent=4)


def print_UID(UID: UIData, f):
    print("--------------", file=f)
    print("---instructionFullStatusList:", file=f)
    for IFS in UID.instructionFullStatusList:
        print('\n'.join(['%s:%s' % item for item in IFS.instruction.__dict__.items()]), file=f)
        print(IFS.issueStartCycle, file=f)
        print(IFS.readStartCycle, file=f)
        print(IFS.exeStartCycle, file=f)
        print(IFS.writeResultStartCycle, file=f)
    print("---functionUnitStatus:", file=f)
    for FUS in UID.functionUnitStatus.functionUnitList:
        print('\n'.join(['%s:%s' % item for item in FUS.__dict__.items()]), file=f)
    print("---registerStatusList:", file=f)
    for RS in UID.registerStatusList:
        print('\n'.join(['%s:%s' % item for item in RS.__dict__.items()]), file=f)
    print("---registerValueList:", file=f)
    for RV in UID.registerValueList:
        print('\n'.join(['%s:%s' % item for item in RV.__dict__.items()]), file=f)
    print("---instructionExtendList:", file=f)
    for IE in UID.instructionExtendList:
        print('\n'.join(['%s:%s' % item for item in IE.instruction.__dict__.items()]), file=f)
        print(IE.operationCode, file=f)
    print("---stallList:", file=f)
    for S in UID.stallList:
        print('\n'.join(['%s:%s' % item for item in S.__dict__.items()]), file=f)
    print("---log:", file=f)
    print(UID.log, file=f)
    print("---ProgramCounter:", file=f)
    print(UID.ProgramCounter, file=f)







