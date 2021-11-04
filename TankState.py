from enum import Enum


class TankState(Enum):
    standing = 0
    exporting = 1
    importing = 2
    uncertain = 3


if __name__ == '__main__':
    print(TankState.standing.value == 0)