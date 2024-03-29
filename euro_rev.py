#!/usr/bin/env python3
"""
Exercise 4-1

An reversibility `y` introduced.
Head may be reported as tail with probability `y`.
Tail may be reported as head with probability `y`.
"""

from typing import Callable

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


class EuroMeasureRev(Suite):
    """
    Euro coin problem with measurement reversibility
    """
    def __init__(self, rev: float):
        super().__init__()
        assert 0.0 <= rev <= 1.0
        self._rev = rev

    @property
    def reversibility(self) -> float:
        """Return measurement reversibility"""
        return self._rev

    def Likelihood(self, data, hypo):
        """
        Denote:
        - hypo H: Head up with given hypothesis
        - hypo T: Tail up with given hypothesis

        Because of reversibility, there are 4 scenarios:
        - hypo H -> measured H: denote h2h
        - hypo H -> measured T: denote h2t
        - hypo T -> measured T: denote t2t
        - hypo T -> measured H: denote t2h

        Given hypothesis head up probability is x%
        hypo H likelihood: x / 100
        hypo T likelihood: 1 - hypo H likelihood = 1 - x / 100

        measured H likelihood = h2h likelihood + t2h likelihood
        measured T likelihood = t2t likelihood + h2t likelihood

        h2h likelihood = hypo H likelihood * (1 - reversibility)
        h2t likelihood = hypo H likelihood * reversibility

        t2t likelihood = hypo T likelihood * (1 - reversibility)
        t2h likelihood = hypo T likelihood * reversibility

        ==>
        measured H likelihood
        = h2h likelihood + t2h likelihood
        = hypo H likelihood * (1 - reversibility) + hypo T likelihood * reversibility
        = (x / 100) * (1 - reversibility) + (1 - x / 100) * reversibility

        measured T likelihood
        = t2t likelihood + h2t likelihood
        = hypo T likelihood * (1 - reversibility) + hypo H likelihood * reversibility
        = (1 - x / 100) * (1 - reversibility) + (x / 100) * reversibility

        And it is easy to verify that, when reversibility is zero.
        measured H likelihood = x / 100 = hypo H likelihood
        measured T likelihood = 1 - x / 100 = hypo T likelihood
        """
        x = hypo

        hypo_H_like = x / 100
        hypo_T_like = 1 - x / 100

        if data == 'H':
            return hypo_H_like * (1 - self._rev) + hypo_T_like * self._rev
        else:
            return hypo_T_like * (1 - self._rev) + hypo_H_like * self._rev


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


def update(euro: EuroMeasureRev | Euro, heads: int, tails: int):
    """Update Euro instances with data"""
    dataset = 'H' * heads + 'T' * tails
    euro.UpdateSet(dataset)


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


def cmp_uni_tri(constrs: list[Callable[[], EuroMeasureRev]],
                update_func: Callable[[Suite], None]):
    '''Compare uniform and triangle prior and their posterior'''
    euros = []
    for constr in constrs:
        uni_euro = constr()
        uni_euro.name = f'uniform, rev: {uni_euro.reversibility:.2f}'
        tri_euro = constr()
        tri_euro.name = f'triangle, rev: {tri_euro.reversibility:.2f}'
        init_with_uniform_prior(uni_euro)
        init_with_triangle_prior(tri_euro)
        euros.append(uni_euro)
        euros.append(tri_euro)

    plot_suites(euros)
    for euro in euros:
        update_func(euro)

    for euro in euros:
        print()
        print("##############################")
        print(f" Posterior from {euro.name}")
        print("##############################")
        summary_suite(euro)

    plot_suites(euros)


if __name__ == '__main__':
    HEADS = 140
    TAILS = 110

    ###############################################
    # Compare EuroMeasureRev(0) and plain Euro.
    # They must be equal.
    ###############################################
    euro = Euro()
    euro_rev_0 = EuroMeasureRev(0)
    init_with_uniform_prior(euro)
    init_with_uniform_prior(euro_rev_0)

    # Values must be the same after initialization
    assert euro.d.keys() == euro_rev_0.d.keys()
    for k, v in euro.d.items():
        v2 = euro_rev_0.d[k]
        assert v == v2

    update(euro, HEADS, TAILS)
    update(euro_rev_0, HEADS, TAILS)

    # Values must be the same after updating
    assert euro.d.keys() == euro_rev_0.d.keys()
    for k, v in euro.d.items():
        v2 = euro_rev_0.d[k]
        assert abs(v - v2) < 0.0001


    #############################
    # Plot and print statistics #
    #############################
    cmp_uni_tri(
        [lambda: EuroMeasureRev(0),
         lambda: EuroMeasureRev(0.1),
         lambda: EuroMeasureRev(0.25),
        ],
        lambda e: update(e, HEADS, TAILS),
    )
