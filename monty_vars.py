#!/usr/bin/env python3
"""
Solve Monty Hall Problem with various methods


Scenario:
  The audience have selected door A.

Data: Monty opens door B, and no car behind door B.
"""

from typing import Any
from thinkbayes import Suite
import bslv

def bslv_solve():
    """solve Monty with bslv"""
    hypos = [
        # The car behind door A
        bslv.Hypo(name='HA', dlls=[('data', 1 / 2)]),
        # The car behind door B
        bslv.Hypo(name='HB', dlls=[('data', 0)]),
        # The car behind door C
        bslv.Hypo(name='HC', dlls=[('data', 1)])
    ]
    data = 'data'
    pmf = bslv.solve(hypos, data)
    pmf.Print()


class Monty(Suite):
    '''Monty Hall Solver'''
    def __init__(self):
        super().__init__(['HA', 'HB', 'HC'])

    def Likelihood(self, data: Any, hypo: Any) -> float:
        assert data == 'data'
        if hypo == 'HA':
            return 1 / 2
        elif hypo == 'HB':
            return 0
        else:
            assert hypo == 'HC'
            return 1


def suite_solve():
    """Solve Monty Hall"""
    s = Monty()
    s.Update('data')
    s.Print()

print()
print('Solve with bslv:')
bslv_solve()

print()
print('Solve with Suite:')
suite_solve()
