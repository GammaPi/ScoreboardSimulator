''' The FunctionUnit class is for the function units of the whole system.
    5 types: integer_alu / load_store / float_add_sub / float_mult / float_div
'''
class FunctionUnit:
    def __init__(self, type, cycles):
        self.type = type
        self.cycles = self.remaining_cycles = cycles
        self.busy = False
        self.operation = None # operation that use the functional unit
        self.fi = self.fj = self.fk = None
        self.qj = self.qk = None
        self.rj = self.rk = True

    '''Display the functional unit status'''
    def __str__(self):
        if not self.busy:
            return f"Func Unit (type {self.type} | busy {self.busy} | cycles {self.cycles} )"
        else:
            return f"Func Unit (type {self.type} | busy {self.busy} | cycles {self.cycles} \n" \
                f"operation {self.operation} | remaining cycles {self.remaining_cycles} \n" \
                f"fi {self.fi} | fj {self.fj} | fk {self.fk} \n" \
                f"qj {self.qj} | qk {self.qk} \n" \
                f"rj {self.rj} | rk {self.rk} )"

    '''Reset the FU after the instruction in use has completed'''
    def clear(self):
        self.operation = None
        self.remaining_cycles = self.cycles
        self.fi = self.fj = self.fk = None
        self.qj = self.qk = None
        self.rj = self.rk = True

    # todo
    '''Issue an instruction'''
    def issue(self, instruction, register_status):
        #if current FN is available, we can issue an instruction
        if self.busy or self.type != instruction.fu:
            return False

        #1.set Busy status
        self.busy = True

        #2.set the Operation type
        self.operation = instruction.op

        #3.set fi, fj, fk
        self.fi, self.fj, self.fk = instruction.dst, instruction.src1, instruction.src2 #todo I should change them to the true value if no RAW hazard

        #4.set qj, qk, rj, rk
        index = int(self.fj[1])
        if register_status[index]:
            self.qj = register_status[index]
            self.rj = False

        index = int(self.fk[1]) if self.fk else None #the 2nd operand can be None
        if index:
            self.qk = register_status[index]
            self.rk = False

        #5.set immediate value
        #todo


        pass

    # todo
    '''Current instruction gets the operand value'''
    def read_operands(self, instruction):
        pass

    # todo
    def execute(self):
        self.remaining_cycles -= 1