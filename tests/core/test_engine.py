"""Tests for OthelloEngine (game state and flow)."""

from othello.core.constants import PlayerColor
from othello.core.engine import OthelloEngine


class TestOthelloEngine:
    def setup_method(self):
        """Create fresh engine before each test."""
        self.engine = OthelloEngine()

    def test_initial_state(self):
        """Test initial board setup and player."""
        assert self.engine.current_player == PlayerColor.BLACK
        assert not self.engine.game_over

    def test_initial_valid_moves_black(self):
        """Test that Black has valid moves initially."""
        valid_moves = self.engine.get_valid_moves(PlayerColor.BLACK)
        assert len(valid_moves) > 0
        # Known valid moves from center setup
        # (2,4) brackets White at (3,4) with Black at (4,4)
        # (3,5) brackets White at (3,4) with Black at (3,3)
        # (4,2) brackets White at (4,3) with Black at (4,4)
        # (5,3) brackets White at (4,3) with Black at (3,3)
        assert (2, 4) in valid_moves
        assert (3, 5) in valid_moves
        assert (4, 2) in valid_moves
        assert (5, 3) in valid_moves
        # (2,3) is NOT valid - no bracketing possible
        assert (2, 3) not in valid_moves

    def test_initial_valid_moves_white(self):
        """Test that White has valid moves initially."""
        valid_moves = self.engine.get_valid_moves(PlayerColor.WHITE)
        assert len(valid_moves) > 0
        # Known valid moves for White from center setup
        assert (2, 3) in valid_moves
        assert (3, 2) in valid_moves
        assert (4, 5) in valid_moves
        assert (5, 4) in valid_moves

    def test_execute_valid_move(self):
        """Test executing a valid move."""
        # Place Black at (2, 4)
        success, flips = self.engine.execute_move((2, 4))
        assert success
        assert self.engine.current_player == PlayerColor.WHITE
        # Optional: verify we got some flips
        assert len(flips) > 0

    def test_execute_invalid_move(self):
        """Test executing an invalid move."""
        # (0, 0) is invalid
        success, flips = self.engine.execute_move((0, 0))
        assert not success
        assert flips == []  # Optional but good practice to verify

    def test_auto_pass_single_player(self):
        """Test automatic pass when one player has no moves."""
        # Create a state where Black has no moves
        original_black_moves = self.engine.valid_moves_cache[PlayerColor.BLACK]
        self.engine.valid_moves_cache[PlayerColor.BLACK] = []

        # Trigger game end check (which handles auto-pass)
        self.engine._check_game_end()

        assert self.engine.current_player == PlayerColor.WHITE
        assert not self.engine.game_over

        # Restore
        self.engine.valid_moves_cache[PlayerColor.BLACK] = original_black_moves

    def test_game_over_double_pass(self):
        """Test game ends when both players have no moves."""
        # Create empty valid moves for both players
        self.engine.valid_moves_cache[PlayerColor.BLACK] = []
        self.engine.valid_moves_cache[PlayerColor.WHITE] = []

        # Black starts with no moves
        self.engine.current_player = PlayerColor.BLACK
        self.engine._check_game_end()

        assert self.engine.game_over

    def test_game_over_board_full_through_double_pass(self):
        """Test game ends when board is full (handled via double-pass logic)."""
        # Fill the board (simulate)
        for r in range(8):
            for c in range(8):
                if r < 4:
                    self.engine.board.set_cell(r, c, PlayerColor.BLACK)
                else:
                    self.engine.board.set_cell(r, c, PlayerColor.WHITE)

        # Recalculate valid moves cache (important: no empty cells = no valid moves)
        self.engine._recalculate_valid_moves()

        # Both players should have no valid moves
        assert len(self.engine.valid_moves_cache[PlayerColor.BLACK]) == 0
        assert len(self.engine.valid_moves_cache[PlayerColor.WHITE]) == 0

        # Trigger game end check
        self.engine._check_game_end()

        assert self.engine.game_over

    def test_score_calculation(self):
        """Test score counting."""
        # After initial setup: 2 Black, 2 White
        score_black = self.engine.get_score(PlayerColor.BLACK)
        score_white = self.engine.get_score(PlayerColor.WHITE)
        assert score_black == 2
        assert score_white == 2

    def test_score_after_move(self):
        """Test score updates after move."""
        self.engine.execute_move((2, 4))
        score_black = self.engine.get_score(PlayerColor.BLACK)
        score_white = self.engine.get_score(PlayerColor.WHITE)
        # Black should have more (placed 1, flipped at least 1)
        assert score_black > score_white

    def test_turn_switching(self):
        """Test that turns alternate correctly."""
        self.engine.execute_move((2, 4))
        assert self.engine.current_player == PlayerColor.WHITE

        self.engine.execute_move((2, 3))
        assert self.engine.current_player == PlayerColor.BLACK

    def test_valid_moves_updated_after_move(self):
        """Test that valid moves list is updated after each move."""
        initial_count = len(self.engine.get_valid_moves(PlayerColor.BLACK))
        self.engine.execute_move((2, 4))
        new_count = len(self.engine.get_valid_moves(PlayerColor.BLACK))
        # Count should change after move
        assert initial_count != new_count

    def test_game_not_over_with_moves_available(self):
        """Test game continues when moves are available."""
        # Ensure both players have moves
        self.engine.valid_moves_cache[PlayerColor.BLACK] = [(2, 4)]
        self.engine.valid_moves_cache[PlayerColor.WHITE] = [(2, 3)]

        self.engine._check_game_end()
        assert not self.engine.game_over

    def test_reset_clears_state(self):
        """Test that reset returns engine to initial state."""
        # Make some moves first
        self.engine.execute_move((2, 4))
        self.engine.execute_move((2, 3))

        # Reset
        self.engine.reset()

        assert self.engine.current_player == PlayerColor.BLACK
        assert not self.engine.game_over
        assert len(self.engine.get_valid_moves(PlayerColor.BLACK)) > 0
        assert len(self.engine.get_valid_moves(PlayerColor.WHITE)) > 0
