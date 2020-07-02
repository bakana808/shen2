
from __future__ import annotations
from typing import List, Type, TYPE_CHECKING

from shen.match import Match

if TYPE_CHECKING:
    from shen.user import User
    from shen.leaderboard import Leaderboard
    from shen.elo.ranker import RankingMethod


class Tournament:
    """
    Represents a tournament for a game.
    """

    def __init__(self, title: str, users: List[User]):
        """
        Create a tournament.

        Args:
            title (str):        the title of this tournament
            users (List[User]): the users in this tournament
        """

        self.title: str = title

        self.users: List[User] = users

        self.matches: List[Match] = []

    def create_match(self, users: List[User]):
        """
        Create a new match for a tournament

        Args:
            users (List[User]): the users in the match

        Raises:
            ValueError: if the users provided are not in the tournament

        Returns:
            Match: the match that was created
        """
        if not set(users).issubset(self.users):
            raise ValueError(
                "cannot create match with users not in this tournament"
            )
        match = Match(users)
        self.matches.append(match)
        return match

    def generate_leaderboards(self,
                              method_type: Type[RankingMethod]) -> Leaderboard:
        method: RankingMethod = method_type()
        return method.generate_leaderboards(self)
