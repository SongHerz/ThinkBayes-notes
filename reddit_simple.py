#!/usr/bin/env python3

from reddit.simple import vote
from reddit.test_vec import gen_test_vec

def test_simple():
    """Run simple policy with test vector"""
    vec = gen_test_vec()
    for user_id, link_id, vote_dir in vec:
        vote(user_id=user_id, link_id=link_id, dir_=vote_dir)


if __name__ == '__main__':
    test_simple()
