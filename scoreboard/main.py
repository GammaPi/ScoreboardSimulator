from Simulator.Simulator import Simulator
from Simulator.Assembler import Assembler

if __name__ == '__main__':
    assembler = Assembler("test2.in")
    simulator = Simulator()
    # Write instructions into instruction memory.
    for i in range(len(assembler.instructions)):
        simulator.instrMemory.write(i, assembler.instructions[i])

    simulator.tick()

    pass
