#!/usr/bin/env python3
"""
Calculate euro coin uniformness
"""

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


def init_with_uniform_prior(suite: Suite):
    for x in range(0, 101):
        suite.Set(x, 1)

    suite.Normalize()


def init_with_triangle_prior(suite: Suite):
    for x in range(0, 51):
        suite.Set(x, x)

    for x in range(51, 101):
        suite.Set(x, 100 - x)

    suite.Normalize()


def update_suite(suite: Suite):
    dataset = 'H' * 140 + 'T' * 110
    suite.UpdateSet(dataset)


def summary_suite(suite: Suite):
    print('Maximum Likelihood:', suite.MaximumLikelihood())
    print('Mean:', suite.Mean())
    print('Median:', Percentile(suite, 50))
    print('Credible Interval:', CredibleInterval(suite, 90))
    print('Prob 50:', suite.Prob(50))


def plot_suites(suites: list[Suite]):
    thinkplot.PrePlot(num=len(suites))
    for s in suites:
        thinkplot.Pmf(s)

    thinkplot.Show(xlabel='x', ylabel='Probability')


uni_suite = Euro()
uni_suite.name = 'uniform'
tri_suite = Euro()
tri_suite.name = 'triangle'
init_with_uniform_prior(uni_suite)
init_with_triangle_prior(tri_suite)

plot_suites([uni_suite, tri_suite])
update_suite(uni_suite)
update_suite(tri_suite)

print()
print("##############################")
print(" Posterior from Uniform Prior")
print("##############################")
summary_suite(uni_suite)

print()
print("###############################")
print(" Posterior from Triangle Prior")
print("###############################")
summary_suite(tri_suite)

plot_suites([uni_suite, tri_suite])
