import json
import os
from common.bean.frame import Frame
from common.bean.instruction_status import InstructionStatus
from View.bean.ui_data import UIData
from View.bean.instruction_full_status import InstructionFullStatus
from View.bean.instruction_extend import InstructionExtend
from View.bean.opcode import opcodesOf
from View.bean.debug import writeTestTmpFile


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
        results = [InstructionExtend]
        for source in sources:
            result = InstructionExtend()
            result.instruction = source.instruction
            result.operationCode = opcodesOf(source.instruction)
            results.append(result)
        return results

    @staticmethod
    def buildUIData(self):
        UID = UIData()
        for frame in self.frames:
            frame = Frame(frame)
            UID.instructionFullStatusList = self.updateIFSList(self, frame.currentCycle, frame.instructionStatusList)
            UID.functionUnitStatus = frame.functionUnitStatus
            UID.registerStatusList = frame.registerStatusList
            UID.registerValueList = frame.registerValueList
            UID.instructionExtendList = self.buildExtendList(UID.instructionFullStatusList)
            UID.stallList = frame.stallList
            UID.log = frame.log
            UID.ProgramCounter = frame.ProgramCounter
            self.UIDs.append(UID)

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
        print(self.toUIData(self, 0))


Workflow.workflow(Workflow)
