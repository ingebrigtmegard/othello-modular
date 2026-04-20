"""Board state management module."""

from typing import List

from .core.constants import BoardSize, PlayerColor


class Board:
    """
    Represents the 8x8 Othello game board.

    Attributes:
        grid: 2D array representing board state.
    """

    def __init__(self) -> None:
        """Initialize empty 8x8 board with center discs."""
        self.grid: List[List[PlayerColor]] = [
            [PlayerColor.EMPTY for _ in range(BoardSize.COLS)]
            for _ in range(BoardSize.ROWS)
        ]
        self._setup_center()

    def _setup_center(self) -> None:
        """Set up the four center discs."""
        # Black at (3,3) and (4,4)
        # White at (3,4) and (4,3)
        self.grid[3][3] = PlayerColor.BLACK
        self.grid[4][4] = PlayerColor.BLACK
        self.grid[3][4] = PlayerColor.WHITE
        self.grid[4][3] = PlayerColor.WHITE

    def get_cell(self, row: int, col: int) -> PlayerColor:
        """
        Get the color of a cell.

        Args:
            row: Row index (0-7)
            col: Column index (0-7)

        Returns:
            PlayerColor of the cell
        """
        return self.grid[row][col]

    def set_cell(self, row: int, col: int, color: PlayerColor) -> None:
        """
        Set the color of a cell.

        Args:
            row: Row index (0-7)
            col: Column index (0-7)
            color: PlayerColor to set
        """
        self.grid[row][col] = color

    def is_empty(self, row: int, col: int) -> bool:
        """Check if a cell is empty."""
        return self.grid[row][col] == PlayerColor.EMPTY

    def is_in_bounds(self, row: int, col: int) -> bool:
        """Check if coordinates are within board boundaries."""
        return 0 <= row < BoardSize.ROWS and 0 <= col < BoardSize.COLS

    def copy(self) -> "Board":
        """Create and return a deep copy of the board."""
        new_board = Board.__new__(Board)
        new_board.grid = [row[:] for row in self.grid]
        return new_board

    def to_list(self) -> List[List[int]]:
        """Convert board to list of lists with integer values."""
        return [[cell.value for cell in row] for row in self.grid]
