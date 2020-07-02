from typing import List, Optional
from dataclasses import dataclass, field
import time as _time

from shen.user import User


@dataclass
class Round:
    """A tournament round.

    A round contains the winners of the round and optionally any metadata about
    the round.
    """

    # a list of users that won this round
    winners: List[User]

    # optional round-related metadata i.e. map name, etc.
    meta: dict = field(default_factory=lambda: {})

    # optional user-related metadata i.e. characters, etc.
    user_meta: dict = field(default_factory=lambda: {})


@dataclass
class Match:
    """Represents a tournament match.

    A match keeps track of score per-user and optionally any metadata about the
    match (such as characters used or map chosen).
    """

    # the users in this match (required)
    users: List[User]

    # the max number of rounds in this match i.e. 1, 3, 5, etc.
    best_of: int = 3

    # the time this match took place
    time: float = _time.time()

    # a list of rounds in this match
    rounds: List[Round] = field(default_factory=lambda: [])

    def get_score(self, user: User) -> int:
        """Get the current score of a given user.

        For each round a user wins, the score increments by 1.
        """
        score = 0

        for rnd in self.rounds:
            if user in rnd.winners:
                score += 1

        return score

    def get_round(self, n: int) -> Round:
        return self.rounds[n]

    def get_winner(self) -> Optional[User]:
        """Gets the winner of the match, or the first winner if there are
        multiple winners.

        Returns:
            Optional[User]: the winner of the match
        """
        high_score = 0
        winner = None

        for user in self.users:
            score = self.get_score(user)
            if score > high_score:
                high_score = score
                winner = user

        return winner

    def get_all_winners(self) -> List[User]:
        """Gets all the winners of the match.

        Returns:
            Optional[List[User]]: [description]
        """
        high_score = 0
        winners = []

        # first find what the high score is
        for user in self.users:
            score = self.get_score(user)
            if score > high_score:
                high_score = score

        # then collect all users that have this score
        for user in self.users:
            if self.get_score(user) == high_score:
                winners.append(user)

        return winners

    def opponents_of(self, user: User) -> List[User]:
        """Gets all the opponents of a user in this match.

        Args:
            user (User): the user

        Returns:
            List[User]: the user's opponents
        """
        opponents = []

        for opponent in self.users:
            if user != opponent:
                opponents.append(opponent)

        return opponents

    def is_finished(self) -> bool:
        return self.get_winner() is not None
