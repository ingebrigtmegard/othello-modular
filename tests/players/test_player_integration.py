"""Integration tests for player system with engine."""

from src.othello.core.constants import PlayerColor
from src.othello.core.engine import OthelloEngine
from src.othello.players.ai_player import AiPlayer
from src.othello.players.random_player import RandomPlayer


class TestPlayerIntegration:
    """Integration tests for players with OthelloEngine."""

    def test_random_player_vs_random_player(self):
        """Test game between two random players."""
        engine = OthelloEngine()
        black = RandomPlayer(PlayerColor.BLACK)
        white = RandomPlayer(PlayerColor.WHITE)

        move_count = 0
        max_moves = 100  # Safety limit

        while not engine.game_over and move_count < max_moves:
            valid_moves = engine.get_valid_moves(engine.current_player)

            if valid_moves:
                if engine.current_player == PlayerColor.BLACK:
                    move = black.get_move(valid_moves)
                else:
                    move = white.get_move(valid_moves)

                engine.execute_move(move)
                move_count += 1

        # Game should end properly
        assert engine.game_over
        assert engine.get_winner() is not None or engine.get_score(
            PlayerColor.BLACK
        ) == engine.get_score(PlayerColor.WHITE)

    def test_ai_player_vs_random_player(self):
        """Test game between AI and random player."""
        engine = OthelloEngine()
        ai = AiPlayer(PlayerColor.BLACK)
        random = RandomPlayer(PlayerColor.WHITE)

        move_count = 0
        max_moves = 100

        while not engine.game_over and move_count < max_moves:
            valid_moves = engine.get_valid_moves(engine.current_player)

            if valid_moves:
                if engine.current_player == PlayerColor.BLACK:
                    move = ai.get_move(valid_moves)
                else:
                    move = random.get_move(valid_moves)

                engine.execute_move(move)
                move_count += 1

        assert engine.game_over

    def test_player_color_consistency(self):
        """Test that players maintain their color."""
        black = RandomPlayer(PlayerColor.BLACK)
        white = AiPlayer(PlayerColor.WHITE)

        assert black.get_color() == PlayerColor.BLACK
        assert white.get_color() == PlayerColor.WHITE
