"""Tests for HumanPlayerAdapter."""

import pytest

from othello.core.constants import PlayerColor
from othello.players.human_adapter import HumanPlayerAdapter


class TestHumanPlayerAdapter:
    """Test suite for HumanPlayerAdapter."""

    def test_init(self):
        """Test player initialization."""
        player = HumanPlayerAdapter(PlayerColor.BLACK)
        assert player.get_color() == PlayerColor.BLACK

    def test_set_move(self):
        """Test setting a move from GUI."""
        player = HumanPlayerAdapter(PlayerColor.BLACK)
        player.set_move((2, 4))
        assert player.pending_move == (2, 4)

    def test_get_move_returns_set_move(self):
        """Test that get_move returns the set move."""
        player = HumanPlayerAdapter(PlayerColor.BLACK)
        player.set_move((2, 4))
        valid_moves = [(2, 4), (3, 5)]

        move = player.get_move(valid_moves)
        assert move == (2, 4)

    def test_get_move_raises_on_no_move(self):
        """Test that get_move raises ValueError when no move is set."""
        player = HumanPlayerAdapter(PlayerColor.BLACK)

        with pytest.raises(ValueError):
            player.get_move([(2, 4)])

    def test_get_move_raises_on_invalid_move(self):
        """Test that get_move raises ValueError on invalid move."""
        player = HumanPlayerAdapter(PlayerColor.BLACK)
        player.set_move((0, 0))
        valid_moves = [(2, 4), (3, 5)]

        with pytest.raises(ValueError):
            player.get_move(valid_moves)
