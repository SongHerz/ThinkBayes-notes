#!/usr/bin/env python3

"""
Reddit problem bayes model.
Only link are modeled by bayes.
"""

from .comm import Vote, VoteDir, Link, User
from .simpleobj import SUser
from .bayesobj import BLink
from .pool import cfg_pool, get_pool


def _is_user_vote_reliable(u: User, link: Link) -> bool | None:
    """
    :return: True, the user vote for the given link is reliable
             False, the user vote for the given link is unreliable
             None, the user has no vote for the given link, or it cannot determine user vote is reliable or not.
    """
    user_vote = link.get_vote(u)
    if user_vote is None:
        return None

    lq = link.quality
    delta = 0.001
    link_is_good = None

    if lq > 0.5 + delta:
        link_is_good = True
    elif 0.5 - delta <= lq <= 0.5 + delta:
        # When the link quality is confusing, consider the link good.
        link_is_good = None
    else:
        assert lq < 0.5 - delta
        link_is_good = False

    if link_is_good is None:
        return None
    elif link_is_good:
        if user_vote.dir_ == VoteDir.UP:
            return True
        else:
            assert user_vote.dir_ == VoteDir.DOWN
            return False
    else:
        if user_vote.dir_ == VoteDir.DOWN:
            return True
        else:
            assert user_vote.dir_ == VoteDir.UP
            return False


def _update_suser_reliability(u: User):
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


def _update_vote_suser_reliabilities(link: Link):
    """Update users who has vote for given link"""
    # Users to update {user id: User}
    users = {}
    for v in link.votes:
        if v.user.id_ not in users:
            users[v.user.id_] = v.user

    for u in users.values():
        _update_suser_reliability(u)


def vote(user_id: int, link_id: int, dir_: VoteDir):
    """User vote a link"""
    user = get_pool().get_user(user_id)
    link = get_pool().get_link(link_id)
    vote_ = Vote(user, dir_)
    link.add_vote(vote_)
    link.commit_vote()
    _update_vote_suser_reliabilities(link)


# Use simple link constructor to create new links
cfg_pool(SUser, BLink)
