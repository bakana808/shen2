"""
User
====

A user contains a UUID as an identifier as well as a
username and discriminator (a 4-digit number).

The form "<username>#<discriminator>" acts as a human-readable alias
for the UUID.

### Limitations

- The discriminator can only be a 4-digit number (ranging from 0000 to 9999).
- The username is case-insensitive and can only contain letters, underscore, and dash.

### Nickname

The _nickname_ is an optional name for this user to display
instead of the username. There are no limitations to the nickname.

### Connections

A user may also contain additional data, like their Discord ID.
This will allow a Discord user with the ID to act on
behalf of this user.
"""

import random
from uuid import UUID, uuid4


def gen_discriminator() -> str:
    """
    Generate a 4-digit discriminator.

    Returns:
        str: the discriminator that was generated
    """
    return '{:04d}'.format(random.randint(0, 9999))


def gen_uuid() -> UUID:
    return uuid4()


class User:
    def __init__(self,
                 username: str,
                 discriminator: str = None,
                 uuid: UUID = None,
                 nickname: str = None):

        # the name of the user
        self.username: str = username

        # the UUID of the user
        self.uuid = uuid or uuid4()

        # the discriminator (4-digit identifier) of the user
        self.discriminator: str = discriminator or gen_discriminator()

        self.nickname: str = nickname or username

    def get_tag(self) -> str:
        return self.username + '#' + self.discriminator

    def __str__(self) -> str:
        return f"({self.uuid}) {self.get_tag()}"

    def __eq__(self, other) -> bool:
        if self.uuid == other.uuid:
            return True
        else:
            return self is other

    def __hash__(self):
        return hash(str(self.uuid))
