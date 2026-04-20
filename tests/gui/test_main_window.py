"""Tests for MainWindow."""

import pytest
from PyQt6.QtWidgets import QApplication

from othello.gui.main_window import MainWindow


@pytest.fixture
def app():
    """Create Qt application."""
    if not QApplication.instance():
        return QApplication([])
    return QApplication.instance()


class TestMainWindow:
    """Test suite for MainWindow."""

    def test_init(self, app):
        """Test main window initialization."""
        window = MainWindow()
        assert window is not None
        assert window.game_controller is not None
        assert window.board_widget is not None
        assert window.score_widget is not None
        assert window.menu_widget is not None

    def test_window_title(self, app):
        """Test window title."""
        window = MainWindow()
        assert "Othello" in window.windowTitle()

    def test_minimum_size(self, app):
        """Test minimum window size."""
        window = MainWindow()
        min_size = window.minimumSize()
        assert min_size.width() >= 800
        assert min_size.height() >= 700
