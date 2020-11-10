import re
from Simulator.Config import Config


class Instruction:
    '''
    A representation of instruction that can be executed by the simulator
    '''

    def __init__(self, op, fu, dst, src1, src2, immed):
        self.op = op
        self.fu = fu
        self.dst = dst
        self.src1 = src1
        self.src2 = src2
        self.immed = immed  # immediate number
        self.id1 = self.id2 = self.exe = self.wb = -1  # for recording the cycle number

    def __str__(self):
        # todo: Output the same binary code as WinMIPS64
        return f"Instruction (op {self.op} | fu {self.fu} | dst {self.dst} | src1 {self.src1} | src2 {self.src2} | immed {self.immed})"


class Assembler:
    def __init__(self, file_path: str):
        self.instruction_file = file_path
        self.instructions = []

        self.parse_instruction_file()

    def parse_instruction_file(self):
        """
        Parse instruction file line by line and convert it to Assembler::Instruction format
        """
        with open(self.instruction_file, 'r') as f:
            instruction_lines = [line.strip() for line in f]
        for instruction in instruction_lines:
            self.parse_instruction_line(instruction)

    def parse_instruction_line(self, line: str):
        """
        Parse a single instruction
        :param line: Instruction text
        """
        symbols = list(filter(None, re.split(',| ', line)))  # Split instruction so that we can process

        # todo: Simulate MAR IR Databus Instruction Bus

        opCode = symbols[0]  # Find instruction by it's op code
        inst_properties = Config.instruction_list[opCode]
        current_inst = None

        # Convert instruction to Assembler::Instruction format
        if inst_properties["instruction_type"] == "R":
            current_inst = Instruction(symbols[0], inst_properties["functional_unit"], symbols[1], symbols[2],
                                       symbols[3], None)
        elif inst_properties["instruction_type"] == "I":
            if inst_properties["functional_unit"] == "integer_alu":
                current_inst = Instruction(symbols[0], inst_properties["functional_unit"], symbols[1], symbols[2], None,
                                           symbols[3])
            elif inst_properties["functional_unit"] == "load_store":
                # todo maybe I should change "$2" to "f2" to make it easy for post-processing?
                current_inst = Instruction(symbols[0], inst_properties["functional_unit"], symbols[1], None,
                                           re.search('(.*)\((.*)\)', symbols[2]).group(2),
                                           re.search('(.*)\((.*)\)', symbols[2]).group(1))
        else:
            # todo J type
            pass

        if current_inst:
            self.instructions.append(current_inst)
        else:
            # todo raise error
            pass
