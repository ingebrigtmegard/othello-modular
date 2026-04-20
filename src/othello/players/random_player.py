"""Random player implementation for testing."""

import random
from typing import List, Optional, Tuple

from .core.constants import PlayerColor
from .players.interfaces import IPlayer


class RandomPlayer(IPlayer):
    """
    Player that chooses a random valid move.

    Useful for testing engine stability and game flow.
    """

    def __init__(self, color: PlayerColor) -> None:
        """
        Initialize random player.

        Args:
            color: The color this player controls
        """
        super().__init__(color)

    def get_move(
        self, valid_moves: List[Tuple[int, int]], game_state: Optional[object] = None
    ) -> Tuple[int, int]:
        """
        Get a random valid move.

        Args:
            valid_moves: List of valid (row, col) coordinates
            game_state: Optional game state (not used)

        Returns:
            Tuple of (row, col) for the chosen move

        Raises:
            ValueError: If no valid moves are available
        """
        if not valid_moves:
            raise ValueError(f"{self.color} has no valid moves")

        return random.choice(valid_moves)
