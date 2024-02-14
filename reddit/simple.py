#!/usr/bin/env python3

"""
Reddit problem simple model.
"""

from .comm import VoteDir, Vote, Link, User
from .pool import get_pool


def _is_user_vote_reliable(u: User, link: Link) -> bool | None:
    """
    :return: True, the user vote for the given link is reliable
             False, the user vote for the given link is unreliable
             None, the user has no vote for the given link, or it cannot determine user vote is reliable or not.
    """
    user_vote = link.get_vote(u)
    if user_vote is None:
        return None

    up_vote_cnt = 0
    dn_vote_cnt = 0
    for v in link.votes:
        if v.dir_ == VoteDir.UP:
            up_vote_cnt += 1
        else:
            assert v.dir_ == VoteDir.DOWN
            dn_vote_cnt += 1

    link_is_good = None
    if up_vote_cnt > dn_vote_cnt:
        # This is a good link
        link_is_good = True
    elif up_vote_cnt == dn_vote_cnt:
        # Not sure this is a good link or a bad link
        link_is_good = False
    else:
        assert up_vote_cnt < dn_vote_cnt
        # This is a bad link
        link_is_good = False

    if link_is_good:
        if user_vote.dir_ == VoteDir.UP:
            return True
        else:
            assert user_vote.dir_ == VoteDir.DOWN
            return False
    else:
        if user_vote.dir_ == VoteDir.DOWN:
            return None
        else:
            assert user_vote.dir_ == VoteDir.UP
            return False


def _update_user_reliability(u: User):
    link_it = get_pool().links

    reli_vote_cnt = 0
    unreli_vote_cnt = 0

    for link in link_it:
        reli = _is_user_vote_reliable(u, link)
        if reli is None:
            continue

        if reli:
            reli_vote_cnt += 1
        else:
            unreli_vote_cnt += 1

    tot_vote_cnt = reli_vote_cnt + unreli_vote_cnt
    assert tot_vote_cnt > 0
    u.reliability = reli_vote_cnt / tot_vote_cnt


def _update_vote_user_reliabilities(link: Link):
    """Update users who has vote for given link"""
    # Users to update {user id: User}
    users = {}
    for v in link.votes:
        if v.user.id_ not in users:
            users[v.user.id_] = v.user

    for u in users.values():
        _update_user_reliability(u)


def vote(user_id: int, link_id: int, dir_: VoteDir):
    """User vote a link"""
    user = get_pool().get_user(user_id)
    link = get_pool().get_link(link_id)
    vote_ = Vote(user, dir_)
    link.add_vote(vote_)
    link.update_quality()
    _update_vote_user_reliabilities(link)
