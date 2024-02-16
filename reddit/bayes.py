#!/usr/bin/env python3

"""
Reddit problem bayes model.
"""

from thinkbayes import Suite

from .comm import Vote, VoteDir, Link, User
from .pool import cfg_pool, get_pool


class LinkQuality(Suite):
    """
    Link quality modeled by Bayes model.
    """
    def __init__(self, name: str):
        super().__init__(range(1, 101), name=name)

    def _likelihood(self, vote_dir: VoteDir, reversibility: float, hypo: int) -> float:
        """
        Denote:
        - hypo U: Upvote with given hypothesis
        - hypo D: Downvote with given hypothesis

        Because of reversibility, there are 4 scenarios:
        - hypo U -> measured U: denote u2u
        - hypo U -> measured D: denote u2d
        - hypo D -> measured D: denote d2d
        - hypo D -> measured U: denote d2u

        Given hypothesis upvote probability is x%
        hypo U likelihood: x / 100
        hypo D likelihood: 1 - hypo U likelihood = 1 - x / 100

        measured U likelihood = u2u likelihood + d2u likelihood
        measured D likelihood = d2d likelihood + u2d likelihood

        u2u likelihood = hypo U likelihood * (1 - reversibility)
        u2d likelihood = hypo U likelihood * reversibility

        d2d likelihood = hypo D likelihood * (1 - reversibility)
        d2u likelihood = hypo D likelihood * reversibility

        ==>
        measured U likelihood
        = u2u likelihood + d2u likelihood
        = hypo U likelihood * (1 - reversibility) + hypo D likelihood * reversibility
        = (x / 100) * (1 - reversibility) + (1 - x / 100) * reversibility

        measured D likelihood
        = d2d likelihood + u2d likelihood
        = hypo D likelihood * (1 - reversibility) + hypo U likelihood * reversibility
        = (1 - x / 100) * (1 - reversibility) + (x / 100) * reversibility

        And it is easy to verify that, when reversibility is zero.
        measured U likelihood = x / 100 = hypo U likelihood
        measured D likelihood = 1 - x / 100 = hypo D likelihood
        """
        x = hypo

        hypo_U_like = x / 100
        hypo_D_like = 1 - x / 100

        if vote_dir == VoteDir.UP:
            return hypo_U_like * (1 - reversibility) + hypo_D_like * reversibility
        else:
            assert vote_dir == VoteDir.DOWN
            return hypo_D_like * (1 - reversibility) + hypo_U_like * reversibility

    def Likelihood(self, data: Vote, hypo: int) -> float:
        """
        :data: Vote
        :hypo: hypothesis of upvote percentage
        """
        return self._likelihood(
            vote_dir=data.dir_,
            reversibility=data.user.reversibility,
            hypo=hypo)


class BLink(Link):
    """Link with bayes model"""
    def __init__(self, id_: int):
        super().__init__(id_)
        # Give pmf a name for visualization
        self._l_quality = LinkQuality(name=f'link_{id_}')

    @property
    def quality(self) -> float | None:
        """Quality of this link"""
        return self._l_quality.Mean()

    def quality2(self) -> float | None:
        return self._l_quality.MaximumLikelihood()

    def pre_commit_update_quality(self):
        """Update quality with staged votes"""
        self._l_quality.UpdateSet(self._staged_votes)

    def post_commit_update_quality(self):
        pass


# def _is_user_vote_reliable(u: User, link: Link) -> bool | None:
#     """
#     :return: True, the user vote for the given link is reliable
#              False, the user vote for the given link is unreliable
#              None, the user has no vote for the given link, or it cannot determine user vote is reliable or not.
#     """
#     user_vote = link.get_vote(u)
#     if user_vote is None:
#         return None
#
#     up_vote_cnt = 0
#     dn_vote_cnt = 0
#     for v in link.votes:
#         if v.dir_ == VoteDir.UP:
#             up_vote_cnt += 1
#         else:
#             assert v.dir_ == VoteDir.DOWN
#             dn_vote_cnt += 1
#
#     link_is_good = None
#     if up_vote_cnt > dn_vote_cnt:
#         # This is a good link
#         link_is_good = True
#     elif up_vote_cnt == dn_vote_cnt:
#         # Not sure this is a good link or a bad link
#         link_is_good = None
#     else:
#         assert up_vote_cnt < dn_vote_cnt
#         # This is a bad link
#         link_is_good = False
#
#     if link_is_good is None:
#         return None
#     elif link_is_good:
#         if user_vote.dir_ == VoteDir.UP:
#             return True
#         else:
#             assert user_vote.dir_ == VoteDir.DOWN
#             return False
#     else:
#         if user_vote.dir_ == VoteDir.DOWN:
#             return True
#         else:
#             assert user_vote.dir_ == VoteDir.UP
#             return False


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
    link.commit_vote()
    _update_vote_user_reliabilities(link)


# Use simple link constructor to create new links
cfg_pool(BLink)
