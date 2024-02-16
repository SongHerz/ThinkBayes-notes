#!/usr/bin/env python3

"""
Reddit problem user / link bayes model.
"""

import numpy as np
from thinkbayes import Suite

from .comm import Vote, VoteDir, Link, User


class UserReliability(Suite):
    """
    User reliability modeled by Bayes model.
    """
    def __init__(self, name: str):
        super().__init__(np.linspace(start=1.0 / 100, stop=1.0, num=100, dtype=float), name=name)

    def Likelihood(self, data: tuple[Vote, float], hypo: int) -> float:
        x = hypo
        vote_reli_like = x
        vote_unreli_like = 1 - x
        # When a vote is unjudgable, give same likelihood to all hypos
        vote_unjudge_like = 1.0

        # vote, and link quality (this vote excluded)
        vote, lq = data
        delta = 0.0001

        link_is_good = None
        if lq > 0.5 + delta:
            # this link is good
            link_is_good = True
        elif 0.5 - delta <= lq <= 0.5 + delta:
            # Not sure if this link is good or not
            link_is_good = None
        else:
            assert lq < 0.5 - delta
            link_is_good = False

        if link_is_good is None:
            return vote_unjudge_like

        expected_vote_dir = VoteDir.UP if link_is_good else VoteDir.DOWN
        return vote_reli_like if expected_vote_dir == vote.dir_ else vote_unreli_like


class BUser(User):
    """User with bayes model"""
    def __init__(self, id_: int):
        super().__init__(id_)
        self._reliability = UserReliability(name=f'user_{id_}')

    @property
    def reliability(self) -> float:
        return self._reliability.Mean()

    def update_reliability(self, new_vote: Vote, link_quality: float):
        """Update reliability with user vote and the voted link"""
        self._reliability.Update((new_vote, link_quality))

    @property
    def max_likelihood(self) -> float:
        return self._reliability.MaximumLikelihood()


class LinkQuality(Suite):
    """
    Link quality modeled by Bayes model.
    """
    def __init__(self, name: str):
        super().__init__(np.linspace(start=1 / 100, stop=1, num=100, dtype=float), name=name)

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

        Given hypothesis upvote probability is x
        hypo U likelihood: x
        hypo D likelihood: 1 - hypo U likelihood = 1 - x

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
        = x * (1 - reversibility) + (1 - x) * reversibility

        measured D likelihood
        = d2d likelihood + u2d likelihood
        = hypo D likelihood * (1 - reversibility) + hypo U likelihood * reversibility
        = (1 - x) * (1 - reversibility) + x * reversibility

        And it is easy to verify that, when reversibility is zero.
        measured U likelihood = x = hypo U likelihood
        measured D likelihood = 1 - x = hypo D likelihood
        """
        assert 0 <= reversibility <= 1.0

        x = hypo

        hypo_U_like = x
        hypo_D_like = 1 - x

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

    @property
    def max_likelihood(self) -> float:
        return self._l_quality.MaximumLikelihood()

    def pre_commit_update_quality(self):
        """Update quality with staged votes"""
        self._l_quality.UpdateSet(self._staged_votes)

    def post_commit_update_quality(self):
        pass
