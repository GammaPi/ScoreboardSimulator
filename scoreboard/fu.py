class FunctionUnit:
    def __init__(self, type, cycles):
        self.type = type
        self.cycles = self.remaining_cycles = cycles
        self.busy = False
        self.operation = None # operation that use the functional unit
        self.fi = self.fj = self.fk = None
        self.qj = self.qk = None
        self.rj = self.rk = True

    # todo
    '''Display the functional unit status'''
    def __str__(self):
        pass

    # todo
    '''Reset the FU after the instruction in use has completed'''
    def clear(self):
        pass

    # todo
    '''Issue an instruction'''
    def issue(self, instruction, register_status):
        #if current FN is available, we can issue an instruction

        #1.set Busy status

        #2.set the Operation type

        #3.set fi, fj, fk

        #4.set qj, qk

        #5.set rj, rk

        pass

    # todo
    '''Current instruction gets the operand value'''
    def read_operands(self):
        pass


    def execute(self):
        self.remaining_cycles -= 1