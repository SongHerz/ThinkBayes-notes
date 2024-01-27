#!/usr/bin/env python3
"""
Train number estimation
"""

from typing import Iterable, Sequence
from thinkbayes import Suite, Percentile
import thinkplot


class Train(Suite):
    """
    Even distribution hypothesis .
    """

    def Likelihood(self, data: int, hypo: int) -> float:
        if hypo < data:
            return 0.0

        return 1.0 / hypo


def estimate(hypo_dists: Sequence[tuple[int, float]],
             dataset: Iterable[int]) -> tuple[Suite, list[float]]:
    """Estimate total train number based on observations
    :param hypos: hypotheses in sequence of (number of train, probability)
    :param dataset: observations of train ids
    :param verbose: show probabilities of each possible train number in txt
    :param plot: plot updated hypotheses distribution
    :return: (Final Suite, estimations) that can be used for plotting
    """
    suite = Train()
    for h, p in hypo_dists:
        suite.Set(h, p)

    suite.Normalize()

    # Estimation sequences based on given observations
    ests = []
    for d in dataset:
        suite.Update(d)
        ests.append(suite.Mean())

    return suite, ests


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
dataset = [60]
suite, ests = estimate(hypo_dists=get_even_hypo_dists(LIMIT), dataset=dataset)
print()
print(f'Limit: {LIMIT}, observations: {dataset}')
print('Detailed distribution:')
suite.Print()
print(f'Estimations: {ests}, final estimation: {ests[-1]}')

thinkplot.Clf()
thinkplot.PrePlot(1)
thinkplot.Pmf(suite)
thinkplot.Show(xlabel="Number of trains", ylabel="Probability")


print()
print()
print('##############################')
print(' Even Distribution Hypotheses')
print('##############################')

limits = [500, 1000, 2000]
dataset = [60, 30, 90]

thinkplot.Clf()
thinkplot.PrePlot(len(limits))
for limit in limits:
    suite, ests = estimate(hypo_dists=get_even_hypo_dists(limit), dataset=dataset)
    suite.name = str(limit) # Set suite name for plotting legends
    thinkplot.Pmf(suite)
    print(f'Limit: {limit}, observations: {dataset}, estimations: {ests}, final estimation: {ests[-1]}')

thinkplot.Show(title='Even distribution hypotheses',
               xlabel='Number of trains',
               ylabel='Probability')


print()
print()
print('###################################')
print(' Power-law Distribution Hypotheses')
print('###################################')

limits = [500, 1000, 2000]
dataset = [60, 30, 90]

thinkplot.Clf()
thinkplot.PrePlot(len(limits))
for limit in limits:
    suite, ests = estimate(hypo_dists=get_power_law_hypo_dists(limit), dataset=dataset)
    suite.name = str(limit)
    thinkplot.Pmf(suite)
    print(f'Limit: {limit}, observations: {dataset}, estimations: {ests}, final estimation: {ests[-1]}')

thinkplot.Show(title='Power-law distribution hypotheses',
               xlabel='Number of trains',
               ylabel='Probability')


print()
print()
print('##########################################')
print(' Even vs Power-law Distribution Hypotheses')
print('##########################################')

limit = 1000
dataset = [60, 30, 90]
even_hypo_dists = get_even_hypo_dists(limit)
power_law_dists = get_power_law_hypo_dists(limit)
thinkplot.Clf()
thinkplot.PrePlot(2)
even_suite, even_ests = estimate(hypo_dists=even_hypo_dists, dataset=dataset)
even_suite.name = "Even"
thinkplot.Pmf(even_suite)
print(f'Limit: {limit}, observations: {dataset}, estimations: {even_ests}, final estimation: {even_ests[-1]}')

cdf = even_suite.MakeCdf()
interval_percent_start, interval_percent_end = 5, 95
interval_start, interval_end = (
    cdf.Percentile(interval_percent_start),
    cdf.Percentile(interval_percent_end))
print('Even Distribution Hypotheses Confidence Interval:')
print(f'({interval_percent_start}%, {interval_percent_end}%), {interval_start}, {interval_end}')

power_law_suite, power_law_ests = estimate(hypo_dists=power_law_dists, dataset=dataset)
power_law_suite.name = "Power-law"
thinkplot.Pmf(power_law_suite)
print(f'Limit: {limit}, observations: {dataset}, estimations: {power_law_ests}, final estimation: {power_law_ests[-1]}')

cdf = power_law_suite.MakeCdf()
interval_percent_start, interval_percent_end = 5, 95
interval_start, interval_end = (
    cdf.Percentile(interval_percent_start),
    cdf.Percentile(interval_percent_end))
print('Power Law Distribution Hypotheses Confidence Interval:')
print(f'({interval_percent_start}%, {interval_percent_end}%), {interval_start}, {interval_end}')


thinkplot.Show(title='Even vs Power-law distribution hypotheses',
               xlabel='Number of trains',
               ylabel='Probability')
