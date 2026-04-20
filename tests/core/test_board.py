"""Tests for Board state management."""

from othello.core.board import Board
from othello.core.constants import PlayerColor


class TestBoard:
    def setup_method(self):
        """Create a fresh board before each test."""
        self.board = Board()

    def test_initial_board_not_completely_empty(self):
        """Test that board has 4 center discs (not completely empty)."""
        # Count total non-empty cells
        non_empty_count = 0
        for r in range(8):
            for c in range(8):
                if not self.board.is_empty(r, c):
                    non_empty_count += 1
        assert non_empty_count == 4

    def test_initial_center_setup(self):
        """Test that center 4 discs are set correctly."""
        # Black: (3,3) and (4,4)
        # White: (3,4) and (4,3)
        assert self.board.get_cell(3, 3) == PlayerColor.BLACK
        assert self.board.get_cell(4, 4) == PlayerColor.BLACK
        assert self.board.get_cell(3, 4) == PlayerColor.WHITE
        assert self.board.get_cell(4, 3) == PlayerColor.WHITE

    def test_initial_board_corners_empty(self):
        """Test that corner cells are empty initially."""
        assert self.board.is_empty(0, 0)
        assert self.board.is_empty(0, 7)
        assert self.board.is_empty(7, 0)
        assert self.board.is_empty(7, 7)

    def test_initial_board_edges_empty(self):
        """Test that edge cells (non-center) are empty initially."""
        # Top edge (excluding center area)
        assert self.board.is_empty(0, 3)
        assert self.board.is_empty(0, 4)
        # Bottom edge
        assert self.board.is_empty(7, 3)
        assert self.board.is_empty(7, 4)
        # Left edge
        assert self.board.is_empty(3, 0)
        assert self.board.is_empty(4, 0)
        # Right edge
        assert self.board.is_empty(3, 7)
        assert self.board.is_empty(4, 7)

    def test_set_cell(self):
        """Test setting a cell value."""
        self.board.set_cell(0, 0, PlayerColor.BLACK)
        assert self.board.get_cell(0, 0) == PlayerColor.BLACK

    def test_board_copy(self):
        """Test that board copy creates independent copy."""
        self.board.set_cell(0, 0, PlayerColor.BLACK)
        board_copy = self.board.copy()
        board_copy.set_cell(0, 0, PlayerColor.WHITE)
        assert self.board.get_cell(0, 0) == PlayerColor.BLACK
        assert board_copy.get_cell(0, 0) == PlayerColor.WHITE

    def test_is_empty(self):
        """Test checking if cell is empty."""
        assert self.board.is_empty(0, 0)
        self.board.set_cell(0, 0, PlayerColor.BLACK)
        assert not self.board.is_empty(0, 0)

    def test_is_in_bounds(self):
        """Test boundary checking."""
        assert self.board.is_in_bounds(0, 0)
        assert self.board.is_in_bounds(7, 7)
        assert not self.board.is_in_bounds(8, 0)
        assert not self.board.is_in_bounds(-1, 0)
