#!/usr/bin/env python3
"""Cookie problem probability calculator and demo"""

import bslv
from thinkbayes import Pmf

class CookieNaive(Pmf):
    """Cookie Probability Solver"""

    def __init__(self, hypos: list[str]):
        super().__init__()
        for h in hypos:
            self.Set(h, 1)

        self.Normalize()

    mixes = {
        'Bowl1': {'vanilla': 0.75, 'chocolate': 0.25},
        'Bowl2': {'vanilla': 0.5, 'chocolate': 0.5}
    }

    def _likelihood(self, data: str, hypo: str) -> float:
        mix = self.mixes[hypo]
        like = mix[data]
        return like

    def update(self, data):
        '''Update posterier probabilies (P(H|D)) with given data'''
        for h in self.Values():
            like = self._likelihood(data, h)
            self.Mult(h, like)

        self.Normalize()


def main():
    '''Try implementations'''
    ########################
    # Naive Implementation #
    ########################
    print()
    print('## Naive Implementation')
    print()
    bowls = ['Bowl1', 'Bowl2']
    cookie_naive = CookieNaive(bowls)
    cookie_naive.update('vanilla')
    cookie_naive.Print()

    #########################
    # Better Implementation #
    #########################
    print()
    print('## Better Implementation')
    print()
    hypos = [
        bslv.Hypo(name='Bowl1', dlls=[('vanilla', 30), ('chocolate', 10)]),
        bslv.Hypo(name='Bowl2', dlls=[('vanilla', 20), ('chocolate', 20)]),
    ]
    pmf = bslv.solve(hypos, 'vanilla')
    pmf.Print()

if __name__ == '__main__':
    main()
