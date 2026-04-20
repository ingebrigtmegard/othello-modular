"""Game constants for Othello."""

from enum import Enum


class PlayerColor(Enum):
    """Player colors enumeration."""

    EMPTY = 0
    BLACK = 1
    WHITE = 2


class BoardSize:
    """Board dimensions."""

    ROWS = 8
    COLS = 8
