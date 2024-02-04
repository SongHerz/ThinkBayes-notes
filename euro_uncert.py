#!/usr/bin/env python3
"""
Exercise 4-1

An uncertainty `y` introduced.
Head may be reported as tail with probability `y`.
Tail may be reported as head with probability `y`.
"""

from typing import Callable

from thinkbayes import Suite, Percentile, CredibleInterval
import thinkplot


class EuroMeasureUncert(Suite):
    """
    Euro coin problem with measurement uncertainty
    """
    def __init__(self, y: float):
        super().__init__()
        assert 0.0 <= y <= 1.0
        self._y = y

    def Likelihood(self, data, hypo):
        x = hypo

        head_lh = None # head likelihood
        tail_lh = None # tail likelihood

        if data == 'H':
            ideal_head_lh = x / 100
            head_lh = ideal_head_lh * (1 - self._y)
            tail_lh = ideal_head_lh * self._y
        else:
            ideal_tail_lh = 1 - x / 100
            tail_lh = ideal_tail_lh * (1 - self._y)
            head_lh = ideal_tail_lh * self._y

        assert head_lh is not None
        assert tail_lh is not None

        return head_lh, tail_lh

    def Update(self, data):
        for hypo in self.Values():
            head_like, tail_like = self.Likelihood(data, hypo)
            self.Mult(hypo, head_like)
            self.Mult(hypo, tail_like)

        return self.Normalize()

    def UpdateSet(self, dataset):
        raise NotImplementedError("Must IMPLEMENT")


def init_with_uniform_prior(suite: Suite):
    """Init suite with uniform prior"""
    for x in range(0, 101):
        suite.Set(x, 1)

    suite.Normalize()


def init_with_triangle_prior(suite: Suite):
    """Init suite with triangle prior"""
    for x in range(0, 51):
        suite.Set(x, x)

    for x in range(51, 101):
        suite.Set(x, 100 - x)

    suite.Normalize()


def update(euro: EuroMeasureUncert, heads: int, tails: int):
    """Update Euro instances with data"""
    dataset = 'H' * heads + 'T' * tails
    for data in dataset:
        euro.Update(data)


def summary_suite(suite: Suite):
    """Print summaries"""
    print('Maximum Likelihood:', suite.MaximumLikelihood())
    print('Mean:', suite.Mean())
    print('Median:', Percentile(suite, 50))
    print('Credible Interval:', CredibleInterval(suite, 90))
    print('Prob 50:', suite.Prob(50))


def plot_suites(suites: list[Suite]):
    """Plot suites in one figure"""
    thinkplot.PrePlot(num=len(suites))
    for s in suites:
        thinkplot.Pmf(s)

    thinkplot.Show(xlabel='x', ylabel='Probability')


def cmp_uni_tri(constr: Callable[[], EuroMeasureUncert], update_func: Callable[[Suite], None]):
    '''Compare uniform and triangle prior and their posterior'''
    uni_euro = constr()
    uni_euro.name = 'uniform'
    tri_euro = constr()
    tri_euro.name = 'triangle'
    init_with_uniform_prior(uni_euro)
    init_with_triangle_prior(tri_euro)

    plot_suites([uni_euro, tri_euro])
    update_func(uni_euro)
    update_func(tri_euro)

    print()
    print("##############################")
    print(" Posterior from Uniform Prior")
    print("##############################")
    summary_suite(uni_euro)

    print()
    print("###############################")
    print(" Posterior from Triangle Prior")
    print("###############################")
    summary_suite(tri_euro)

    plot_suites([uni_euro, tri_euro])


HEADS = 140
TAILS = 110

cmp_uni_tri(lambda: EuroMeasureUncert(0.00001), lambda e: update(e, HEADS, TAILS))
cmp_uni_tri(lambda: EuroMeasureUncert(0.5), lambda e: update(e, HEADS, TAILS))
