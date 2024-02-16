#!/usr/bin/env python3

from reddit.bayes import vote, get_pool
from reddit.test_vec import gen_test_vec
import thinkplot


def test_bayes():
    """Run bayes model with test vector"""
    vec = gen_test_vec(True)
    for i, (user_id, link_id, vote_dir) in enumerate(vec):
        vote(user_id=user_id, link_id=link_id, dir_=vote_dir)
        # print()
        # print(f'# LOOP: {i}')
        # print(f'test vec: user id: {user_id}, link id: {link_id}, vote dir: {vote_dir}')
        # get_pool().print_summary()

    print()
    print('#####################')
    print('# Calculated Summary#')
    print('#####################')
    get_pool().print_summary()

    print("DEBUG QUALITY 2")

    # thinkplot.Pmfs([link._l_quality for link in get_pool().links])
    # thinkplot.Show(xlabel='x', ylabel='Probability')

    for user in get_pool().users:
        print(f'User: {user.id_}, reliability: {user.reliability}, max likelihood: {user.max_likelihood}')
        thinkplot.Pmf(user._reliability)
        thinkplot.Show(xlabel='x', ylabel='Probability')

    for link in get_pool().links:
        print(f'Link: {link.id_}, quality: {link.quality}, max likelihood: {link.max_likelihood}')
        thinkplot.Pmf(link._l_quality)
        thinkplot.Show(xlabel='x', ylabel='Probability')



if __name__ == '__main__':
    test_bayes()
