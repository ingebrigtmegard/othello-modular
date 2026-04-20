"""Tests for RandomPlayer."""

import pytest

from src.othello.core.constants import PlayerColor
from src.othello.players.random_player import RandomPlayer


class TestRandomPlayer:
    """Test suite for RandomPlayer."""

    def test_init(self):
        """Test player initialization."""
        player = RandomPlayer(PlayerColor.BLACK)
        assert player.get_color() == PlayerColor.BLACK

    def test_get_move_returns_valid_move(self):
        """Test that get_move returns a valid move."""
        player = RandomPlayer(PlayerColor.BLACK)
        valid_moves = [(2, 4), (3, 5), (4, 2), (5, 3)]

        move = player.get_move(valid_moves)
        assert move in valid_moves

    def test_get_move_raises_on_empty_moves(self):
        """Test that get_move raises ValueError on empty moves."""
        player = RandomPlayer(PlayerColor.BLACK)

        with pytest.raises(ValueError):
            player.get_move([])

    def test_multiple_calls_return_different_moves(self):
        """Test that multiple calls can return different moves."""
        player = RandomPlayer(PlayerColor.BLACK)
        valid_moves = [(2, 4), (3, 5), (4, 2), (5, 3)]

        moves = [player.get_move(valid_moves) for _ in range(10)]
        # Not all moves should be the same (with high probability)
        assert len(set(moves)) > 1
