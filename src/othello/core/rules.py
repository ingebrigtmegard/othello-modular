"""Rules validation and flipping logic module."""

from typing import List, Tuple

from .board import Board
from .constants import PlayerColor


class RulesValidator:
    """
    Handles all rule validation and disc flipping logic.

    Attributes:
        DIRECTIONS: 8 possible directions to check for flips.
    """

    DIRECTIONS: List[Tuple[int, int]] = [
        (-1, -1),
        (-1, 0),
        (-1, 1),  # Top row
        (0, -1),
        (0, 1),  # Middle row
        (1, -1),
        (1, 0),
        (1, 1),  # Bottom row
    ]

    def __init__(self) -> None:
        """Initialize the rules validator."""
        pass

    def calculate_flips(
        self, board: Board, row: int, col: int, player_color: PlayerColor
    ) -> List[Tuple[int, int]]:
        """
        Calculate all discs that would be flipped by placing at (row, col).

        Args:
            board: Current board state
            row: Target row
            col: Target column
            player_color: Color placing the disc

        Returns:
            List of (row, col) tuples for discs to flip
        """
        all_flips: List[Tuple[int, int]] = []
        opponent_color = (
            PlayerColor.WHITE
            if player_color == PlayerColor.BLACK
            else PlayerColor.BLACK
        )

        for dr, dc in self.DIRECTIONS:
            flips = self._get_flips_in_direction(
                board, row, col, dr, dc, player_color, opponent_color
            )
            all_flips.extend(flips)

        return all_flips

    def _get_flips_in_direction(
        self,
        board: Board,
        row: int,
        col: int,
        dr: int,
        dc: int,
        player_color: PlayerColor,
        opponent_color: PlayerColor,
    ) -> List[Tuple[int, int]]:
        """
        Get flips in a single direction.

        Args:
            board: Current board state
            row: Starting row
            col: Starting column
            dr: Direction row increment
            dc: Direction column increment
            player_color: Color placing the disc
            opponent_color: Opponent color

        Returns:
            List of (row, col) tuples for discs to flip in this direction
        """
        flips: List[Tuple[int, int]] = []
        r, c = row + dr, col + dc

        # Collect opponent discs
        while board.is_in_bounds(r, c) and board.get_cell(r, c) == opponent_color:
            flips.append((r, c))
            r += dr
            c += dc

        # Check if we hit our own color (valid bracket)
        if flips and board.is_in_bounds(r, c) and board.get_cell(r, c) == player_color:
            return flips

        return []

    def is_valid_move(
        self, board: Board, row: int, col: int, player_color: PlayerColor
    ) -> bool:
        """
        Check if placing a disc at (row, col) is a valid move.

        Args:
            board: Current board state
            row: Target row
            col: Target column
            player_color: Color attempting to move

        Returns:
            True if move is valid, False otherwise
        """
        if not board.is_in_bounds(row, col):
            return False
        if not board.is_empty(row, col):
            return False

        flips = self.calculate_flips(board, row, col, player_color)
        return len(flips) > 0

    def flip_discs(
        self, board: Board, row: int, col: int, player_color: PlayerColor
    ) -> List[Tuple[int, int]]:
        """
        Execute the flip operation on the board.

        Args:
            board: Board to modify
            row: Target row
            col: Target column
            player_color: Color placing the disc

        Returns:
            List of flipped disc positions
        """
        flips = self.calculate_flips(board, row, col, player_color)

        # Place the new disc
        board.set_cell(row, col, player_color)

        # Flip all opponent discs
        for r, c in flips:
            board.set_cell(r, c, player_color)

        return flips
