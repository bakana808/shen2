import math


class Elo:
    def __init__(self, floor: float = 0, k: float = 40):
        """In the Elo rating system, the k-factor `k` determines how much a
        player's skill rating can change with each win or loss.

        Args:
            floor (float, optional): the lowest skill rating a player can have.
                                     Defaults to 0.
            k (float, optional): the k-factor to use.
                                 Defaults to 40.
        """
        self.floor = floor
        self.k = k

    def get_expected_score(self, a_or_diff: float, b: float = None):
        """Calculates the expected score of a player with rating `a` based on
        the rating difference between that player and an opponent with
        rating `b`.

        The expected score is a number between 0 - 1 inclusive. If the rating
        difference between both players are 0, then the expected score will
        be 0.5.

        Args:
            a (float): the rating of the player
            b (float): the rating of the opponent
        """
        if b is None:
            diff = a_or_diff
        else:
            diff = b - a_or_diff

        return 1 / (1 + math.pow(10, diff / 400))

    def get_adjustment(self, a: float, b: float, score: float):
        """Calculates the rating adjustment using a player's rating `a`,
        an opponent's rating `b`, and `score`, which is a number between 0 and
        1.

        Adding this adjustment to the player's initial rating will give the
        player's new rating.

        Args:
            a (float): [description]
            b (float): [description]
            score (float): [description]
        """
        expected_score = self.get_expected_score(a, b)
        return round(self.k * (score - expected_score))
