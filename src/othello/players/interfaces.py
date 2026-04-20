"""Player interface definitions."""

from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from othello.core.constants import PlayerColor


class IPlayer(ABC):
    """
    Abstract base class for all player types.

    Players decide which move to make but cannot validate moves.
    Validation is handled by the OthelloEngine.
    """

    def __init__(self, color: PlayerColor) -> None:
        """
        Initialize player.

        Args:
            color: The color this player controls
        """
        self.color = color

    @abstractmethod
    def get_move(
        self, valid_moves: List[Tuple[int, int]], game_state: Optional[object] = None
    ) -> Tuple[int, int]:
        """
        Get the next move from the player.

        Args:
            valid_moves: List of valid (row, col) coordinates
            game_state: Optional game state object for AI decision making

        Returns:
            Tuple of (row, col) for the chosen move

        Raises:
            ValueError: If no valid moves are available
        """
        pass

    def get_color(self) -> PlayerColor:
        """
        Get the player's color.

        Returns:
            PlayerColor enum value
        """
        return self.color
