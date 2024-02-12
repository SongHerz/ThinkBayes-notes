#!/usr/bin/env python3
"""
Generate test vector
"""

import math
from random import Random
import numpy as np

from .comm import VoteDir


def gen_test_vec() -> list[tuple[int, int, VoteDir]]:
    """
    Generate test vector.
    :return: list of test vectors in [(user id, link id, vote dir)]
    """
    rand = Random(100)

    USER_COUNT = 5
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
    for uid in user_ids:
        for link_id in good_link_ids:
            # link_id = rand.choice(link_ids)
            # dir_ = rand.randint(0, 1)
            # FIXME: calculate dir based on good/bad link and user reliability
            dir_ = 0

            k = (uid, link_id)
            if k in vote_map:
                # Only the first random vote sound.
                continue

            if dir_ == 0:
                vote_dir = VoteDir.UP
            else:
                vote_dir = VoteDir.DOWN

            vote_map[k] = vote_dir

        for link_id in bad_link_ids:
            # FIXME: calculate dir based on good/bad link and user reliability
            dir_ = 1

            k = (uid, link_id)
            if k in vote_map:
                # Only the first random vote sound.
                continue

            if dir_ == 0:
                vote_dir = VoteDir.UP
            else:
                vote_dir = VoteDir.DOWN

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
