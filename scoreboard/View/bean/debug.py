import json
from common.bean.frame import Frame
from common.bean.frame import FunctionUnitStatus


def writeTestTmpFile():
    frames = []
    frame = Frame()

    frame.currentCycle = 1
    frame.ProgramCounter = "1"
    frame.stallList = []
    frame.instructionStatusList = []
    frame.functionUnitStatus = FunctionUnitStatus()
    frame.registerStatusList = []
    frame.registerValueList = []
    frame.log = ""

    frames.append(frame)
    with open("tmp", 'w') as f:
        json.dump(frames, f, default=lambda obj: obj.__dict__, indent=4)


