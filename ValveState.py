from enum import Enum


class ValveState(Enum):
    standing = 0
    open = 1
    close = 2
    uncertain = 3