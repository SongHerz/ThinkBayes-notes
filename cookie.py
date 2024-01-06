#!/usr/bin/env python3
"""Cookie problem probability calculator and demo"""

from typing import Iterable
from thinkbayes import Pmf


class Hypo:
    '''Hyposis and data likelihoods under this hyposis'''
    def __init__(self, name: str, dlls: Iterable[tuple[str, float]]):
        '''
        :param name: name of this hypothesis
        :param dlls: likelihoods of data in pairs of (data, likelihood)
        '''
        self.name = name
        # Normalize data distribution
        s = sum(ll for _, ll in dlls)
        self.dll = {}
        for data, ll in dlls:
            assert data not in self.dll, 'duplicate data not allowed'
            self.dll[data] = ll / s

    def all_data(self) -> Iterable[str]:
        ''':return: all data without its probabilites'''
        return self.dll.keys()

    def likelihood(self, data: str) -> float:
        ''':return: likelihood of given data of this hypothesis'''
        return self.dll[data]


def cookie_solver(hypos: Iterable[Hypo], data: str):
    '''Calculate all P(H|D) with given data'''
    # {hypo name: hypo}
    name2h = {h.name: h for h in hypos}

    ####################################
    # Calculate P(H) for all hypotheses
    ####################################
    pmf = Pmf()
    # Add hypotheses (assume all hypotheses have the same probability)
    for h in hypos:
        pmf.Set(h.name, 1)

    # This normalization is not necessary, because there is a final normalization.
    pmf.Normalize()

    ##########################################################
    # Calculate P(H)P(D|H) for all hypotheses with given data
    ##########################################################
    # Update posterior probabilities for all hypotheses with given data
    for hname in pmf.Values():
        h = name2h[hname]
        pmf.Mult(hname, h.likelihood(data))

    # P(H|D) = P(H)P(D|H)/P(D)
    # For given D, all P(H|D) calculations use the same P(D),
    # and it is not necessary to calculate P(D), just normalization is enough.
    pmf.Normalize()

    ########################
    # Final result printing
    ########################
    pmf.Print()


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
        Hypo(name='Bowl1', dlls=[('vanilla', 30), ('chocolate', 10)]),
        Hypo(name='Bowl2', dlls=[('vanilla', 20), ('chocolate', 20)]),
    ]
    cookie_solver(hypos, 'vanilla')

if __name__ == '__main__':
    main()
