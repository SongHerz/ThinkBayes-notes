#!/usr/bin/env python3

"""
Common classes for reddit problem.
"""

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


class ResourcePool:
    """Encapsulate all resource retrieval"""
    def __init__(self):
        self._user_pool = UserPool()
        self._link_pool = LinkPool()

    def get_user(self, id_: int) -> User:
        """Get User object with given user id"""
        return self._user_pool.get(id_)

    def get_link(self, id_: int) -> Link:
        """Get Link object with given link id"""
        return self._link_pool.get(id_)