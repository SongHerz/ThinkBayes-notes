#!/usr/bin/env python3

from reddit.bayes import vote, get_pool
from reddit.test_vec import gen_test_vec
import thinkplot


def test_bayes():
    """Run bayes model with test vector"""
    vec = gen_test_vec()
    for user_id, link_id, vote_dir in vec:
        vote(user_id=user_id, link_id=link_id, dir_=vote_dir)

    print()
    print('#####################')
    print('# Calculated Summary#')
    print('#####################')
    get_pool().print_summary()

    print("DEBUG QUALITY 2")

    # thinkplot.Pmfs([link._l_quality for link in get_pool().links])
    # thinkplot.Show(xlabel='x', ylabel='Probability')

    for link in get_pool().links:
        thinkplot.Pmf(link._l_quality)
        thinkplot.Show(xlabel='x', ylabel='Probability')
        print(f'Link: {link.id_}, quality2: {link.quality2()}')


if __name__ == '__main__':
    test_bayes()
