#!/usr/bin/env python3
"""Bayes solver"""

from typing import Iterable
from thinkbayes import Pmf


class Hypo:
    '''Hyposis and data likelihoods under this hyposis'''

    @staticmethod
    def _normalize_dlls(dlls: Iterable[tuple[str, float]]) -> dict[str, float]:
        '''
        :return: normalized data distribution
        '''
        s = sum(ll for _, ll in dlls)
        dll = {}
        for data, ll in dlls:
            assert data not in dll, 'duplicate data not allowed'
            dll[data] = ll / s
        return dll

    def __init__(self, name: str, dlls: Iterable[tuple[str, float]]):
        '''
        :param name: name of this hypothesis
        :param dlls: likelihoods of data in pairs of (data, likelihood)
        '''
        self.name = name
        self.dll = self._normalize_dlls(dlls)

    def all_data(self) -> Iterable[str]:
        ''':return: all data without its probabilites'''
        return self.dll.keys()

    def likelihood(self, data: str) -> float:
        ''':return: likelihood of given data of this hypothesis'''
        return self.dll[data]


def solve(hypos: Iterable[Hypo], data: str) -> Pmf:
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

    return pmf