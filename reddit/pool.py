#!/usr/bin/env python3

"""Pool of user and link"""

from typing import Iterator, Callable
from dataclasses import dataclass

from .comm import User, Link, Vote, VoteDir


class UserPool:
    """All users"""
    def __init__(self, constr: Callable[[int], User]):
        self._constr = constr
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
            user = self._constr(id_)
            self._users[user.id_] = user
            return user


class LinkPool:
    """All linkes"""
    def __init__(self, constr: Callable[[int], Link]):
        self._constr = constr
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
            link = self._constr(id_)
            self._links[link.id_] = link
            return link


class ResourcePool:
    """Encapsulate all resource retrieval"""
    def __init__(self, user_constr: Callable[[int], User], link_constr: Callable[[int], Link]):
        self._user_pool = UserPool(user_constr)
        self._link_pool = LinkPool(link_constr)

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


_g_user_constr = None
_g_link_constr = None
_g_pool = None


def cfg_pool(user_constr: Callable[[int], User], link_constr: Callable[[int], Link]):
    """Config resource pool"""
    global _g_user_constr
    global _g_link_constr
    assert (_g_user_constr is None) and (_g_link_constr is None), 'Only allow config pool once'
    _g_user_constr = user_constr
    _g_link_constr = link_constr


def get_pool() -> ResourcePool:
    """Singleton ResourcePool"""
    global _g_pool
    assert (_g_user_constr is not None) and (_g_link_constr is not None), 'cfg_pool must be called before calling get_pool'
    if _g_pool is None:
        _g_pool = ResourcePool(_g_user_constr, _g_link_constr)

    return _g_pool
