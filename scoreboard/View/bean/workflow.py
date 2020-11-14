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

    path: str = "tmp"
    frames: list = []
    UIDs: list = []
    IFSList: list = []

    @staticmethod
    def readTmpFile(self, path: str):
        with open(path, 'r') as f:
            self.frames = json.load(f)

    @staticmethod
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
            else:
                print("Unknown Stage Status..Aborting")
                os.abort()
        return self.IFSList

    @staticmethod
    def buildExtendList(sources: list) -> list:
        results = []
        for source in sources:
            result = InstructionExtend()
            result.instruction = source.instruction
            result.operationCode = opcodesOf(source.instruction)
            results.append(result)
        return results

    @staticmethod
    def buildUIData(self):
        for frameDict in self.frames:
            UID = UIData()
            frame = Frame.newFrame(frameDict)
            UID.instructionFullStatusList = self.updateIFSList(self, frame.currentCycle, frame.instructionStatusList)
            UID.functionUnitStatus = frame.functionUnitStatus
            UID.registerStatusList = frame.registerStatusList
            UID.registerValueList = frame.registerValueList
            UID.instructionExtendList = self.buildExtendList(UID.instructionFullStatusList)
            UID.stallList = frame.stallList
            UID.log = frame.log
            UID.ProgramCounter = frame.ProgramCounter
            self.UIDs.append(copy.deepcopy(UID))

    @staticmethod
    def toUIData(self, dst: int) -> UIData:
        return self.UIDs[dst]

    @staticmethod
    def workflow(self):
        writeTestTmpFile()
        # callSimulator()
        self.readTmpFile(self, self.path)
        self.buildUIData(self)
        # callUI()

        f = open("out.txt", "w")
        print_UID(self.toUIData(self, 0), f)
        print_UID(self.toUIData(self, 1), f)
        f.close()



Workflow.workflow(Workflow)
