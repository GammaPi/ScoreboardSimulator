import re
import Simulator.Config as Config
from Simulator.AbstractHW import Instruction
from Simulator.Registers import IntRegister, FloatRegister


class Assembler:
    def __init__(self, instrFilePath: str):
        self.instrFilePath = instrFilePath
        self.instructions = []

        self.parseInstrFile()

    def parseInstrFile(self):
        """
        Parse instruction file line by line and convert it to Assembler::Instruction format
        """
        with open(self.instrFilePath, 'r') as f:
            instrLines = [line.strip() for line in f]
        for instruction in instrLines:
            self.parseInstrLine(instruction)

    def parseInstrLine(self, line: str):
        """
        Parse a single instruction
        :param line: Instruction text
        """
        symbols = list(filter(None, re.split(',|\s|\(|\)', line)))  # Split instruction so that we can process

        opName = symbols[0]  # Find instruction type by it's op Name
        curInstrType: Config.InstrType = Config.InstrType[opName]

        # todo: implement more robust grammar checker
        curInstr: Instruction = None
        if curInstrType == Config.InstrType.LW:
            # LW Rdst,imm(Rsrc1)
            curInstr = Instruction(instrType=curInstrType, dstReg=IntRegister(symbols[1]),
                                   src1Reg=IntRegister(symbols[3]),
                                   src2Reg=None, immed=symbols[2])
        elif curInstrType == Config.InstrType.SW:
            # SW Rsrc1,imm(Rdst)
            curInstr = Instruction(instrType=curInstrType, dstReg=IntRegister(symbols[3]),
                                   src1Reg=IntRegister(symbols[1]),
                                   src2Reg=None, immed=symbols[2])
        elif curInstrType == Config.InstrType.L_D:
            # L.D Fdst,imm(Rsrc1)
            curInstr = Instruction(instrType=curInstrType, dstReg=FloatRegister(symbols[1]),
                                   src1Reg=IntRegister(symbols[3]),
                                   src2Reg=None, immed=symbols[2])
        elif curInstrType == Config.InstrType.S_D:
            # S.D Fsrc1,imm(Rdst)
            curInstr = Instruction(instrType=curInstrType, dstReg=IntRegister(symbols[3]),
                                   src1Reg=FloatRegister(symbols[1]),
                                   src2Reg=None, immed=symbols[2])
        elif curInstrType in [Config.InstrType.DADD, Config.InstrType.DSUB, Config.InstrType.DMUL,
                              Config.InstrType.DDIV]:
            # DADD Rdst,Rsrc1,Rsrc2
            curInstr = Instruction(instrType=curInstrType, dstReg=IntRegister(symbols[1]),
                                   src1Reg=IntRegister(symbols[2]),
                                   src2Reg=IntRegister(symbols[3]), immed=None)
        elif curInstrType in [Config.InstrType.DADDI, Config.InstrType.DSUBI]:
            # DADDI Rsrc1,Rsrc2,imm
            curInstr = Instruction(instrType=curInstrType, dstReg=IntRegister(symbols[1]),
                                   src1Reg=IntRegister(symbols[2]),
                                   src2Reg=None, immed=symbols[3])
        elif curInstrType in [Config.InstrType.BEQ, Config.InstrType.BNE]:
            # BEQ Rsrc1,Rsrc2,imm
            curInstr = Instruction(instrType=curInstrType, dstReg=None,
                                   src1Reg=IntRegister(symbols[1]),
                                   src2Reg=IntRegister(symbols[2]), immed=symbols[3])
        elif curInstrType in [Config.InstrType.BEQZ, Config.InstrType.BNEZ]:
            # BEQZ Rsrc1,loop
            curInstr = Instruction(instrType=curInstrType, dstReg=None,
                                   src1Reg=IntRegister(symbols[1]),
                                   src2Reg=None, immed=symbols[2])
        elif curInstrType in [Config.InstrType.ADD_D, Config.InstrType.SUB_D, Config.InstrType.MUL_D,
                              Config.InstrType.DIV_D]:
            # ADD.D Fdst,Fsrc1,Fsrc2
            curInstr = Instruction(instrType=curInstrType, dstReg=FloatRegister(symbols[1]),
                                   src1Reg=FloatRegister(symbols[2]),
                                   src2Reg=FloatRegister(symbols[3]), immed=None)
        elif curInstrType == Config.InstrType.J:
            # J immed
            curInstr = Instruction(instrType=curInstrType, dstReg=None,
                                   src1Reg=None,
                                   src2Reg=None, immed=symbols[1])
        else:
            assert False

        if curInstr:
            self.instructions.append(curInstr)
        else:
            assert False
        return curInstr