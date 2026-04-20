"""Main application window."""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QMainWindow, QVBoxLayout, QWidget

from .gui.board_widget import BoardWidget
from .gui.game_controller import GameController
from .gui.menu_widget import MenuWidget
from .gui.score_widget import ScoreWidget


class MainWindow(QMainWindow):
    """
    Main application window.

    Attributes:
        game_controller: GameController instance
    """

    def __init__(self) -> None:
        """Initialize main window."""
        super().__init__()
        self._setup_ui()

    def closeEvent(self, event) -> None:
        """Handle window close event."""
        if self.game_controller:
            self.game_controller.deactivate()
        event.accept()

    def _setup_ui(self) -> None:
        """Set up the main window UI."""
        self.setWindowTitle("Othello (Reversi)")
        self.setMinimumSize(800, 700)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout()
        central_widget.setLayout(layout)

        # Game area (board + score)
        game_area = QWidget()
        game_layout = QVBoxLayout()
        game_area.setLayout(game_layout)

        # Board
        self.board_widget = BoardWidget()
        game_layout.addWidget(self.board_widget, alignment=Qt.AlignmentFlag.AlignCenter)

        # Score
        self.score_widget = ScoreWidget()
        game_layout.addWidget(self.score_widget)

        layout.addWidget(game_area)

        # Menu area
        self.menu_widget = MenuWidget()
        layout.addWidget(self.menu_widget, alignment=Qt.AlignmentFlag.AlignTop)

        # Controller
        self.game_controller = GameController(
            self.board_widget, self.score_widget, self.menu_widget
        )
