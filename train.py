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
    Train likelihood even distribution on given hypothesis .
    """

    def Likelihood(self, data: int, hypo: int) -> float:
        if hypo < data:
            return 0.0

        return 1.0 / hypo


class Train2(Suite):
    """
    When there are multiple companies
    """
    def Likelihood(self, data: int, hypo: int) -> float:
        if hypo < data:
            return 0.0

        # Assume train ids also in power-law distribution.
        assert data <= hypo
        alpha = 1.0
        s = sum(d ** (-alpha) for d in range(1, hypo + 1))
        return (data ** (-alpha)) / s


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
    """Result of an estimation"""
    limit: int
    dataset: Sequence[int]
    suite: Suite
    # Estimations on each updates
    ests: list[float]
    # Credible interval in percents (start, end)
    ci_start_pct: float
    ci_end_pct: float
    # Credible interval in estimated numbers (start, end)
    ci_start: float
    ci_end: float


def get_ests(suite_constr: Callable[[], Suite],
             hypo_dists_func: Callable[[int], list[tuple[int, float]]],
             limits: Sequence[int],
             dataset: Sequence[int]) -> list[Estimation]:
    """Generate estimations"""
    ret = []
    for limit in limits:
        hypo_dists = hypo_dists_func(limit)
        suite, ests = estimate(suite_constr, hypo_dists=hypo_dists, dataset=dataset)
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


def plot_ests(ests: list[Estimation], title: str):
    """Plot estimation results"""
    thinkplot.Clf()
    thinkplot.PrePlot(len(ests))
    limits = []
    for est in ests:
        limits.append(est.limit)
        thinkplot.Pmf(est.suite)
        print(f'Limit: {est.limit}, dataset: {est.dataset}, '
              f'estimations: {est.ests}, final estimation: {est.ests[-1]}')

        ci_str = (f'Credible interval {est.ci_start_pct}% ~ {est.ci_end_pct}%: '
                  f'{est.ci_start} ~ {est.ci_end}')
        print(ci_str)

    thinkplot.Show(title=title,
                   xlabel='Number of trains',
                   ylabel='Probability')


def plot_alot(suite_constr: Callable[[], Suite]):
    """Plot with various plots"""
    limits = [1000]
    dataset = [60]
    ests = get_ests(suite_constr=suite_constr,
                    hypo_dists_func=get_even_hypo_dists,
                    limits=limits,
                    dataset=dataset)
    plot_ests(ests=ests,
              title='\n'.join(['Even distribution hypotheses',
                               f'Distribution limits: {limits}',
                               f'Dataset: {dataset}',
                               ]))


    print()
    print()
    print('##############################')
    print(' Even Distribution Hypotheses')
    print('##############################')
    limits = [500, 1000, 2000]
    dataset = [60, 30, 90]
    ests = get_ests(suite_constr=suite_constr,
                    hypo_dists_func=get_even_hypo_dists,
                    limits=limits,
                    dataset=dataset)
    plot_ests(ests=ests,
              title='\n'.join(['Even distribution hypotheses',
                               f'Distribution limits: {limits}',
                               f'Dataset: {dataset}',
                               ]))


    print()
    print()
    print('###################################')
    print(' Power-law Distribution Hypotheses')
    print('###################################')
    limits = [500, 1000, 2000]
    dataset = [60, 30, 90]
    ests = get_ests(suite_constr=suite_constr,
                    hypo_dists_func=lambda x: get_power_law_hypo_dists(x, alpha=1.0),
                    limits=limits,
                    dataset=dataset)
    plot_ests(ests=ests,
              title='\n'.join(['Power-law distribution hypotheses',
                               f'Distribution limits: {limits}',
                               f'Dataset: {dataset}',
                               ]))


    print()
    print()
    print('##########################################')
    print(' Even vs Power-law Distribution Hypotheses')
    print('##########################################')

    limit = 1000
    dataset = [60, 30, 90]
    even_ests = get_ests(suite_constr=suite_constr,
                         hypo_dists_func=get_even_hypo_dists,
                         limits=[limit],
                         dataset=dataset)
    assert len(even_ests) == 1
    # Overwrite name for plotting legends
    even_ests[0].suite.name = 'Even'

    power_law_ests = get_ests(suite_constr=suite_constr,
                              hypo_dists_func=lambda x: get_power_law_hypo_dists(x, alpha=1.0),
                              limits=[limit],
                              dataset=dataset)
    assert len(power_law_ests) == 1
    power_law_ests[0].suite.name = 'Power-law'

    ests = []
    ests.extend(even_ests)
    ests.extend(power_law_ests)

    plot_ests(ests=ests,
              title='\n'.join(['Even vs Power-law distribution hypotheses',
                               f'Distribution limits: {[limit]}',
                               f'Dataset: {dataset}',
                               ]))

print()
print('#############')
print(' One Company')
print('#############')
plot_alot(Train)
print()
print('###############')
print(' Multi-Company')
print('###############')
plot_alot(Train2)
