from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QTableWidgetItem

from View.controller.ui_controller import UiController, UiTestController


class MyMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.cycleNumber = 0
        # self.uiController = UiController()
        self.uiController = UiTestController()
        self.uiController.start()
        # self.setupUi(self)

    def setUI(self, ui):
        self.ui = ui

    def __clearAll(self):
        self.ui.cycleLabel.setText(QtCore.QCoreApplication.translate("MainWindow", "Cycle:" + str(self.cycleNumber)))
        self.ui.pcLabel.setText(QtCore.QCoreApplication.translate("MainWindow", "PC:0"))
        self.ui.logBrowser.setText("Message:")
        self.ui.functionUnitStatusTableWidget.clearContents()
        self.ui.stallTableWidget.clearContents()
        self.ui.instructionStatusTableWidget.clearContents()
        self.ui.rgStatusValueTableWidget.clearContents()
        self.ui.rgStatusValueTableWidget.setColumnCount(1)
        self.ui.rgStatusValueTableWidget.setHorizontalHeaderItem(0, QTableWidgetItem("Registers"))
        bondFont = self.ui.rgStatusValueTableWidget.horizontalHeader().font()
        bondFont.setBold(True)
        self.ui.rgStatusValueTableWidget.horizontalHeader().setFont(bondFont)

    def __updateView(self):
        self.__clearAll()
        uiData = self.uiController.getFinalDataToCycle(self.cycleNumber)
        instructionFullStatusList = uiData.instructionFullStatusList
        instructionExtendList = uiData.instructionExtendList
        functionUnitStatusList = uiData.functionUnitStatus.functionUnitList
        registerStatusList = uiData.registerStatusList
        registerValueList = uiData.registerValueList
        stallList = uiData.stallList
        programCounter = uiData.ProgramCounter
        log = uiData.log

        self.ui.functionUnitStatusTableWidget.setRowCount(len(functionUnitStatusList))
        for index, value in enumerate(functionUnitStatusList):
            # todo what is des in functionUnit
            self.ui.functionUnitStatusTableWidget.setItem(index, 0, QTableWidgetItem(value.name))
            self.ui.functionUnitStatusTableWidget.setItem(index, 1, QTableWidgetItem(value.busy))
            self.ui.functionUnitStatusTableWidget.setItem(index, 2, QTableWidgetItem(value.op))
            self.ui.functionUnitStatusTableWidget.setItem(index, 3, QTableWidgetItem(value.fi))
            self.ui.functionUnitStatusTableWidget.setItem(index, 4, QTableWidgetItem(value.fj))
            self.ui.functionUnitStatusTableWidget.setItem(index, 5, QTableWidgetItem(value.fk))
            self.ui.functionUnitStatusTableWidget.setItem(index, 6, QTableWidgetItem(value.qj))
            self.ui.functionUnitStatusTableWidget.setItem(index, 7, QTableWidgetItem(value.qk))
            self.ui.functionUnitStatusTableWidget.setItem(index, 8, QTableWidgetItem(value.rj))
            self.ui.functionUnitStatusTableWidget.setItem(index, 9, QTableWidgetItem(value.rk))

        self.ui.stallTableWidget.setRowCount(len(stallList))
        for index, value in enumerate(stallList):
            self.ui.stallTableWidget.setItem(index, 0, QTableWidgetItem(value.type))
            self.ui.stallTableWidget.setItem(index, 1, QTableWidgetItem(value.dependToRegister))
            self.ui.stallTableWidget.setItem(index, 2, QTableWidgetItem(value.dependFromRegister))

        self.ui.instructionStatusTableWidget.setRowCount(len(instructionFullStatusList))
        for index, value in enumerate(instructionFullStatusList):
            instruction = value.instruction
            self.ui.instructionStatusTableWidget.setItem(index, 0, QTableWidgetItem(instruction.name))
            self.ui.instructionStatusTableWidget.setItem(index, 1, QTableWidgetItem(instruction.destinationName))
            self.ui.instructionStatusTableWidget.setItem(index, 2, QTableWidgetItem(instruction.operandLeftName))
            self.ui.instructionStatusTableWidget.setItem(index, 3, QTableWidgetItem(instruction.operandRightName))
            self.ui.instructionStatusTableWidget.setItem(index, 4, QTableWidgetItem(str(value.issueStartCycle)))
            self.ui.instructionStatusTableWidget.setItem(index, 5, QTableWidgetItem(str(value.readStartCycle)))
            self.ui.instructionStatusTableWidget.setItem(index, 6, QTableWidgetItem(str(value.exeStartCycle)))
            self.ui.instructionStatusTableWidget.setItem(index, 7, QTableWidgetItem(str(value.writeResultStartCycle)))
        for index, value in enumerate(instructionExtendList):
            instruction = value.instruction
            self.ui.instructionStatusTableWidget.setItem(index, 8, QTableWidgetItem(instruction.address))
            self.ui.instructionStatusTableWidget.setItem(index, 9, QTableWidgetItem(instruction.tag))
            self.ui.instructionStatusTableWidget.setItem(index, 10, QTableWidgetItem(value.operationCode))

        self.ui.rgStatusValueTableWidget.setColumnCount(len(registerStatusList))
        for index, value in enumerate(registerStatusList):
            self.ui.rgStatusValueTableWidget.setHorizontalHeaderItem(index, QTableWidgetItem(value.registerName))
            self.ui.rgStatusValueTableWidget.setItem(0, index, QTableWidgetItem(value.functionUnitName))
        bondFont = self.ui.rgStatusValueTableWidget.horizontalHeader().font()
        bondFont.setBold(True)
        self.ui.rgStatusValueTableWidget.horizontalHeader().setFont(bondFont)
        for index, value in enumerate(registerValueList):
            self.ui.rgStatusValueTableWidget.setItem(1, index, QTableWidgetItem(value.value))
        self.ui.logBrowser.setText(log)
        self.ui.cycleLabel.setText(QtCore.QCoreApplication.translate("MainWindow", "Cycle:" + str(self.cycleNumber)))
        self.ui.pcLabel.setText(QtCore.QCoreApplication.translate("MainWindow", "PC:" + programCounter))

    def nextStepButtonClick(self):
        self.cycleNumber += 1
        self.__updateView()

    def upStepButtonClick(self):
        if self.cycleNumber == 0:
            return
        self.cycleNumber -= 1
        if self.cycleNumber == 0:
            self.__clearAll()
            return
        self.__updateView()

    def resetButtonClick(self):
        self.cycleNumber = 0
        self.__clearAll()
