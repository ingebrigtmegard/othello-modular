"""AI player implementation with basic heuristics."""

from typing import List, Optional, Tuple

from othello.core.constants import PlayerColor
from .interfaces import IPlayer


class AiPlayer(IPlayer):
    """
    AI player using heuristic evaluation.

    Priority:
    1. Corner positions (most valuable)
    2. Edge positions (stable)
    3. Avoid X and C squares (adjacent to corners)
    4. Random remaining moves
    """

    # Weight for different board positions
    CORNER_WEIGHT = 10
    EDGE_WEIGHT = 5
    X_SQUARE_WEIGHT = -5  # Bad squares adjacent to corners
    C_SQUARE_WEIGHT = -3  # Slightly bad squares
    NORMAL_WEIGHT = 1

    def __init__(self, color: PlayerColor, difficulty: str = "medium") -> None:
        """
        Initialize AI player.

        Args:
            color: The color this player controls
            difficulty: "easy", "medium", or "hard" (not fully implemented)
        """
        super().__init__(color)
        self.difficulty = difficulty
        self._setup_position_weights()

    def _setup_position_weights(self) -> None:
        """Set up position weight map for board evaluation."""
        self.position_weights: List[List[int]] = [[0] * 8 for _ in range(8)]

        # Corners
        corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
        for r, c in corners:
            self.position_weights[r][c] = self.CORNER_WEIGHT

        # Edges (non-corner)
        for r in range(8):
            for c in range(8):
                if (r == 0 or r == 7 or c == 0 or c == 7) and (r, c) not in corners:
                    self.position_weights[r][c] = self.EDGE_WEIGHT

        # X squares (diagonally adjacent to corners)
        x_squares = [(1, 1), (1, 6), (6, 1), (6, 6)]
        for r, c in x_squares:
            self.position_weights[r][c] = self.X_SQUARE_WEIGHT

        # C squares (orthogonally adjacent to corners)
        c_squares = [(0, 1), (0, 6), (1, 0), (1, 7), (6, 0), (6, 7), (7, 1), (7, 6)]
        for r, c in c_squares:
            self.position_weights[r][c] = self.C_SQUARE_WEIGHT

    def _evaluate_move(self, move: Tuple[int, int]) -> int:
        """
        Evaluate a move based on position weights.

        Args:
            move: (row, col) tuple

        Returns:
            Score for this move
        """
        r, c = move
        return self.position_weights[r][c]

    def get_move(
        self, valid_moves: List[Tuple[int, int]], game_state: Optional[object] = None
    ) -> Tuple[int, int]:
        """
        Get the best move based on heuristics.

        Args:
            valid_moves: List of valid (row, col) coordinates
            game_state: Optional game state (not used in basic AI)

        Returns:
            Tuple of (row, col) for the chosen move

        Raises:
            ValueError: If no valid moves are available
        """
        if not valid_moves:
            raise ValueError(f"{self.color} has no valid moves")

        # Score all valid moves
        scored_moves = [(self._evaluate_move(move), move) for move in valid_moves]

        # Sort by score (descending)
        scored_moves.sort(key=lambda x: x[0], reverse=True)

        # Return the best move
        return scored_moves[0][1]
