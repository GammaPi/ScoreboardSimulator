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


    '''Simulate a clock cycle in the scoreboard'''
    def tick(self):
        print("------------------------------")
        print("Cycle", self.current_cycle)

        current_instruction = self.decoder.instructions[self.pc] if self.has_remaining_instructions() else None

        print(current_instruction)

        self.pc += 1
        self.current_cycle += 1

    def done(self):
        return not self.has_remaining_instructions()

    def has_remaining_instructions(self):
        return self.pc < len(self.decoder.instructions)

    def init_function_unit(self):
        self.function_units = [] #todo I just use a list to store all of the function units, maybe it's more efficient to use dict
        func_unit_conf = Config.functional_units

        for unit in func_unit_conf.keys():
            for i in range(func_unit_conf.get(unit).get("quantity")):
                self.function_units.append(FunctionUnit(unit, func_unit_conf.get(unit).get("clock_cycles")))
        print(self.function_units)

if __name__ == '__main__':
    central_control = Control("test.in")

    while not central_control.done():
        central_control.tick()
