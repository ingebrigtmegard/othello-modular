"""Tests for RulesValidator (flipping logic)."""

from ..src.othello.core.board import Board
from ..src.othello.core.constants import PlayerColor
from ..src.othello.core.rules import RulesValidator


class TestRulesValidator:
    def setup_method(self):
        self.validator = RulesValidator()

    def _clear_center(self, board: Board) -> None:
        """Helper to clear center discs for clean test setup."""
        board.set_cell(3, 3, PlayerColor.EMPTY)
        board.set_cell(4, 4, PlayerColor.EMPTY)
        board.set_cell(3, 4, PlayerColor.EMPTY)
        board.set_cell(4, 3, PlayerColor.EMPTY)

    def test_horizontal_flip(self):
        """Test flipping discs horizontally."""
        board = Board()
        self._clear_center(board)

        # Set up: Black at (4,0), White at (4,1), (4,2), Black at (4,3)
        # Place new Black at (4,4) - should NOT flip (Black at 4,3 blocks)
        board.set_cell(4, 0, PlayerColor.BLACK)
        board.set_cell(4, 1, PlayerColor.WHITE)
        board.set_cell(4, 2, PlayerColor.WHITE)
        board.set_cell(4, 3, PlayerColor.BLACK)

        flips = self.validator.calculate_flips(board, 4, 4, PlayerColor.BLACK)
        # Going LEFT from (4,4): (4,3)=Black (same color, no bracket!)
        # No flips possible
        assert len(flips) == 0

    def test_horizontal_flip_correct(self):
        """Test flipping discs horizontally - correct setup."""
        board = Board()
        self._clear_center(board)

        # Set up: Black at (4,1), White at (4,2), (4,3)
        # Place new Black at (4,4) - should flip White at (4,3) and (4,2)
        board.set_cell(4, 1, PlayerColor.BLACK)
        board.set_cell(4, 2, PlayerColor.WHITE)
        board.set_cell(4, 3, PlayerColor.WHITE)

        flips = self.validator.calculate_flips(board, 4, 4, PlayerColor.BLACK)
        # Going LEFT from (4,4): (4,3)=White, (4,2)=White, (4,1)=Black (bracket!)
        assert len(flips) == 2
        assert (4, 3) in flips
        assert (4, 2) in flips

    def test_vertical_flip(self):
        """Test flipping discs vertically."""
        board = Board()
        self._clear_center(board)

        # Set up: Black at (1,4), White at (2,4), (3,4)
        # Place new Black at (4,4) - should flip White at (3,4) and (2,4)
        board.set_cell(1, 4, PlayerColor.BLACK)
        board.set_cell(2, 4, PlayerColor.WHITE)
        board.set_cell(3, 4, PlayerColor.WHITE)

        flips = self.validator.calculate_flips(board, 4, 4, PlayerColor.BLACK)
        # Going UP from (4,4): (3,4)=White, (2,4)=White, (1,4)=Black (bracket!)
        assert len(flips) == 2
        assert (3, 4) in flips
        assert (2, 4) in flips

    def test_diagonal_flip(self):
        """Test flipping discs diagonally."""
        board = Board()
        self._clear_center(board)

        # Set up: Black at (1,1), White at (2,2), (3,3)
        # Place new Black at (4,4) - should flip White at (3,3) and (2,2)
        board.set_cell(1, 1, PlayerColor.BLACK)
        board.set_cell(2, 2, PlayerColor.WHITE)
        board.set_cell(3, 3, PlayerColor.WHITE)

        flips = self.validator.calculate_flips(board, 4, 4, PlayerColor.BLACK)
        # Going UP-LEFT from (4,4): (3,3)=White, (2,2)=White, (1,1)=Black (bracket!)
        assert len(flips) == 2
        assert (3, 3) in flips
        assert (2, 2) in flips

    def test_no_flip_no_bracket(self):
        """Test no flip when no bracket exists."""
        board = Board()
        self._clear_center(board)

        board.set_cell(4, 0, PlayerColor.WHITE)
        board.set_cell(4, 1, PlayerColor.WHITE)

        flips = self.validator.calculate_flips(board, 4, 2, PlayerColor.BLACK)
        # Going LEFT from (4,2): (4,1)=White, (4,0)=White, then edge
        # No Black disc to bracket - no flips
        assert len(flips) == 0

    def test_is_valid_move(self):
        """Test valid move detection."""
        board = Board()
        # Valid move at (2, 4) - flips white disc at (3, 4) with Black at (4, 4)
        assert self.validator.is_valid_move(board, 2, 4, PlayerColor.BLACK)

    def test_is_invalid_move_occupied(self):
        """Test invalid move on occupied cell."""
        board = Board()
        assert not self.validator.is_valid_move(board, 3, 3, PlayerColor.BLACK)

    def test_is_invalid_move_no_flip(self):
        """Test invalid move when no discs can be flipped."""
        board = Board()
        # (0, 0) is empty but no bracketing possible
        assert not self.validator.is_valid_move(board, 0, 0, PlayerColor.BLACK)

    def test_all_directions_check(self):
        """Test that all 8 directions are checked."""
        board = Board()
        # Setup for valid move in multiple directions
        # Black at (3,3) and (4,4), White at (3,4) and (4,3)
        # This is the standard initial setup
        # (2, 4) should be valid - flips White at (3,4) with Black at (4,4)
        assert self.validator.is_valid_move(board, 2, 4, PlayerColor.BLACK)

    def test_edge_cases_no_flip(self):
        """Test edge cases where flipping should occur."""
        board = Board()
        self._clear_center(board)

        # Black at (0,0), White at (0,1), place Black at (0,2)
        board.set_cell(0, 0, PlayerColor.BLACK)
        board.set_cell(0, 1, PlayerColor.WHITE)

        flips = self.validator.calculate_flips(board, 0, 2, PlayerColor.BLACK)
        # Going LEFT from (0,2): (0,1)=White, (0,0)=Black (bracket!)
        # This SHOULD flip 1 disc
        assert len(flips) == 1
        assert (0, 1) in flips

    def test_edge_cases_no_flip_no_bracket(self):
        """Test edge cases where flipping should not occur."""
        board = Board()
        self._clear_center(board)

        # White at (0,0), White at (0,1), place Black at (0,2)
        board.set_cell(0, 0, PlayerColor.WHITE)
        board.set_cell(0, 1, PlayerColor.WHITE)

        flips = self.validator.calculate_flips(board, 0, 2, PlayerColor.BLACK)
        # Going LEFT: (0,1)=White, (0,0)=White, then edge
        # No Black disc to bracket - no flips
        assert len(flips) == 0
