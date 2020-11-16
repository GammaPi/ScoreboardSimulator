import json
import os
import copy
from common.bean.frame import Frame
from common.bean.instruction_status import InstructionStatus
from View.bean.ui_data import UIData
from View.bean.instruction_full_status import InstructionFullStatus
from View.bean.instruction_extend import InstructionExtend
from View.bean.opcode import opcodesOf
from View.bean.debug import writeTestTmpFile, print_UID


class Workflow:
    path: str = "../tmp"
    frames: list = []
    UIDs: list = []
    IFSList: list = []

    def __init__(self):
        self.path = "tmp"
        self.frames = []
        self.realFrames = []
        self.UIDs = []
        self.IFSList = []

    def readTmpFile(self, path: str):
        with open(path, 'r') as f:
            self.frames = json.load(f)

    def updateIFSList(self, currentCycle: int, updates: list) -> list:
        for update in updates:
            if update.stage == "issue":
                newInstrStat = InstructionFullStatus()
                newInstrStat.instruction = update.instruction
                newInstrStat.issueStartCycle = currentCycle
                self.IFSList.append(newInstrStat)
            elif update.stage == "read":
                for IFS in self.IFSList:
                    if IFS.issueStartCycle == update.instruction.issueCycle:
                        IFS.readStartCycle = currentCycle
                        break
            elif update.stage == "execute":
                for IFS in self.IFSList:
                    if IFS.issueStartCycle == update.instruction.issueCycle:
                        IFS.exeStartCycle = currentCycle
                        break
            elif update.stage == "wb":
                for IFS in self.IFSList:
                    if IFS.issueStartCycle == update.instruction.issueCycle:
                        IFS.writeResultStartCycle = currentCycle
                        break
            elif update.stage == "stall":
                pass
            else:
                print("Unknown Stage Status: "+update.stage+"..Aborting")
                os.abort()
        return self.IFSList

    def buildExtendList(self, sources: list) -> list:
        results = []
        for source in sources:
            result = InstructionExtend()
            result.instruction = source.instruction
            result.operationCode = opcodesOf(source.instruction)
            results.append(result)
        return results

    def buildUIData(self):
        for frameDict in self.frames:
            frame = Frame.newFrame(frameDict)
            self.realFrames.append(frame)

        killTarget = []
        for idx, frame in enumerate(self.realFrames):
            for idxInstr, instr in enumerate(frame.instructionStatusList):
                if instr.stage == "execute" and idx != len(self.realFrames)-1:
                    find = False
                    for futureFrame in self.realFrames[idx+1:]:
                        for instr2 in futureFrame.instructionStatusList:
                            if instr.instruction.issueCycle == instr2.instruction.issueCycle and instr2.stage == "execute":
                                killTarget.append([idx, instr.instruction.issueCycle])
                                find = True
                                break
                        if find is True:
                            break

        for idx, frame in enumerate(self.realFrames):
            newISL = []
            for instr in frame.instructionStatusList:
                if [idx, instr.instruction.issueCycle] not in killTarget:
                    newISL.append(instr)
            frame.instructionStatusList = copy.deepcopy(newISL)

        for frame in self.realFrames:
            UID = UIData()
            UID.instructionFullStatusList = self.updateIFSList(frame.currentCycle, frame.instructionStatusList)
            UID.functionUnitStatus = frame.functionUnitStatus
            UID.registerStatusList = frame.registerStatusList
            UID.registerValueList = frame.registerValueList
            UID.instructionExtendList = self.buildExtendList(UID.instructionFullStatusList)
            UID.stallList = frame.stallList
            UID.log = frame.log
            UID.ProgramCounter = frame.ProgramCounter
            self.UIDs.append(copy.deepcopy(UID))


    def toUIData(self, dst: int) -> UIData:
        return self.UIDs[dst]

    def lengthOfUIDs(self):
        return len(self.UIDs)

    def workflow(self):
        # writeTestTmpFile()
        # callSimulator()
        self.readTmpFile(self.path)
        self.buildUIData()
        # callUI()

        # f = open("out.txt", "w")
        # print_UID(self.toUIData(0), f)
        # print_UID(self.toUIData(1), f)
        # f.close()

# Workflow.workflow(Workflow)
