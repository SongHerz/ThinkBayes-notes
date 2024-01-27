#!/usr/bin/env python3
"""
Train number estimation
"""

from typing import Iterable, Sequence, Callable
from dataclasses import dataclass

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


def estimate(suite_constr: Callable[[], Suite],
             hypo_dists: Sequence[tuple[int, float]],
             dataset: Iterable[int]) -> tuple[Suite, list[float]]:
    """Estimate total train number based on observations
    :param hypos: hypotheses in sequence of (number of train, probability)
    :param dataset: observations of train ids
    :param verbose: show probabilities of each possible train number in txt
    :param plot: plot updated hypotheses distribution
    :return: (Final Suite, estimations) that can be used for plotting
    """
    suite = suite_constr()
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


@dataclass(frozen=True)
class Estimation:
    limit: int
    dataset: Sequence[int]
    suite: Suite
    # Estimations on each updates
    ests: list[float]
    # Confidence interval in percents (start, end)
    ci_start_pct: float
    ci_end_pct: float
    # Confidence interval in estimated numbers (start, end)
    ci_start: float
    ci_end: float


def get_ests(limits: Sequence[int],
             dataset: Sequence[int],
             hypo_dists_func: Callable[[int], list[tuple[int, float]]]) -> list[Estimation]:
    """Generate estimations"""
    ret = []
    for limit in limits:
        hypo_dists = hypo_dists_func(limit)
        suite, ests = estimate(Train, hypo_dists=hypo_dists, dataset=dataset)
        suite.name = str(limit) # Set suite name for plotting legends

        cdf = suite.MakeCdf()
        ci_start_pct, ci_end_pct = 5, 95
        ci_start, ci_end = cdf.Percentile(ci_start_pct), cdf.Percentile(ci_end_pct)
        ret.append(Estimation(limit=limit,
                              dataset=dataset,
                              suite=suite,
                              ests=ests,
                              ci_start_pct=ci_start_pct,
                              ci_end_pct=ci_end_pct,
                              ci_start=ci_start,
                              ci_end=ci_end))
    return ret


def plot_est(ests: list[Estimation], title: str):
    """Plot estimation results"""
    thinkplot.Clf()
    thinkplot.PrePlot(len(ests))
    limits = []
    for est in ests:
        limits.append(est.limit)
        # Set label name for plotting legends
        thinkplot.Pmf(est.suite, label=str(est.limit))
        print(f'Limit: {est.limit}, dataset: {est.dataset}, estimations: {est.ests}, final estimation: {est.ests[-1]}')

        ci_str = f'Confidence interval {est.ci_start_pct}% ~ {est.ci_end_pct}%: {est.ci_start} ~ {est.ci_end}'
        print(ci_str)

    thinkplot.Show(title='\n'.join([f'{title}',
                                    f'Distribution limits: {limits}',
                                    ci_str,
                                    ]),
                   xlabel='Number of trains',
                   ylabel='Probability')


plot_est(ests=get_ests(limits=[1000],
                       dataset=[60],
                       hypo_dists_func=get_even_hypo_dists),
          title='Even distribution hypotheses')


print()
print()
print('##############################')
print(' Even Distribution Hypotheses')
print('##############################')
plot_est(ests=get_ests(limits=[500, 1000, 2000],
                       dataset=[60, 30, 90],
                       hypo_dists_func=get_even_hypo_dists),
         title='Even distribution hypotheses')


print()
print()
print('###################################')
print(' Power-law Distribution Hypotheses')
print('###################################')
plot_est(ests=get_ests(limits=[500, 1000, 2000],
                       dataset=[60, 30, 90],
                       hypo_dists_func=lambda x: get_power_law_hypo_dists(x, alpha=1.0)),
        title='Power-law distribution hypotheses')


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
even_suite, even_ests = estimate(Train, hypo_dists=even_hypo_dists, dataset=dataset)
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

power_law_suite, power_law_ests = estimate(Train, hypo_dists=power_law_dists, dataset=dataset)
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


thinkplot.Show(title='\n'.join(['Even vs Power-law distribution hypotheses',
                                f'Distribution limits: {limit}',
                                f'Dataset: {dataset}']),
               xlabel='Number of trains',
               ylabel='Probability')
