#!/usr/bin/env python3

"""
Common classes for reddit problem.
"""

from typing import Iterator
from enum import Enum, auto
from abc import ABC, abstractmethod


class User(ABC):
    """Represent an user"""
    def __init__(self, id_: int):
        """Represent a redditor (a user)"""
        self.id_ = id_

    @property
    @abstractmethod
    def reliability(self):
        """Return reliability value (0 ~ 1)"""
        raise NotImplementedError('Child class must implement this')

    @property
    def reversibility(self):
        """Reversibility"""
        return 1.0 - self.reliability


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
        # [Vote]
        self._staged_votes = []
        # {user id: Vote}
        self._user_votes = {}

    def add_vote(self, vote: Vote):
        """Add a vote to this link"""
        self._staged_votes.append(vote)

    @abstractmethod
    def pre_commit_update_quality(self):
        """Method used to update link quality before committing votes.
        This method is called inside commit_vote.
        """
        raise NotImplementedError('Child class must implement this')

    @abstractmethod
    def post_commit_update_quality(self):
        """Method used to update link quality after committing votes.
        This method is called inside commit_vote.
        """
        raise NotImplementedError('Child class must implement this')

    def commit_vote(self):
        """Commit staged votes"""
        self.pre_commit_update_quality()

        for v in self._staged_votes:
            self._user_votes[v.user.id_] = v

        self._staged_votes.clear()

        self.post_commit_update_quality()

    @property
    def votes(self) -> Iterator[Vote]:
        """Return an iterator on votes of this link"""
        return self._user_votes.values()

    def get_vote(self, u: User) -> Vote | None:
        """Return a vote by given user"""
        return self._user_votes.get(u.id_, None)

    @property
    @abstractmethod
    def quality(self) -> float | None:
        """Quality of this link"""
        raise NotImplementedError('Child class must implement this')

