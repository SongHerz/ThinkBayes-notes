#!/usr/bin/env python3

"""
Common classes for reddit problem.
"""

from dataclasses import dataclass

@dataclass(frozen=True)
class User:
    """Represent a redditor (a user)"""
    id_: int


@dataclass(frozen=True)
class Vote:
    """Represent a vote"""
    UP = 0
    DOWN = 1
    def __init__(self, user: User, vote: int):
        self.user = user
        self.vote = vote


class Link:
    """Represent a link"""
    def __init__(self, id_: int):
        self.id_ = id_
        # {user id: Vote}
        self.user_votes = {}

    def add_vote(self, vote: Vote):
        """Add a vote to this link"""
        self.user_votes[vote.user.id_] = vote


class UserPool:
    """All users"""
    def __init__(self):
        # {id: User}
        self._users = {}

    def get(self, id_: int) -> User:
        """Lazily retrieve an user"""
        if id_ in self._users:
            return self._users[id_]
        else:
            user = User(id_)
            self._users[user.id_] = user
            return user


class LinkPool:
    """All linkes"""
    def __init__(self):
        # {id: Link}
        self._links = {}

    def get(self, id_: int) -> Link:
        """Lazily retrieve a link"""
        if id_ in self._links:
            return self._links[id_]
        else:
            link = Link(id_)
            self._links[link.id_] = link
            return link
