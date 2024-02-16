#!/usr/bin/env python3
"""
Generate test vector
"""

import math
from random import Random
from collections import Counter
import numpy as np

from .comm import VoteDir


# def _reliability_to_reversibility(reliability: float) -> float:
#     """Calculate vote reversibility given reliability"""
#     assert 0.0 <= reliability <= 1.0
#
#     # Linear Map reliability -> revsersibility
#     # 1 -> 0
#     # 0 -> 0.5
#     # ==> reversibility = (-0.5) * reliability + 0.5
#     return (-0.5) *  reliability + 0.5
#
# def _reversibility_to_reliability(reversibility: float) -> float:
#     """Reverse function of _reliability_to_reversibility"""
#     return (-2) * reversibility + 1

def _reliability_to_reversibility(reliability: float) -> float:
    assert 0.0 <= reliability <= 1.0
    return 1.0 - reliability

def _reversibility_to_reliability(reversibility: float) -> float:
    assert 0.0 <= reversibility <= 1.0
    return 1.0 - reversibility

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
    rev = _reliability_to_reversibility(reliability)

    roll = rand.random()
    if rev < roll:
        # Keep intended vote
        return intended_vote_dir
    else:
        # Reverse intended vote
        return _reverse_vote_dir(intended_vote_dir)


def _get_decimal_next_order_of_magnitute(v: int) -> int:
    """Calculate next order of magnitute
    e.g. 
    1. 50 -> 100
    1. 99 -> 100
    1. 100 -> 1000
    """
    assert v > 0
    order = math.log10(v)
    next_order = math.ceil(order)
    if next_order == order:
        # In case of v == 10, 100, 1000 ...
        next_order += 1

    return 10 ** next_order


def gen_test_vec(shuffle: bool) -> list[tuple[int, int, VoteDir]]:
    """
    Generate test vector.
    :param shuffle: shuffle test vector before returning.
    :return: list of test vectors in [(user id, link id, vote dir)]
    """
    rand = Random(100)

    USER_COUNT = 8        # pylint: disable=C0103
    LINK_COUNT = 15       # pylint: disable=C0103
    GOOD_LINK_RATIO = 0.8 # pylint: disable=C0103
    GOOD_LINK_COUNT = math.floor(LINK_COUNT * GOOD_LINK_RATIO) # pylint: disable=C0103
    BAD_LINK_COUNT = LINK_COUNT - GOOD_LINK_COUNT              # pylint: disable=C0103
    user_ids = list(range(USER_COUNT))

    GOOD_LINK_START = 0   # pylint: disable=C0103
    GOOD_LINK_END_INC = GOOD_LINK_START + GOOD_LINK_COUNT - 1                # pylint: disable=C0103
    BAD_LINK_START = _get_decimal_next_order_of_magnitute(GOOD_LINK_END_INC) # pylint: disable=C0103
    BAD_LINK_END_INC = BAD_LINK_START + BAD_LINK_COUNT - 1                   # pylint: disable=C0103


    # Predefined good / bad links
    good_link_ids = list(range(GOOD_LINK_START, GOOD_LINK_END_INC + 1))
    bad_link_ids = list(range(BAD_LINK_START, BAD_LINK_END_INC + 1))
    assert len(set(good_link_ids).intersection(bad_link_ids)) == 0, 'No link id overlap allowed'

    # Assign user reliability from 1.0 to 0.5
    uid_reli_map = {}
    uid_reli_map.update(
        x for x in zip(user_ids, np.linspace(start=1.0, stop=0.5, num=len(user_ids), dtype=float)))

    ########################
    # Generate test vector #
    ########################
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

    ####################################################
    # Calculate User Reliability After Vote Simulation #
    ####################################################
    # {uid: relibility}
    sim_uid_vote_intended_cnt_map = Counter()
    sim_uid_vote_unintended_cnt_map = Counter()
    for (uid, link_id), vote_dir in vote_map.items():
        if link_id in good_link_ids:
            is_intended_vote_dir = (vote_dir == VoteDir.UP)   # pylint: disable=C0325
        else:
            assert link_id in bad_link_ids
            is_intended_vote_dir = (vote_dir == VoteDir.DOWN) # pylint: disable=C0325

        if is_intended_vote_dir:
            sim_uid_vote_intended_cnt_map[uid] += 1
        else:
            sim_uid_vote_unintended_cnt_map[uid] += 1

    sim_uid_reli_map = {}
    for uid in user_ids:
        intended_votes = sim_uid_vote_intended_cnt_map[uid]
        unintended_votes = sim_uid_vote_unintended_cnt_map[uid]
        reversibility = unintended_votes / (intended_votes + unintended_votes)
        reliability = _reversibility_to_reliability(reversibility)
        sim_uid_reli_map[uid] = reliability


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
        sim_reli = sim_uid_reli_map[uid]
        print(f'user: {uid}, planned reliability: {reli}, sim reliability: {sim_reli}')

    print()

    vec = [(user_id, link_id, vote_dir) for (user_id, link_id), vote_dir in vote_map.items()]
    if shuffle:
        rand.shuffle(vec)

    return vec
