""" The FunctionUnit class is for the function units of the whole system.
    5 types: integer_alu / load_store / float_add_sub / float_mult / float_div
"""
class FunctionUnit:
    def __init__(self, type, cycles):
        self.type = type
        self.cycles = self.remaining_cycles = cycles
        self.busy = False
        self.operation = None # operation that use the functional unit
        self.fi = self.fj = self.fk = None
        self.qj = self.qk = None
        self.rj = self.rk = True
        self.instruction_idx = -1 # record the index of the issued instruction
        self.lock = False # handle the wb collision

    '''Display the functional unit status'''
    def __str__(self):
        if not self.busy:
            return f"Func Unit (type {self.type} | busy {self.busy} | cycles {self.cycles} )"
        else:
            return f"Func Unit (type {self.type} | busy {self.busy} | cycles {self.cycles} \n" \
                f"operation {self.operation} | remaining cycles {self.remaining_cycles} \n" \
                f"fi {self.fi} | fj {self.fj} | fk {self.fk} \n" \
                f"qj {self.qj} | qk {self.qk} \n" \
                f"rj {self.rj} | rk {self.rk})"

    '''Reset the FU after the instruction in use has completed'''
    def clear(self):
        self.operation = None
        self.remaining_cycles = self.cycles
        self.fi = self.fj = self.fk = None
        self.qj = self.qk = None
        self.rj = self.rk = True
        self.instruction_idx = -1
        self.busy = False

    '''Issue an instruction'''
    def issue(self, instruction, register_status):
        # No need to check! since can_issue already checks for that
        # #if current FN is available, we can issue an instruction
        # if self.busy or self.type != instruction.fu:
        #     return False

        #1.set Busy status
        self.busy = True

        #2.set the Operation type
        self.operation = instruction.op

        #3.set fi, fj, fk
        # todo Implement the real calculation: I should change them to the true value when no RAW hazard
        self.fi, self.fj, self.fk = instruction.dst, instruction.src1, instruction.src2

        #4.set qj, qk, rj, rk
        index = int(self.fj[1:]) if self.fj else None #the 1nd operand can be None - load / store
        if index != None and register_status[index]:
            self.qj = register_status[index]
            self.rj = False

        index = int(self.fk[1:]) if self.fk else None #the 2nd operand can be None - ALUi
        if index != None and register_status[index]:
            self.qk = register_status[index]
            self.rk = False

        #5.set immediate value
        if self.type == "load_store": #then qk is immediate
            self.fj = instruction.immed
        elif instruction.immed: #then it's I type
            self.fk = instruction.immed


    '''Current instruction gets the operand value'''
    def read_operands(self):
        #reset the rj, rk for determining the execution stage
        self.rj = False
        self.rk = False


    def execute(self):
        # todo I don't deal with the real calculation
        self.remaining_cycles -= 1


    def write_back(self, function_units):
        for unit in function_units:
            if unit.qj == self:
                unit.rj = True
                unit.qj = None
            if unit.qk == self:
                unit.rk = True
                unit.qk = None
