
from __future__ import annotations
from typing import List, Type, Dict, TYPE_CHECKING
from operator import attrgetter

if TYPE_CHECKING:
    from shen.tournament import Tournament
    from shen.user import User
    from shen.elo.ranker import Stats


class Leaderboard:
    """
    Represents the leaderboard of a tournament at a given moment in time.
    """

    def __init__(self, tournament: Tournament, stat_list: List[Stats]):

        # the tournament that this leaderboard is of
        self._tournament: Tournament = tournament

        self._stat_list: List[Stats] = stat_list

    def get_by_place(self, n) -> Stats:
        return self._stat_list[n]
