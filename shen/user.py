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
    def __init__(self, name: str, discriminator: str = None, id: UUID = None):

        # the UUID of the user
        if id is None:
            id = uuid4()

        self.id: UUID = id
        # the name of the user
        self.name: str = name

        # the discriminator (4-digit identifier) of the user
        if discriminator is None:
            discriminator = gen_discriminator()

        self.discriminator: str = discriminator

    def __str__(self) -> str:
        return self.name + '#' + self.discriminator

    def __eq__(self, other) -> bool:
        if self.id == other.id:
            return True
        else:
            return self is other

    def __hash__(self):
        return hash(str(self.id))
