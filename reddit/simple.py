#!/usr/bin/env python3

"""
Reddit problem simple model.
"""

from .comm import ResourcePool, VoteDir, Vote

g_pool = ResourcePool()

def vote(user_id: int, link_id: int, dir_: VoteDir):
    """User vote a link"""
    user = g_pool.get_user(user_id)
    link = g_pool.get_link(link_id)
    vote_ = Vote(user, dir_)
    link.add_vote(vote_)
