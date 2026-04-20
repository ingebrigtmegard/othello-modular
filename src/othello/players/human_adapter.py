"""Human player adapter for GUI integration."""

from typing import List, Optional, Tuple

from othello.core.constants import PlayerColor
from .interfaces import IPlayer


class HumanPlayerAdapter(IPlayer):
    """
    Adapter for human players using GUI input.

    This class doesn\'t actually get moves itself. It waits for
    the GUI to provide moves through the controller.
    """

    def __init__(self, color: PlayerColor) -> None:
        """
        Initialize human player adapter.

        Args:
            color: The color this player controls
        """
        super().__init__(color)
        self.pending_move: Optional[Tuple[int, int]] = None

    def set_move(self, move: Tuple[int, int]) -> None:
        """
        Set the move from GUI input.

        Args:
            move: (row, col) tuple from GUI click
        """
        self.pending_move = move

    def get_move(
        self, valid_moves: List[Tuple[int, int]], game_state: Optional[object] = None
    ) -> Tuple[int, int]:
        """
        Get the pending move from GUI.

        Args:
            valid_moves: List of valid (row, col) coordinates
            game_state: Optional game state (not used)

        Returns:
            Tuple of (row, col) for the chosen move

        Raises:
            ValueError: If no move has been set by GUI
        """
        if self.pending_move is None:
            raise ValueError("No move has been provided by GUI")

        if self.pending_move not in valid_moves:
            raise ValueError(f"Move {self.pending_move} is not valid")

        return self.pending_move
