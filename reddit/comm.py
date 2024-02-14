#!/usr/bin/env python3

"""
Common classes for reddit problem.
"""

from typing import Iterator
from enum import Enum, auto
from dataclasses import dataclass

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

    @property
    def quality(self) -> float | None:
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


class UserPool:
    """All users"""
    def __init__(self):
        # {id: User}
        self._users = {}

    @property
    def users(self) -> Iterator[User]:
        """Return an iterator on all users"""
        return self._users.values()

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

    @property
    def links(self) -> Iterator[Link]:
        """Return an iterator on all links"""
        return self._links.values()

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

    @dataclass(frozen=True)
    class LinkVote:
        """Combination of (a link that an user has voted, the vote)"""
        link: Link
        vote: Vote

    def _print_user_summary(self):
        # {user id: LinkVote}
        uid_lv_map = {}
        for link in self._link_pool.links:
            for vote in link.votes:
                uid = vote.user.id_
                if uid not in uid_lv_map:
                    uid_lv_map[uid] = []

                uid_lv_map[uid].append(self.LinkVote(link=link, vote=vote))

        for user in self._user_pool.users:
            uid = user.id_
            lvs = uid_lv_map.get(uid, [])
            print(f'User: {uid}, votes: {len(lvs)}, reliability: {user.reliability}')

    def _print_link_summary(self):
        links = sorted(self._link_pool.links, key=lambda link: link.id_)

        for link in links:
            upvotes = []
            downvotes = []
            for vote in link.votes:
                if vote.dir_ == VoteDir.UP:
                    upvotes.append(vote)
                else:
                    assert vote.dir_ == VoteDir.DOWN
                    downvotes.append(vote)

            print(f'Link: {link.id_}, up: {len(upvotes)}, down: {len(downvotes)}, quality: {link.quality}')

    def print_summary(self):
        """Show summary by users and links"""
        print('##############')
        print(' User Summary')
        print('##############')
        self._print_user_summary()
        print()
        print('##############')
        print(' Link Summary')
        print('##############')
        self._print_link_summary()
