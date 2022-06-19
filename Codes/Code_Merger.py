from enum import Enum, unique


@unique
class Code_Merger(Enum):
    BASE = 0
    TESTER = 1
    TWO_WAY = 2
    ADAPTIVE_VIRTUAL = 3
    ADAPTIVE_REAL = 4
