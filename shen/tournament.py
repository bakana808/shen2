from __future__ import annotations
from typing import List, Type, TYPE_CHECKING

from shen.match import Match
from shen.player import Player

if TYPE_CHECKING:
    from shen import Shen
    from shen.user import User
    from shen.leaderboard import Leaderboard
    from shen.elo.ranker import RankingMethod


class Tournament:
    """
    Represents a tournament for a game.
    """
    def __init__(self, shn: "Shen", title: str, users: List[User] = []):
        """
        Create a tournament.

        Args:
            title (str):        the title of this tournament
            users (List[User]): the users in this tournament
        """

        self.shn: Shen = shn

        self.title: str = title

        self.players: List[Player] = []

        self.matches: List[Match] = []

        for user in users:
            self.add_user(user)

    def _player(self, user: User):
        try:
            return next(player for player in self.players
                        if player.user == user)
        except IndexError:
            raise ValueError(f"the user {user} is not in this tournament")

    def add_user(self, user: User, nickname=None):
        self.players.append(Player(user, self, nickname))

    def start_match(self, users: List[User], best_of=3) -> Match:
        """
        Create a new match for a tournament

        Args:
            users (List[User]): the users in the match

        Raises:
            ValueError: if the users provided are not in the tournament

        Returns:
            Match: the match that was created
        """
        players = [self._player(user) for user in users]

        match = Match(self, players, best_of=best_of)
        self.matches.append(match)
        return match

    def generate_leaderboards(self,
                              method_type: Type[RankingMethod]) -> Leaderboard:
        method: RankingMethod = method_type()
        return method.generate_leaderboards(self)
