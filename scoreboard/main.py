from Simulator.AbstractHW import RegType
from Simulator.Simulator import Simulator
from Simulator.Assembler import Assembler
import json

from View.ui.mainwindow import Ui_MainWindow

if __name__ == '__main__':
    assembler = Assembler("testLec9ScoreboardingExample.in")
    simulator = Simulator()

    # todo: specify instruction starting point.Currently assume 0.
    # Write instructions into instruction memory.
    for i in range(len(assembler.instructions)):
        simulator.instrMemory.write(i, assembler.instructions[i])

    # Initialize some registers and data memory
    intRegisters = simulator.registerDict[RegType.GP_INT]
    floatRegisters = simulator.registerDict[RegType.GP_INT]
    for i in range(len(intRegisters)):
        simulator.registerDict[RegType.GP_INT][i].write(i)
    for i in range(len(floatRegisters)):
        simulator.registerDict[RegType.GP_FLOAT][i].write(float(i))
    for i in range(simulator.dataMemory.totalSize):
        simulator.dataMemory.write(i, i)

    # Keep calling tick until finished
    while not simulator.finished() and simulator.controlUnit.cycleCounter < 1000:
        simulator.tick()

    with open("tmp", 'w') as f:
        json.dump(simulator.frameList, f, default=lambda obj: obj.__dict__, indent=4)
    mainwindow = Ui_MainWindow()
    mainwindow.uiStart()
