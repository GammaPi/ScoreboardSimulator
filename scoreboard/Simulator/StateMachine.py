from abc import ABCMeta, abstractmethod

from Simulator.AbstractHW import AbstractStateMachine


class MultiCycleDFA(AbstractStateMachine):
    '''
    This is a multi-cycle Deterministic Finite State Machine.
    It supports state transitions after a certain amount of cycles
    '''

    def __init__(self, stateTransferList: list, initialState):
        """
        :param stateList: List of states and their transition cycles. eg: [(0,1,3),(1,0,4)] 0=>1 3 cycles; 1=>0 4 cycles. State can be abitrary pyobject. But have to have unique hash.
        """
        # Convert State Transfer List to Adjacent list.
        self.adjTable = {}
        self.curState = initialState
        self.counter = 0

        for stateTransItem in stateTransferList:
            fromState, toState, transferCycle = stateTransItem
            assert fromState not in self.adjTable  # This is a DFA
            self.adjTable[fromState] = (toState, transferCycle)

        assert self.curState in self.adjTable

    def next(self):
        self.counter += 1
        if self.curState in self.adjTable:
            toState, transferCycle = self.adjTable[self.curState]
        else:
            self.curState=None
            return None
        if self.counter == transferCycle:
            self.counter = 0
            self.curState = toState
        return self.curState

    def peek(self):
        toState, transferCycle = self.adjTable[self.curState]
        return toState

    @property
    def curState(self):
        return self._curState

    @curState.setter
    def curState(self, newState, curCounter=0):
        self.counter = curCounter
        self._curState = newState
