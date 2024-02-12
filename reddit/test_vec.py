#!/usr/bin/env python3
"""
Generate test vector
"""

import random

from .comm import VoteDir


def gen_test_vec() -> list[tuple[int, int, VoteDir]]:
    """
    Generate test vector.
    :return: list of test vectors in [(user id, link id, vote dir)]
    """
    user_ids = list(range(10))
    link_ids = list(range(15))

    ret = []
    for uid in user_ids:
        for _ in link_ids:
            link_id = random.choice(link_ids)
            dir_ = random.randint(0, 1)
            if dir_ == 0:
                vote_dir = VoteDir.UP
            else:
                vote_dir = VoteDir.DOWN

            ret.append((uid, link_id, vote_dir))

    return ret
