from typing import List, Optional, Tuple, Dict, TYPE_CHECKING
from dataclasses import dataclass, field
import time as _time

from shen.player import Player

if TYPE_CHECKING:
    from shen.user import User
    from shen.tournament import Tournament


@dataclass
class Round:
    """A tournament round.

    A round contains the winners of the round and optionally any metadata about
    the round.
    """

    # a list of players that won this round
    winners: List[Player]

    # optional round-related metadata i.e. map name, etc.
    meta: dict = field(default_factory=lambda: {})

    # optional player-related metadata i.e. characters, etc.
    player_meta: dict = field(default_factory=lambda: {})


@dataclass
class Match:
    """Represents a tournament match.

    A match keeps track of score per-player and optionally any metadata about the
    match (such as characters used or map chosen).
    """

    tny: "Tournament"

    # the players in this match (required)
    players: List[Player]

    # the max number of rounds in this match i.e. 1, 3, 5, etc.
    best_of: int = 3

    # the time this match took place
    time: float = _time.time()

    # a list of rounds in this match
    rounds: List[Round] = field(default_factory=lambda: [])

    def record_win(self, *winners: "User") -> Round:
        """Record that a player has won the match."""

        players = [self.tny._player(user) for user in winners]

        # initialize player meta
        player_meta: Dict[Player, dict] = {}
        for player in self.players:
            player_meta[player] = {}

        rnd = Round(players, player_meta=player_meta)
        self.rounds.append(rnd)
        return rnd

    def get_score(self, player: Player) -> int:
        """Get the current score of a given player.

        For each round a player wins, the score increments by 1.
        """
        score = 0

        for rnd in self.rounds:
            # print(rnd.winners)
            if player in rnd.winners:
                score += 1

        return score

    def get_round(self, n: int) -> Round:
        return self.rounds[n]

    def get_winner(self) -> Optional[Player]:
        """Gets the winner of the match, or the first winner if there are
        multiple winners.

        Returns:
            Optional[Player]: the winner of the match
        """
        high_score = 0
        winner = None

        for player in self.players:
            score = self.get_score(player)
            if score > high_score:
                high_score = score
                winner = player

        return winner

    def get_all_winners(self) -> List[Player]:
        """Gets all the winners of the match.

        Returns:
            Optional[List[Player]]: [description]
        """
        high_score = 0
        winners = []

        # first find what the high score is
        for player in self.players:
            score = self.get_score(player)
            if score > high_score:
                high_score = score

        # then collect all players that have this score
        for player in self.players:
            if self.get_score(player) == high_score:
                winners.append(player)

        return winners

    def opponents_of(self, player: Player) -> List[Player]:
        """Gets all the opponents of a player in this match.

        Args:
            player (Player): the player

        Returns:
            List[Player]: the player's opponents
        """
        opponents = []

        for opponent in self.players:
            if player != opponent:
                opponents.append(opponent)

        return opponents

    def get_opponent(self, player: Player) -> Player:
        return self.opponents_of(player)[0]

    def is_finished(self) -> bool:
        return self.get_winner() is not None
