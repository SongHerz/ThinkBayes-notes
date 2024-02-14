#!/usr/bin/env python3

"""
Common classes for reddit problem.
"""

from typing import Iterator
from enum import Enum, auto
from abc import ABC, abstractmethod, abstractproperty


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


class Link(ABC):
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

    @abstractproperty
    def quality(self) -> float | None:
        """Quality of this link"""
        raise NotImplementedError('Child class must implement this')

    @abstractmethod
    def update_quality(self):
        """Update quality of this link"""
        raise NotImplementedError('Child class must implement this')
