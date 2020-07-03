#!/usr/bin/python3

from typing import Optional, List, Dict, Any

from shen.user import User
from shen.tournament import Tournament
from shen.match import Match


def _i(msg: str):
    print(f"[I] {msg}")


def _w(msg: str):
    print(f"[W] {msg}")


def _e(msg: str):
    print(f"[E] {msg}")


class Shen:
    def __init__(self):

        # the users in this session
        self.users: Dict[Any, User] = {}

        # the matches in this session (in order)
        # TODO: move to tournament class
        self.matches: List[Match] = []

    def create_user(self, name: str) -> User:
        """
        Create a new user.

        Args:
            name (str): the name of the user

        Returns:
            User: the user created
        """
        user = User(name)
        self.users[user.uuid] = user
        return user

    def add_user(self, user: User):
        self.users[user.uuid] = user

    def user(self, uuid_or_user) -> User:
        """
        Get a user by their UUID.

        Args:
            uuid: the UUID of the user

        Returns:
            User: the user
        """
        if isinstance(uuid_or_user, User):
            return uuid_or_user
        else:
            return self.users[uuid_or_user]

    def add_match(self, match: Match):
        self.matches.append(match)

    def start_match(self, users: List[User], best_of=3) -> Match:
        """
        Start a new match.
        """
        match = Match(users, best_of=best_of)
        self.add_match(match)
        return match

    def create_tournament(self, title: str, users: List[User]) -> Tournament:
        """
        Create a Tournament.

        Args:
            title (str): the title of the tournament
            users (List[User]): the users in the tournament

        Returns:
            Tournament: the tournament created
        """
        return Tournament(title, users)


def init() -> "Shen":
    return Shen()

