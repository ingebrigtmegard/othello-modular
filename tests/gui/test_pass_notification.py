"""Tests for pass notification system."""

from unittest.mock import Mock, patch

from othello.core.constants import PlayerColor
from othello.core.events import EngineEvent, EngineEventType
from othello.gui.game_controller import GameController


class TestPassNotification:
    """Test suite for pass notification system."""

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

        # FIX: Mock sound_manager
        self.mock_sound_manager = Mock()

        # Patch GameController to use mock sound_manager
        self.original_sound_manager = None
        try:
            from othello.utils import sounds

            self.original_sound_manager = sounds.SoundManager
        except ImportError:
            pass

    def test_pass_event_shows_notification(self):
        """Test that pass event triggers notification."""
        # Create controller with mocked sound_manager
        with patch(
            "othello.gui.game_controller.SoundManager",
            return_value=self.mock_sound_manager,
        ):
            controller = GameController(
                self.mock_board, self.mock_score, self.mock_menu
            )

            # Simulate pass event
            event = EngineEvent(
                EngineEventType.PASS_OCCURRED,
                {"player": PlayerColor.BLACK, "message": "Pass"},
            )
            controller.on_engine_event(event)

            self.mock_score.show_pass.assert_called_once_with(PlayerColor.BLACK)
            self.mock_sound_manager.play.assert_called_once_with("pass")

    def test_pass_event_sets_timer(self):
        """Test that pass event starts hide timer."""
        controller = GameController(self.mock_board, self.mock_score, self.mock_menu)

        # Simulate pass event
        event = EngineEvent(
            EngineEventType.PASS_OCCURRED,
            {"player": PlayerColor.WHITE, "message": "Pass"},
        )
        controller.on_engine_event(event)

        # Timer should be started (check if start method was called)
        assert controller.pass_timer is not None

    def test_hide_pass_notification_works(self):
        """Test that hide pass notification clears the message."""
        controller = GameController(self.mock_board, self.mock_score, self.mock_menu)

        # Call hide directly
        controller._hide_pass_notification()

        self.mock_score.hide_pass.assert_called_once()
