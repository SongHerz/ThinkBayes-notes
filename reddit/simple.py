#!/usr/bin/env python3

"""
Reddit problem simple model.
"""

from .comm import ResourcePool, VoteDir, Vote

_g_pool = ResourcePool()


def get_pool() -> ResourcePool:
    """Singleton ResourcePool"""
    return _g_pool


def vote(user_id: int, link_id: int, dir_: VoteDir):
    """User vote a link"""
    user = _g_pool.get_user(user_id)
    link = _g_pool.get_link(link_id)
    vote_ = Vote(user, dir_)
    link.add_vote(vote_)
    link.update_quality()
