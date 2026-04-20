"""Tests for game constants."""

from othello.core.constants import BoardSize, PlayerColor


class TestConstants:
    def test_board_size(self):
        assert BoardSize.ROWS == 8
        assert BoardSize.COLS == 8

    def test_player_colors(self):
        assert PlayerColor.BLACK.value == 1
        assert PlayerColor.WHITE.value == 2
