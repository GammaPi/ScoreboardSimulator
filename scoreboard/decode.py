import re
from configure import Config

class Instruction:
    def __init__(self, op, fu, dst, src1, src2, immed):
        self.op = op
        self.fu = fu
        self.dst = dst
        self.src1 = src1
        self.src2 = src2
        self.immed = immed # immediate number


    # todo
    def __str__(self):
        pass



class InstructionParse:
    def __init__(self, file_path):
        self.instruction_file = file_path
        self.instructions = []

    def parse_instruction_file(self):
        with open(self.instruction_file, 'r') as f:
            instruction_lines = [line.strip() for line in f]
        for instruction in instruction_lines:
            self.parse_instruction_line(instruction)


    def parse_instruction_line(self, line):
        symbols = list(filter(None, re.split(',| ', line))) # remove empty symbols

        key = symbols[0]      # instruction type
        inst_properties = Config.instruction_list[key]
        current_inst = None

        if inst_properties["instruction_type"] == "R":
            current_inst = Instruction(symbols[0], inst_properties["functional_unit"], symbols[1], symbols[2], symbols[3], None)
        elif inst_properties["instruction_type"] == "I":
            if inst_properties["functional_unit"] == "integer_alu":
                current_inst = Instruction(symbols[0], inst_properties["functional_unit"], symbols[1], symbols[2], None, symbols[3])
            elif inst_properties["functional_unit"] == "load_store":
                #todo maybe I should change "$2" to "f2" to make it easy for post-processing?
                current_inst = Instruction(symbols[0], inst_properties["functional_unit"], symbols[1], re.search('(.*)\((.*)\)', symbols[2]).group(2), None, re.search('(.*)\((.*)\)', symbols[2]).group(1))
        else:
            # J type
            pass

        if current_inst:
            self.instructions.append(current_inst)
        else:
            #todo raise error
            pass