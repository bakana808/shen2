from __future__ import annotations
import copy as _copy
import math
from typing import Dict, List
from operator import attrgetter

from shen.elo import Elo
from shen.match import Match
from shen.leaderboard import Leaderboard
from shen.tournament import Tournament
from shen.user import User


class Stats:
    def __init__(self, user: User, **meta):

        # the user these stats belong to
        self.user: User = user

        # the amount of matches played and the amount won
        self.match_count: int = 0

        self.win_count: int = 0

        # any metainfo
        self.meta: dict = meta

    def copy(self) -> Stats:
        return _copy.copy(self)


class RankingMethod:
    def __init__(self):

        self.elo: Elo = Elo()

    def generate_leaderboards(self, tournament: Tournament) -> Leaderboard:
        """
        Generate a leaderboard

        Args:
            tournament (Tournament): the tournament to generate a
                                     leaderboard for
        """
        stats_dict: Dict[User, Stats] = {}

        print('starting leaderboard generation...')
        print(f'(using ${ len(tournament.matches) } matches)')

        for match in tournament.matches:

            for user in match.users:
                stats = stats_dict.get(user, self.on_init_stats(user))

            new_stats_dict = {}
            for user in match.users:

                new_stats_dict[user] = self.on_process_stats(
                    stats_dict, stats, match)

            # merge the modified stats with the originals
            stats_dict = {**stats_dict, **new_stats_dict}

        stats_list = self.on_sort_stats(list(stats_dict.values()))
        return Leaderboard(tournament, stats_list)

    def on_init_stats(self, user: User) -> Stats:
        """
        Initialize a user's statistics.

        Args:
            user (User): the user

        Returns:
            Stats: a newly created Stats object
        """
        return Stats(user, rating=1000)

    def on_process_stats(self, stats_dict: Dict[User, Stats], stats: Stats,
                         match: Match) -> Stats:
        """
        Process a user's statistics based on a match they played.
        This method should return an updated version of the stats given.

        Args:
            stats (Stats): the statistics of a user in the match
            match (Match): the match that was played

        Returns:
            Stats: an updated version of the statistics given
        """
        user: User = stats.user
        stats = stats.copy()

        stats.match_count += 1
        if match.winner == user:
            stats.win_count += 1
            score = 1
        else:
            score = 0

        for opponent in match.opponents_of(stats.user):
            o_stats = stats_dict.get(opponent, self.on_init_stats(user))

        adjustment = math.ceil(
            self.elo.get_adjustment(stats.meta['rating'],
                                    o_stats.meta['rating'], score))

        stats.meta['rating'] += adjustment

        return stats

    def on_sort_stats(self, stat_list: List[Stats]) -> List[Stats]:
        """
        Sort a list of Stats objects by leaderboard placement.
        The order of the list returned should be the same as they appear on a
        leaderboard.

        Args:
            stat_list (List[Stats]): an unordered list

        Returns:
            List[Stats]: an ordered list
        """
        stat_list = sorted(stat_list,
                           key=lambda stats:
                           (stats.win_count / stats.match_count),
                           reverse=True)
        stat_list = sorted(stat_list,
                           key=lambda stats: stats.meta['rating'],
                           reverse=True)

        return stat_list
