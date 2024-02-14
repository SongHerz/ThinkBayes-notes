#!/usr/bin/env python3

"""
Common classes for reddit problem.
"""

from typing import Iterator
from enum import Enum, auto


class User:
    """Represent an user"""
    def __init__(self, id_: int):
        """Represent a redditor (a user)"""
        self.id_ = id_
        # Reliability 0 ~ 1
        self.reliability = 0.5

    @property
    def reliability(self):
        """Return reliability value"""
        return self._reliability

    @reliability.setter
    def reliability(self, v: float):
        assert 0 <= v <= 1.0
        self._reliability = v


class VoteDir(Enum):
    """Vote directions"""
    UP = auto()
    DOWN = auto()


class Vote:
    """Represent a vote"""
    def __init__(self, user: User, dir_: VoteDir):
        self.user = user
        self.dir_ = dir_


class Link:
    """Represent a link"""
    def __init__(self, id_: int):
        self.id_ = id_
        # {user id: Vote}
        self.user_votes = {}
        self._quality = None

    def add_vote(self, vote: Vote):
        """Add a vote to this link"""
        self.user_votes[vote.user.id_] = vote

    @property
    def votes(self) -> Iterator[Vote]:
        """Return an iterator on votes of this link"""
        return self.user_votes.values()

    def get_vote(self, u: User) -> Vote | None:
        """Return a vote by given user"""
        return self.user_votes.get(u.id_, None)

    @property
    def quality(self) -> float | None:
        """Quality of this link"""
        return self._quality

    def update_quality(self):
        """Update quality of this link according to all votes"""
        up_votes = 0
        down_votes = 0
        for vote in self.user_votes.values():
            if vote.dir_ == VoteDir.UP:
                up_votes += 1
            else:
                assert vote.dir_ == VoteDir.DOWN
                down_votes += 1

        tot_votes = up_votes + down_votes
        assert tot_votes >= 0
        if tot_votes == 0:
            # unable to determine the quality
            self._quality = None
        else:
            self._quality = up_votes / tot_votes





