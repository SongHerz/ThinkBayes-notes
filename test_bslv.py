#!/usr/bin/env python3
'''Test Bayes solver'''

from typing import Iterable
from bslv import Hypo, solve

def _test_solve(hypos: Iterable[Hypo], data: str,
                exps: Iterable[tuple[str, float]],
                delta: float = 0.0001):
    """
    Test Bayes solver with given hypotheses and data
    :param hypos: hypotheses
    :param exps: expected posteriors when given data happens.
    :param data: the max difference allowed between expected posteriors and calcated ones.
    """
    assert delta >= 0.0
    pmf = solve(hypos, data)
    d = pmf.GetDict()
    for h, exp_p in exps:
        cal_p = d[h]
        assert abs(cal_p - exp_p) < delta, 'Expected posterior varies too far away'


def test_cookie():
    """test with cookie data"""
    # cc is short for 'cookie count'
    bowl1_cc = 30 + 10
    bowl2_cc = 20 + 20
    hypos = [
        Hypo(name='Bowl1', dlls=[('vanilla', 30 / bowl1_cc), ('chocolate', 10 / bowl1_cc)]),
        Hypo(name='Bowl2', dlls=[('vanilla', 20 / bowl2_cc), ('chocolate', 20 / bowl2_cc)]),
    ]
    data = 'vanilla'
    exps = [('Bowl1', 0.6), ('Bowl2', 0.4)]
    _test_solve(hypos=hypos, data=data, exps=exps)


def test_monty_hall():
    """test with monty hall problem"""
    # Scenario:
    #   The audience have selected door A.
    #
    # Data: Monty opens door B, and no car behind door B.
    hypos = [
        # The car behind door A
        Hypo(name='HA', dlls=[('data', 1 / 2)]),
        # The car behind door B
        Hypo(name='HB', dlls=[('data', 0)]),
        # The car behind door C
        Hypo(name='HC', dlls=[('data', 1)])
    ]
    data = 'data'
    exps = [('HA', 0.33333), ('HB', 0), ('HC', 0.66666)]
    _test_solve(hypos=hypos, data=data, exps=exps)

def test_mm():
    """test with MM problem"""
    # # Scenario:
    # 2 bags of MM
    # - one from 1994
    # - the other from 1996
    dist_b4_1995 = {
        'brown': 30 / 100,
        'yellow': 20 / 100,
        'red': 20 / 100,
        'green': 10 / 100,
        'orange': 10 / 100,
        'tan': 10 / 100,
    }
    dist_since_1995 = {
        'blue': 24 / 100,
        'green': 20 / 100,
        'orange': 16 / 100,
        'yellow': 14 / 100,
        'red': 13 / 100,
        'brown': 13 / 100,
    }

    dist_1994 = dist_b4_1995
    dist_1996 = dist_since_1995

    def get_dist(tab: dict[str, float], color: str) -> float:
        return tab.get(color, 0.0)

    # Data: pick 2 MMs from each bag.
    #       - the 1st MM is yellow.
    #       - the 2nd MM is green
    hypos = [
        # the 1st bag 1994, the 2nd bag 1996
        Hypo(name='H1', dlls=[('data', get_dist(dist_1994, 'yellow') * get_dist(dist_1996, 'green'))]),
        # the 1st bag 1996, the 2nd bag 1994
        Hypo(name='H2', dlls=[('data', get_dist(dist_1996, 'yellow') * get_dist(dist_1994, 'green'))]),
    ]
    # Get P(H1|D)
    data = 'data'
    exps = [('H1', 200 / (200 + 70)), ('H2', 70 / (200 + 70))]
    _test_solve(hypos=hypos, data=data, exps=exps)