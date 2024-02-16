#!/usr/bin/env python3

"""
Reddit problem simple user / link object.
"""

from typing import Iterator

from .comm import VoteDir, Vote, User, Link


class SUser(User):
    """User with simple reliability model"""
    def __init__(self, id_: int):
        """A simple user"""
        super().__init__(id_)
        self._reliability = 0.5

    @property
    def reliability(self):
        return self._reliability

    @reliability.setter
    def reliability(self, v: float):
        assert 0 <= v <= 1.0
        self._reliability = v


class SLink(Link):
    """Simple Link with simple quality"""
    def __init__(self, id_: int):
        super().__init__(id_)
        self._quality = None

    @property
    def quality(self) -> float | None:
        """Quality of this link"""
        return self._quality

    @staticmethod
    def _do_update_quality(vote_it: Iterator[Vote]) -> float | None:
        """Update quality of this link according to all votes"""
        up_votes = 0
        down_votes = 0
        for vote in vote_it:
            if vote.dir_ == VoteDir.UP:
                up_votes += 1
            else:
                assert vote.dir_ == VoteDir.DOWN
                down_votes += 1

        tot_votes = up_votes + down_votes
        assert tot_votes >= 0
        if tot_votes == 0:
            # unable to determine the quality
            return None
        else:
            return up_votes / tot_votes

    def pre_commit_update_quality(self):
        pass

    def post_commit_update_quality(self):
        self._quality = self._do_update_quality(self._user_votes.values())