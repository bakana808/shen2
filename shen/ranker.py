"""
Ranker
======

The ranker reads a list of matches and calculates the rankings of the players.

* * *

Ranking Algorithm
-----------------

Players can be ranked using different algorithms.

### Elo Rating

When using the Elo rating system, players have a "skill rating" - a number
that represents how skilled they are.

A "k-factor" (40 by default) is also used to determine the "weight" of
each match. A higher k-factor means that each match will more drastically
change each player's rating.

The initial skill rating of every player is 1500.

Every match will adjust the rating of each player involved according to
match score.

Players are then ranked in order according to their skill rating.

### Challenge Ranking

All players start off with a initial random place on the rankings.

At the result of each match, if the loser was ranked higher than the winner,
the winner will switch ranks with the loser.

If a player is inactive for too long, their rank will "decay" and they will
switch ranks with the player below them.
"""

import math
from dataclasses import dataclass
from typing import List
from shen import Shen, _i, _w, _e
from shen.user import User
from shen.player import Player
from shen.match import Match
from shen.elo import Elo
from shen.tournament import Tournament


class RankingAlgo:
    def __init__(self, name: str):

        # the name of the algorithm
        self.name: str = name

    def start(self, tny: Tournament):
        """Starts the algorithm."""

        _i("Starting Ranking Algorithm...")
        _i("-" * 80)
        _i(f"tournament: {tny.title}")
        _i(f"    method: {self.name}")
        _i(f" # players: {len(tny.players)}")
        _i(f" # matches: {len(tny.matches)}")
        _i("-" * 80)

        self.on_start(tny)

        for match in tny.matches:
            self.on_match(match)

        self.on_finish(tny)

    def on_start(self, tny: Tournament):
        """Called at the beginning of the algorithm."""
        pass

    def on_match(self, match: Match):
        """Called at every match."""
        pass

    def on_finish(self, tny: Tournament):
        """Called after all matches have been processed."""
        pass


class EloRankingAlgo(RankingAlgo):
    def __init__(self):

        RankingAlgo.__init__(self, "Elo Ranking System")

        self.elo: Elo = Elo()

    def on_start(self, tny: Tournament):

        self.stats_dict = {}

        # initialize all player's stats
        _i("initializing all players stats...")

        for player in tny.players:
            self.stats_dict[player.user.uuid] = {"rating": 1500, "matches": 0}

    def process_match(self, match: Match, player: Player):

        # get stats of this player
        stats = self.stats_dict.get(player.user.uuid, None)

        # get score of this player
        score = 0
        # _i(f"check: {match.get_winner()} == {player}")
        if match.get_winner() == player:
            score = 1

        # get skill rating of opponent
        for opponent in match.opponents_of(player):
            opp_stats = self.stats_dict.get(opponent.user.uuid, None)
            if not opp_stats:
                _w("cannot find player.user: {opponent} !")

        # calculate skill rating adjustment
        adj = math.ceil(
            self.elo.get_adjustment(stats["rating"], opp_stats["rating"],
                                    score))

        # _i(f"{player} => score={score} adj={adj}")

        return adj

    def on_match(self, match: Match):

        adj_stats = {}

        for player in match.players:
            adj = self.process_match(match, player)
            adj_stats[player.user.uuid] = {
                "rating": self.stats_dict[player.user.uuid]["rating"] + adj,
                "matches": self.stats_dict[player.user.uuid]["matches"] + 1
            }

        # merge adjusted stats with originals
        self.stats_dict = {**self.stats_dict, **adj_stats}

    def on_finish(self, tny: Tournament):

        _i("finished reading matches.")

        # sort stats
        stats_list = [(k, v) for k, v in self.stats_dict.items()]
        stats_list = sorted(stats_list,
                            key=lambda stats: stats[1]["rating"],
                            reverse=True)

        # filter out players with 0 matches
        no_matches = [i for i in stats_list if i[1]["matches"] == 0]
        stats_list = [i for i in stats_list if i[1]["matches"] > 0]

        place = 1
        for v in stats_list:
            _i(f"{place}: {tny._player(tny.shn.user(v[0]))} ({v[1]['rating']})"
               )
            place += 1

        _i(f"players w/ no matches:")

        for v in no_matches:
            _i(f"{tny.shn.user(v[0])}")
