#!/usr/bin/env python3
"""
Generate test vector
"""

import math
from random import Random
import numpy as np

from .comm import VoteDir


def _calc_reversibility(reliability: float) -> float:
    """Calculate vote reversibility given reliability"""
    assert 0.0 <= reliability <= 1.0

    # Linear Map reliability -> revsersibility
    # 1 -> 0
    # 0 -> 0.5
    # ==> reversibility = (-0.5) * reliability + 0.5
    return (-0.5) *  reliability + 0.5


def _reverse_vote_dir(vote_dir: VoteDir) -> VoteDir:
    if vote_dir == VoteDir.UP:
        return VoteDir.DOWN
    else:
        assert vote_dir == VoteDir.DOWN
        return VoteDir.UP


def _calc_vote_dir(rand: Random, reliability: float, intended_vote_dir: VoteDir) -> VoteDir:
    """
    Calculate user vote based on its reliability.
    """
    rev = _calc_reversibility(reliability)

    roll = rand.random()
    if rev < roll:
        # Keep intended vote
        return intended_vote_dir
    else:
        # Reverse intended vote
        return _reverse_vote_dir(intended_vote_dir)


def gen_test_vec() -> list[tuple[int, int, VoteDir]]:
    """
    Generate test vector.
    :return: list of test vectors in [(user id, link id, vote dir)]
    """
    rand = Random(100)

    USER_COUNT = 8
    LINK_COUNT = 15
    user_ids = list(range(USER_COUNT))

    GOOD_LINK_RATIO = 0.8

    # Classify predefined good / bad links
    last_good_link_idx_plus1 = math.floor(LINK_COUNT * GOOD_LINK_RATIO)
    good_link_ids = list(range(0, last_good_link_idx_plus1))
    bad_link_ids = list(range(last_good_link_idx_plus1, LINK_COUNT))

    # Assign user reliability from [1.0 to 0.0]
    uid_reli_map = {}
    uid_reli_map.update(x for x in zip(user_ids, list(np.linspace(start=1.0, stop=0.0, num=len(user_ids), dtype=float))))

    # {(uid, link id): vote_dir}
    vote_map = {}
    for uid, reli in uid_reli_map.items():
        for link_id in good_link_ids:
            k = (uid, link_id)
            if k in vote_map:
                # Only the first random vote sound.
                continue

            vote_dir = _calc_vote_dir(rand, reli, VoteDir.UP)
            vote_map[k] = vote_dir

        for link_id in bad_link_ids:
            k = (uid, link_id)
            if k in vote_map:
                # Only the first random vote sound.
                continue

            vote_dir = _calc_vote_dir(rand, reli, VoteDir.DOWN)
            vote_map[k] = vote_dir

    print()
    print('#####################')
    print(' Test Vector Summary')
    print('#####################')
    print()
    print('# Link Quality')
    print(f'Good Links: {good_link_ids}')
    print(f'Bad Links: {bad_link_ids}')
    print()
    print('# User reliability')
    for uid, reli in uid_reli_map.items():
        print(f'user: {uid}, reliability: {reli}')

    print()

    return [(user_id, link_id, vote_dir) for (user_id, link_id), vote_dir in vote_map.items()]
