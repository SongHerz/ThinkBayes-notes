#!/usr/bin/env python3
"""
Solve dice problem
"""

from thinkbayes import Suite


class Dice(Suite):
    """Dice class"""

    def Likelihood(self, data: float, hypo: int) -> float:
        if hypo < data:
            return 0

        return 1.0 / hypo


dice = Dice([4, 6, 8, 12, 20])

rolls = [6, 8, 7, 7, 5, 4]
for i, r in enumerate(rolls, start=1):
    dice.Update(r)
    print()
    print(f'{i}th experiment')
    print(f'  number: {r}')
    print('  Updated posterier')
    dice.Print()
