# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets

from View.ui.MyMainWindow import MyMainWindow


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1202, 689)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.rgStatusValueTableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.rgStatusValueTableWidget.setGeometry(QtCore.QRect(10, 470, 891, 91))
        self.rgStatusValueTableWidget.setObjectName("rgStatusValueTableWidget")
        self.rgStatusValueTableWidget.setColumnCount(1)
        self.rgStatusValueTableWidget.setRowCount(2)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.rgStatusValueTableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.rgStatusValueTableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.rgStatusValueTableWidget.setHorizontalHeaderItem(0, item)
        self.logBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.logBrowser.setGeometry(QtCore.QRect(10, 570, 891, 61))
        self.logBrowser.setObjectName("logBrowser")
        self.stallTableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.stallTableWidget.setGeometry(QtCore.QRect(730, 260, 461, 192))
        self.stallTableWidget.setObjectName("stallTableWidget")
        self.stallTableWidget.setColumnCount(3)
        self.stallTableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.stallTableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.stallTableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.stallTableWidget.setHorizontalHeaderItem(2, item)
        self.stallTableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.stallTableWidget.horizontalHeader().setDefaultSectionSize(138)
        self.instructionStatusTableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.instructionStatusTableWidget.setGeometry(QtCore.QRect(10, 0, 1181, 231))
        self.instructionStatusTableWidget.setObjectName("instructionStatusTableWidget")
        self.instructionStatusTableWidget.setColumnCount(11)
        self.instructionStatusTableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.instructionStatusTableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.instructionStatusTableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.instructionStatusTableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.instructionStatusTableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.instructionStatusTableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.instructionStatusTableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.instructionStatusTableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.instructionStatusTableWidget.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.instructionStatusTableWidget.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.instructionStatusTableWidget.setHorizontalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.instructionStatusTableWidget.setHorizontalHeaderItem(10, item)
        self.instructionStatusTableWidget.horizontalHeader().setDefaultSectionSize(104)
        self.functionUnitStatusTableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.functionUnitStatusTableWidget.setGeometry(QtCore.QRect(10, 260, 711, 191))
        self.functionUnitStatusTableWidget.setObjectName("functionUnitStatusTableWidget")
        self.functionUnitStatusTableWidget.setColumnCount(10)
        self.functionUnitStatusTableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.functionUnitStatusTableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.functionUnitStatusTableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.functionUnitStatusTableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.functionUnitStatusTableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.functionUnitStatusTableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.functionUnitStatusTableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.functionUnitStatusTableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.functionUnitStatusTableWidget.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.functionUnitStatusTableWidget.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.functionUnitStatusTableWidget.setHorizontalHeaderItem(9, item)
        self.functionUnitStatusTableWidget.horizontalHeader().setDefaultSectionSize(68)
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(920, 470, 261, 111))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.cycleLabel = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(32)
        self.cycleLabel.setFont(font)
        self.cycleLabel.setObjectName("cycleLabel")
        self.verticalLayout.addWidget(self.cycleLabel)
        self.pcLabel = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(32)
        self.pcLabel.setFont(font)
        self.pcLabel.setObjectName("pcLabel")
        self.verticalLayout.addWidget(self.pcLabel)
        self.widget1 = QtWidgets.QWidget(self.centralwidget)
        self.widget1.setGeometry(QtCore.QRect(910, 590, 275, 32))
        self.widget1.setObjectName("widget1")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget1)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.upStepButton = QtWidgets.QPushButton(self.widget1)
        self.upStepButton.setObjectName("upStepButton")
        self.horizontalLayout.addWidget(self.upStepButton)
        self.nextStepButton = QtWidgets.QPushButton(self.widget1)
        self.nextStepButton.setEnabled(True)
        self.nextStepButton.setObjectName("nextStepButton")
        self.horizontalLayout.addWidget(self.nextStepButton)
        self.resetButton = QtWidgets.QPushButton(self.widget1)
        self.resetButton.setObjectName("resetButton")
        self.horizontalLayout.addWidget(self.resetButton)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1202, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.nextStepButton.clicked.connect(MainWindow.nextStepButtonClick)
        self.upStepButton.clicked.connect(MainWindow.upStepButtonClick)
        self.resetButton.clicked.connect(MainWindow.resetButtonClick)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ScoreBoardSimulator"))
        item = self.rgStatusValueTableWidget.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "FunctionUnit"))
        item = self.rgStatusValueTableWidget.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "Value"))
        item = self.rgStatusValueTableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Registers"))
        self.logBrowser.setHtml(_translate("MainWindow",
                                           "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                           "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                           "p, li { white-space: pre-wrap; }\n"
                                           "</style></head><body style=\" font-family:\'.SF NS Text\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
                                           "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">Message:</span></p></body></html>"))
        item = self.stallTableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "StallType"))
        item = self.stallTableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "DependTo"))
        item = self.stallTableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "DependFrom"))
        item = self.instructionStatusTableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "InstructionNam"))
        item = self.instructionStatusTableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "dest"))
        item = self.instructionStatusTableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "j"))
        item = self.instructionStatusTableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "k"))
        item = self.instructionStatusTableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Issue"))
        item = self.instructionStatusTableWidget.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "ReadOperands"))
        item = self.instructionStatusTableWidget.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "Exe"))
        item = self.instructionStatusTableWidget.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "WriteResult"))
        item = self.instructionStatusTableWidget.horizontalHeaderItem(8)
        item.setText(_translate("MainWindow", "Address"))
        item = self.instructionStatusTableWidget.horizontalHeaderItem(9)
        item.setText(_translate("MainWindow", "Lable"))
        item = self.instructionStatusTableWidget.horizontalHeaderItem(10)
        item.setText(_translate("MainWindow", "OperationCode"))
        item = self.functionUnitStatusTableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Name"))
        item = self.functionUnitStatusTableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Busy"))
        item = self.functionUnitStatusTableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Op"))
        item = self.functionUnitStatusTableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "DestFi"))
        item = self.functionUnitStatusTableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "S1Fj"))
        item = self.functionUnitStatusTableWidget.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "S2Fk"))
        item = self.functionUnitStatusTableWidget.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "FUQj"))
        item = self.functionUnitStatusTableWidget.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "FUQk"))
        item = self.functionUnitStatusTableWidget.horizontalHeaderItem(8)
        item.setText(_translate("MainWindow", "Fj?Rj"))
        item = self.functionUnitStatusTableWidget.horizontalHeaderItem(9)
        item.setText(_translate("MainWindow", "Fk?Rk"))
        self.cycleLabel.setText(_translate("MainWindow", "Cycle:0"))
        self.pcLabel.setText(_translate("MainWindow", "PC:0"))
        self.upStepButton.setText(_translate("MainWindow", "Up Step"))
        self.nextStepButton.setText(_translate("MainWindow", "Next Step"))
        self.resetButton.setText(_translate("MainWindow", "ReSet"))

    def uiStart(self):
        import sys

        app = QtWidgets.QApplication(sys.argv)
        # MainWindow = QtWidgets.QMainWindow()
        MainWindow = MyMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)
        MainWindow.setUI(ui)
        MainWindow.show()
        sys.exit(app.exec_())
