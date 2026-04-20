"""Tests for AiPlayer."""

import pytest

from src.othello.core.constants import PlayerColor
from src.othello.players.ai_player import AiPlayer


class TestAiPlayer:
    """Test suite for AiPlayer."""

    def test_init(self):
        """Test player initialization."""
        player = AiPlayer(PlayerColor.BLACK)
        assert player.get_color() == PlayerColor.BLACK
        assert player.difficulty == "medium"

    def test_init_with_difficulty(self):
        """Test player initialization with difficulty."""
        player = AiPlayer(PlayerColor.WHITE, "hard")
        assert player.difficulty == "hard"

    def test_get_move_prefer_corners(self):
        """Test that AI prefers corner moves."""
        player = AiPlayer(PlayerColor.BLACK)
        valid_moves = [(1, 1), (2, 2), (0, 0), (3, 3)]

        move = player.get_move(valid_moves)
        assert move == (0, 0), "AI should prefer corner (0,0)"

    def test_get_move_avoid_x_squares(self):
        """Test that AI avoids X squares adjacent to corners."""
        player = AiPlayer(PlayerColor.BLACK)
        valid_moves = [(1, 1), (2, 2), (3, 3), (4, 4)]

        move = player.get_move(valid_moves)
        assert move != (1, 1), "AI should avoid X square (1,1)"

    def test_get_move_raises_on_empty_moves(self):
        """Test that get_move raises ValueError on empty moves."""
        player = AiPlayer(PlayerColor.BLACK)

        with pytest.raises(ValueError):
            player.get_move([])

    def test_position_weights_setup(self):
        """Test that position weights are set correctly."""
        player = AiPlayer(PlayerColor.BLACK)

        # Corners should have highest weight
        assert player.position_weights[0][0] == player.CORNER_WEIGHT
        assert player.position_weights[0][7] == player.CORNER_WEIGHT
        assert player.position_weights[7][0] == player.CORNER_WEIGHT
        assert player.position_weights[7][7] == player.CORNER_WEIGHT

        # X squares should have negative weight
        assert player.position_weights[1][1] == player.X_SQUARE_WEIGHT
        assert player.position_weights[6][6] == player.X_SQUARE_WEIGHT
