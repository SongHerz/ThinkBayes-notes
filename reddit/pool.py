#!/usr/bin/env python3

"""Pool of user and link"""

from typing import Iterator
from dataclasses import dataclass

from .comm import User, Link, Vote, VoteDir


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

    @property
    def links(self) -> Iterator[Link]:
        """Return an iterator on all links"""
        return self._link_pool.links

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


_g_pool = ResourcePool()

def get_pool() -> ResourcePool:
    """Singleton ResourcePool"""
    return _g_pool