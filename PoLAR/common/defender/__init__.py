from .badacts import BadActsDefender
from .onion import ONIONDefender
from .strip import STRIPDefender
from .cube import CUBEDefender
from .bki import BKIDefender
from .polar import PoLARDefender


def selectDefender(name):
    defender_map = {
        "badacts": BadActsDefender,
        "onion": ONIONDefender,
        "strip": STRIPDefender,
        "cube": CUBEDefender,
        "bki": BKIDefender,
        "polar": PoLARDefender
    }
    return defender_map[name]
