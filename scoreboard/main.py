from decode import InstructionParse
from fu import FunctionUnit
from configure import Config

''' The control class is for the central control of the whole system.
'''
class Control:
    def __init__(self, file_path):
        self.pc = 0
        self.current_cycle = 1

        self.decoder = InstructionParse(file_path=file_path)
        self.init_function_unit()
        self.reg_status = [None for i in range(Config.register_status_size)]


    '''Simulate a clock cycle in the scoreboard'''
    def tick(self):
        print("------------------------------")
        print("Cycle", self.current_cycle)
        print(self.reg_status)

        current_instruction = self.decoder.instructions[self.pc] if self.has_remaining_instructions() else None

        for unit in self.function_units:
            if unit.lock == True:
                unit.lock = False

        for unit in self.function_units:
            if self.can_issue(current_instruction, unit):
                self.issue(current_instruction, unit)
                self.pc += 1
                # unit.lock = True
                print("==issue==", unit)
            elif self.can_read_operands(unit):
                self.read_operands(unit)
                # unit.lock = True
                print("==read==", unit)
            elif self.can_execute(unit):
                self.execute(unit)
                unit.lock = True
                print("==execute==", unit)

        for unit in self.function_units:
            # wb should be consider separately since we handle all the FUs in one cycle
            if not unit.lock and self.can_write_back(unit):
                self.write_back(unit)
                unit.lock = False
                print("==wb==", unit)

        self.current_cycle += 1
        print("~~~~~~~~~")

    def done(self):
        still_executing = False
        for unit in self.function_units:
            if unit.busy:
                still_executing = True
                break
        return not self.has_remaining_instructions() and not still_executing

    def has_remaining_instructions(self):
        return self.pc < len(self.decoder.instructions)

    def init_function_unit(self):
        self.function_units = [] #todo I just use a list to store all of the function units, maybe it's more efficient to use dict
        func_unit_conf = Config.functional_units

        for unit in func_unit_conf.keys():
            for i in range(func_unit_conf.get(unit).get("quantity")):
                self.function_units.append(FunctionUnit(unit, func_unit_conf.get(unit).get("clock_cycles")))


    def can_issue(self, instruction, function_unit):
        #based on lesson9 slide10 Solution for WAW: Detect hazard and stall issue of new instruction until other instruction completes
        return instruction != None and instruction.fu == function_unit.type and (not function_unit.busy) and (not self.reg_status[int(instruction.dst[1:])])


    def issue(self, instruction, function_unit):
        function_unit.issue(instruction, self.reg_status)
        function_unit.instruction_idx = self.pc
        self.reg_status[int(instruction.dst[1:])] = function_unit
        self.decoder.instructions[function_unit.instruction_idx].id1 = self.current_cycle
        # print(f"Instruction {instruction} ISSUE at cycle {self.current_cycle}")


    def can_read_operands(self, function_unit):
        return function_unit.busy and function_unit.rj and function_unit.rk

    def read_operands(self, function_unit):
        function_unit.read_operands()
        self.decoder.instructions[function_unit.instruction_idx].id2 = self.current_cycle

    def can_execute(self, function_unit):
        return function_unit.busy and not function_unit.rj and not function_unit.rk and function_unit.remaining_cycles > 0

    def execute(self, function_unit):
        function_unit.execute()
        if function_unit.remaining_cycles == 0:
            self.decoder.instructions[function_unit.instruction_idx].exe = self.current_cycle

    def can_write_back(self, function_unit):
        return function_unit.busy and function_unit.remaining_cycles == 0

    def write_back(self, function_unit):
        function_unit.write_back(self.function_units)
        self.decoder.instructions[function_unit.instruction_idx].wb = self.current_cycle
        self.reg_status[int(function_unit.fi[1:])] = None
        function_unit.clear()


if __name__ == '__main__':
    central_control = Control("test2.in")

    while not central_control.done():
        central_control.tick()
