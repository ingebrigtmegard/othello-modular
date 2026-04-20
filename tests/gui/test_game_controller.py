"""Tests for GameController."""

from unittest.mock import Mock

from src.othello.core.constants import PlayerColor
from src.othello.gui.game_controller import GameController
from src.othello.players.random_player import RandomPlayer


class TestGameController:
    """Test suite for GameController."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_board = Mock()
        self.mock_board.cell_clicked = Mock()
        self.mock_score = Mock()
        self.mock_menu = Mock()

        # Configure get_player_config to return a tuple
        self.mock_menu.get_player_config.return_value = ("Human", "AI - Medium")

        self.mock_menu.new_game_btn = Mock()
        self.mock_menu.new_game_btn.clicked = Mock()
        self.mock_menu.quit_btn = Mock()
        self.mock_menu.quit_btn.clicked = Mock()

    def test_init(self):
        """Test controller initialization."""
        controller = GameController(self.mock_board, self.mock_score, self.mock_menu)
        assert controller.engine is not None
        assert controller.board_widget == self.mock_board

    def test_set_players(self):
        """Test setting players."""
        controller = GameController(self.mock_board, self.mock_score, self.mock_menu)
        players = {PlayerColor.BLACK: RandomPlayer(PlayerColor.BLACK)}
        controller.set_players(players)
        assert PlayerColor.BLACK in controller.players

    def test_update_display_calls_widget_methods(self):
        """Test that update_display calls widget update methods."""
        controller = GameController(self.mock_board, self.mock_score, self.mock_menu)

        # Reset mock call count (called once in __init__)
        self.mock_board.reset_mock()
        self.mock_score.reset_mock()

        controller._update_display()

        self.mock_board.update_board.assert_called_once()
        self.mock_board.set_valid_moves.assert_called_once()
        self.mock_score.update_scores.assert_called_once()
        self.mock_score.set_turn.assert_called_once()
