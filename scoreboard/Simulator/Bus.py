from Simulator.AbstractHW import AbstractBus


class BusBusyException(Exception):
    pass


# todo: Process binary rather than actual python data structure
class Bus(AbstractBus):
    def __init__(self, name, numBits):
        super().__init__(name, numBits)
        self.BUSY = False

    def read(self):
        if self.BUSY:
            raise BusBusyException()
        return self.value

    def write(self, value):
        if self.BUSY:
            raise BusBusyException()
        self.value = value
