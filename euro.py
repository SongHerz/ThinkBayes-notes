#!/usr/bin/env python3
"""
Calculate euro coin uniformness
"""

from typing import Callable, Any

from thinkbayes import Suite, Percentile, CredibleInterval
import thinkplot


class Euro(Suite):
    """
    Calcuate probability of coin head side up probabilities.
    """
    def Likelihood(self, data, hypo):
        x = hypo

        if data == 'H':
            return x / 100
        else:
            return 1 - x / 100

class EuroFast(Suite):
    """
    Calcuate probability of coin head side up probabilities.
    """
    def Likelihood(self, data, hypo):
        """
        data is in (heads count, tails count)
        """
        x = hypo / 100.0
        heads, tails = data
        return (x ** heads) * ((1 - x) ** tails)


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


def update_euro(euro: Euro):
    """Update Euro instances with data"""
    dataset = 'H' * 140 + 'T' * 110
    euro.UpdateSet(dataset)

def update_eurofast(eurofast: EuroFast):
    """Update EuroFast instances with data"""
    # heads: 140, tails: 100
    data = (140, 100)
    eurofast.Update(data)


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


def cmp_uni_tri(constr: Callable[[], Euro], update: Callable[[Suite], None]):
    '''Compare uniform and triangle prior and their posterior'''
    uni_euro = constr()
    uni_euro.name = 'uniform'
    tri_euro = constr()
    tri_euro.name = 'triangle'
    init_with_uniform_prior(uni_euro)
    init_with_triangle_prior(tri_euro)

    plot_suites([uni_euro, tri_euro])
    update(uni_euro)
    update(tri_euro)

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


cmp_uni_tri(Euro, update_euro)

print()
print('# !!!! WARNING !!!!')
print('# with EuroFast, number becomes too small,')
print('# and the final result are not the same as the final result of Euro')
cmp_uni_tri(EuroFast, update_eurofast)