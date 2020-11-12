from abc import ABCMeta, abstractmethod
from Simulator.Bus import AbstractBus


class AccessViolation(Exception):
    pass


class AbstractMemory(metaclass=ABCMeta):
    def __init__(self, name: str, totalSize: int):
        """
        Initialize simulator
        :param name:Name of the memory unit
        :param totalSize: The size of this memory (In Bytes)
        """
        self.name = name
        self.totalSize = totalSize

    @abstractmethod
    def read(self, location: int):
        pass

    @abstractmethod
    def write(self, location: int, value):
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
        if 0 <= location and location < self.totalSize:
            raise AccessViolation('Location %d causes access violation in memory %s' % (location, self.name))
        return self.memDict[location].value

    def write(self, location, value):
        if type(value) is int:
            # One byte
            if location < 0 or location >= self.totalSize:
                raise AccessViolation('Location %d causes access violation in memory %s' % (location, self.name))
            memEntry = Memory._MemEntry(value, location, location)
            self.memDict[location] = memEntry

        elif type(value) is float:
            # Two bytes
            if location < 0 or location + 1 >= self.totalSize:
                raise AccessViolation('Location %d causes access violation in memory %s' % (location, self.name))
            memEntry = Memory._MemEntry(value, location, location + 1)
            self.memDict[location] = memEntry
            self.memDict[location + 1] = memEntry
