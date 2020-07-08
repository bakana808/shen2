from typing import Optional, TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from shen.user import User
    from shen.tournament import Tournament


@dataclass
class Player:

    user: "User"
    tournament: "Tournament"
    nickname: Optional[str] = None

    def __post_init__(self):
        self.nickname = self.nickname or self.user.get_tag()

    def __eq__(self, other) -> bool:
        return other and self.tournament == other.tournament and self.user == other.user

    def __hash__(self):
        return hash(self.user)

    def __str__(self):
        return self.nickname
