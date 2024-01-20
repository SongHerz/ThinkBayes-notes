#!/usr/bin/env python3
"""
Train number estimation
"""

from typing import Iterable, Sequence
from thinkbayes import Suite
import thinkplot


class Train(Suite):
    """
    Even distribution hypothesis .
    """

    def Likelihood(self, data: int, hypo: int) -> float:
        if hypo < data:
            return 0.0

        return 1.0 / hypo


def estimate(
    hypo_dists: Sequence[tuple[int, float]],
    obs: Iterable[int],
    verbose: False,
    plot: False,
) -> float:
    """Estimate total train number based on observations
    :param hypos: hypotheses in sequence of (number of train, probability)
    :param obs: observations of train ids
    :param verbose: show probabilities of each possible train number in txt
    :param plot: plot updated hypotheses distribution
    """
    suite = Train()
    for h, p in hypo_dists:
        suite.Set(h, p)

    suite.Normalize()

    # Estimation sequences based on given observations
    ests = []
    for ob in obs:
        suite.Update(ob)
        ests.append(suite.Mean())

    if verbose:
        print()
        print("Detailed distribution:")
        suite.Print()

    if plot:
        thinkplot.PrePlot(1)
        thinkplot.Pmf(suite)
        thinkplot.Show(xlabel="Number of trains", ylabel="Probability")

    return ests


def get_even_hypo_dists(limit: int) -> list[tuple[int, float]]:
    """Get even distributed hypotheses"""
    assert limit >= 1
    hypo_dists = [(h, 1) for h in range(1, limit + 1)]
    mu = sum(v for _, v in hypo_dists)
    return [(h, v / mu) for h, v in hypo_dists]


def get_power_law_hypo_dists(limit: int, alpha: float = 1.0) -> list[tuple[int, float]]:
    """Get power-law distributed hypotheses"""
    assert limit >= 1
    hypo_dists = [(h, h ** (-alpha)) for h in range(1, limit + 1)]
    mu = sum(v for _, v in hypo_dists)
    return [(h, v / mu) for h, v in hypo_dists]


LIMIT = 1000
obs = [60]
ests = estimate(hypo_dists=get_even_hypo_dists(LIMIT), obs=obs, verbose=True, plot=True)
print(f'Limit: {LIMIT}, observations: {obs}, estimation: {ests[-1]}')


print()
print()
print('##############################')
print(' Even Distribution Hypotheses')
print('##############################')
obs = [60, 30, 90]
for limit in [500, 1000, 2000]:
    ests = estimate(hypo_dists=get_even_hypo_dists(limit), obs=obs, verbose=False, plot=False)
    print(f'Limit: {limit}, observations: {obs}, estimations: {ests}, final estimation: {ests[-1]}')


print()
print()
print('###################################')
print(' Power-law Distribution Hypotheses')
print('###################################')
obs = [60, 30, 90]
for limit in [500, 1000, 2000]:
    ests = estimate(hypo_dists=get_power_law_hypo_dists(limit), obs=obs, verbose=False, plot=False)
    print(f'Limit: {limit}, observations: {obs}, estimations: {ests}, final estimation: {ests[-1]}')
