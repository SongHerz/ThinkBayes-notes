#!/usr/bin/env python3

"""
Reddit problem with bayes modeled link and simple user.
"""

from .comm import Vote, VoteDir
from .bayesobj import BLink, BUser
from .pool import cfg_pool, get_pool


def vote(user_id: int, link_id: int, dir_: VoteDir):
    """User vote a link"""
    user = get_pool().get_user(user_id)
    link = get_pool().get_link(link_id)
    # Link quality before this vote
    lq_b4_new_vote = link.quality
    new_vote = Vote(user, dir_)
    link.add_vote(new_vote)
    link.commit_vote()

    user.update_reliability(new_vote, lq_b4_new_vote)



# Use simple link constructor to create new links
cfg_pool(BUser, BLink)
