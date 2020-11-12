from abc import ABCMeta, abstractmethod


class BusBusyException(Exception):
    pass


class AbstractBus(metaclass=ABCMeta):
    def __init__(self, name, numBits):
        """
        :param name: Bus name
        :param numBits: Bus Width
        """
        self.name = name
        self.numBits = numBits
        self.BUSY = False

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def write(self, value):
        pass


# todo: Process binary rather than actual python data structure
class Bus(AbstractBus):
    def __init__(self, name, numBits):
        super().__init__(name, numBits)

    def read(self):
        if self.BUSY:
            raise BusBusyException()
        return self.value

    def write(self, value):
        self.BUSY = True
        self.value = value
        self.BUSY = False
