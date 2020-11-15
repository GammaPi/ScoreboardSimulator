from Simulator.AbstractHW import AbstractMemory, Instruction


class AccessViolation(Exception):
    pass


class DictMemory(AbstractMemory):
    class _MemEntry:
        def __init__(self, value, start, end):
            self.value = value
            self.start = start
            self.end = end

    def __init__(self, name, totalSize: int):
        super().__init__(name, totalSize)
        self.memDict = {}

    def read(self, location):
        if location < 0 or location >= self.totalSize:
            raise AccessViolation('Location %d causes access violation in memory %s' % (location, self.name))
        if location not in self.memDict:
            return 0
        else:
            return self.memDict[location].value

    def write(self, location, value):
        if type(value) is int:
            # One word
            if location < 0 or location >= self.totalSize:
                raise AccessViolation('Location %d causes access violation in memory %s' % (location, self.name))
            memEntry = DictMemory._MemEntry(value, location, location)
            self.memDict[location] = memEntry

        elif type(value) is float:
            # Two words
            if location < 0 or location + 1 >= self.totalSize:
                raise AccessViolation('Location %d causes access violation in memory %s' % (location, self.name))
            memEntry = DictMemory._MemEntry(value, location, location + 1)
            self.memDict[location] = memEntry
            self.memDict[location + 1] = memEntry
        if type(value) is Instruction:
            #todo: Translate instruction into bytecode
            # One word
            if location < 0 or location + 1 >= self.totalSize:
                raise AccessViolation('Location %d causes access violation in memory %s' % (location, self.name))
            memEntry = DictMemory._MemEntry(value, location, location)
            self.memDict[location] = memEntry