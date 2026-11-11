"""Registry of floor mechanics. Add a new mechanic module here to make it usable in any game."""
from .binary import Binary
from .cipher import Cipher
from .programs import Programs
from .sorting_ai import SortingAI
from .variables import Variables

REGISTRY = {m.name: m for m in (Programs(), Variables(), Binary(), Cipher(), SortingAI())}


def get(name):
    if name not in REGISTRY:
        raise KeyError(f"unknown mechanic {name!r}; known: {', '.join(REGISTRY)}")
    return REGISTRY[name]
