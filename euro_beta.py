#!/usr/bin/env python3
"""
Calculate euro coin uniformness with beta distribution.

This link explains beta distributeion, and its relation to Bayes well
https://www.zhihu.com/question/30269898
"""

from thinkbayes import Beta

HEADS = 140
TAILS = 110

beta = Beta()
beta.Update((HEADS, TAILS))
print('Mean:', beta.Mean())
