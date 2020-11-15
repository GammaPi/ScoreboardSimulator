from Simulator.AbstractHW import RegType
from Simulator.Simulator import Simulator
from Simulator.Assembler import Assembler

if __name__ == '__main__':
    assembler = Assembler("test2.in")
    simulator = Simulator()
    # Write instructions into instruction memory.
    for i in range(len(assembler.instructions)):
        simulator.instrMemory.write(i, assembler.instructions[i])

    intRegisters=simulator.registerDict[RegType.GP_INT]
    floatRegisters=simulator.registerDict[RegType.GP_INT]
    for i in range(len(intRegisters)):
        simulator.registerDict[RegType.GP_INT][i].write(i)
    for i in range(len(floatRegisters)):
        simulator.registerDict[RegType.GP_INT][i].write(i)

    for i in range(simulator.dataMemory.totalSize):
        simulator.dataMemory.write(i,i)



    while not simulator.finished():
        simulator.tick()

    pass
