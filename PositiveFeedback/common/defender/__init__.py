from .badacts import BadActsDefender
from .onion import ONIONDefender
from .strip import STRIPDefender
from .cube import CUBEDefender
from .bki import BKIDefender
from .fp import FPDefender


def selectDefender(name):
    defender_map = {
        "badacts": BadActsDefender,
        "onion": ONIONDefender,
        "strip": STRIPDefender,
        "cube": CUBEDefender,
        "bki": BKIDefender,
        "fp": FPDefender
    }
    return defender_map[name]
