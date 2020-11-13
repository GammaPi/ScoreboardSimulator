from Simulator.StateMachine import MultiCycleDFA
from enum import Enum


class State(Enum):
    A = 1
    B = 2
    C = 3
    D = 4


def testMultiCycleDFA():
    mdfa = MultiCycleDFA([(State.A, State.B, 2),
                          (State.B, State.C, 3),
                          (State.C, State.D, 4),
                          (State.D, State.A, 1),
                          ], State.A)
    assert (mdfa.curState == State.A)
    # A->B
    assert (mdfa.next() == State.A and mdfa.curState == State.A)
    assert (mdfa.next() == State.B and mdfa.curState == State.B)
    # B->C
    assert (mdfa.next() == State.B and mdfa.curState == State.B)
    assert (mdfa.next() == State.B and mdfa.curState == State.B)
    assert (mdfa.next() == State.C and mdfa.curState == State.C)
    # C->D
    assert (mdfa.next() == State.C and mdfa.curState == State.C)
    assert (mdfa.next() == State.C and mdfa.curState == State.C)
    assert (mdfa.next() == State.C and mdfa.curState == State.C)
    assert (mdfa.next() == State.D and mdfa.curState == State.D)
    # D->A
    assert (mdfa.next() == State.A and mdfa.curState == State.A)

    mdfa.curState = State.D
    # D->A
    assert (mdfa.next() == State.A and mdfa.curState == State.A)
    # A->B
    assert (mdfa.next() == State.A and mdfa.curState == State.A)
    assert (mdfa.next() == State.B and mdfa.curState == State.B)
