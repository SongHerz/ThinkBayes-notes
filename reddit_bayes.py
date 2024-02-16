#!/usr/bin/env python3

from reddit.bayes import vote, get_pool
from reddit.test_vec import gen_test_vec


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


if __name__ == '__main__':
    test_bayes()
