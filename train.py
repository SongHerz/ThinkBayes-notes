#!/usr/bin/env python3
"""
Train number estimation
"""

from thinkbayes import Suite
import thinkplot


class EvenDistHypoTrain(Suite):
    """
    Even distribution hypothesis .
    """

    def Likelihood(self, data: int, hypo: int) -> float:
        if hypo < data:
            return 0.0

        return 1.0 / hypo


hypos = range(1, 1001)
suite = EvenDistHypoTrain(hypos)
suite.Update(60)
suite.Print()
print()
print("Mean", suite.Mean())
thinkplot.PrePlot(1)
thinkplot.Pmf(suite)
thinkplot.Show(xlabel="Number of trains", ylabel="Probability")
