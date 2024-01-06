#!/usr/bin/env python3
"""Cookie problem probability calculator and demo"""

from thinkbayes import Pmf


class Cookie(Pmf):
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
        for h in self.Values():
            like = self._likelihood(data, h)
            self.Mult(h, like)

        self.Normalize() 



bowls = ['Bowl1', 'Bowl2']
cookie = Cookie(bowls)
cookie.update('vanilla')
cookie.Print()