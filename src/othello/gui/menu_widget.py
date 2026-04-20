"""Menu widget for game controls."""

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QComboBox,
    QGroupBox,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class MenuWidget(QWidget):
    """
    Widget for game menu and controls.

    Attributes:
        new_game_btn: Button to start new game
        quit_btn: Button to quit game
        ai_black_combo: Dropdown for Black AI difficulty
        ai_white_combo: Dropdown for White AI difficulty
    """

    # Signal emitted when player configuration changes
    player_config_changed = pyqtSignal(str, str)

    def __init__(self, parent: QWidget = None) -> None:
        """
        Initialize menu widget.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the UI components."""
        layout = QVBoxLayout()
        layout.setSpacing(15)

        # New Game Button
        self.new_game_btn = QPushButton("NEW GAME")
        self.new_game_btn.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.new_game_btn.setStyleSheet(
            "background-color: #4CAF50; color: white; padding: 10px;"
        )
        layout.addWidget(self.new_game_btn)

        # AI Configuration
        config_group = QGroupBox("Player Configuration")
        config_layout = QVBoxLayout()
        config_layout.setSpacing(10)

        # Black Player
        black_label = QLabel("Black Player:")
        black_label.setFont(QFont("Arial", 10))
        self.ai_black_combo = self._create_player_combo()
        self.ai_black_combo.currentIndexChanged.connect(self._on_config_changed)
        black_layout = QVBoxLayout()
        black_layout.addWidget(black_label)
        black_layout.addWidget(self.ai_black_combo)
        config_layout.addLayout(black_layout)

        # White Player
        white_label = QLabel("White Player:")
        white_label.setFont(QFont("Arial", 10))
        self.ai_white_combo = self._create_player_combo()
        self.ai_white_combo.currentIndexChanged.connect(self._on_config_changed)
        white_layout = QVBoxLayout()
        white_layout.addWidget(white_label)
        white_layout.addWidget(self.ai_white_combo)
        config_layout.addLayout(white_layout)

        config_group.setLayout(config_layout)
        layout.addWidget(config_group)

        # Quit Button
        self.quit_btn = QPushButton("QUIT")
        self.quit_btn.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.quit_btn.setStyleSheet(
            "background-color: #f44336; color: white; padding: 10px;"
        )
        layout.addWidget(self.quit_btn)

        layout.addStretch()
        self.setLayout(layout)

    def _create_player_combo(self):
        """Create player type dropdown."""
        combo = QComboBox()
        combo.addItems(["Human", "AI - Easy", "AI - Medium", "AI - Hard"])
        combo.setFont(QFont("Arial", 10))
        combo.setCurrentIndex(1)  # Default to AI - Medium
        return combo

    def _on_config_changed(self) -> None:
        """Handle configuration change."""
        black_player = self.ai_black_combo.currentText()
        white_player = self.ai_white_combo.currentText()
        self.player_config_changed.emit(black_player, white_player)

    def get_player_config(self) -> tuple[str, str]:
        """
        Get current player configuration.

        Returns:
            Tuple of (black_player, white_player)
        """
        return (self.ai_black_combo.currentText(), self.ai_white_combo.currentText())

    def set_player_config(self, black: str, white: str) -> None:
        """
        Set player configuration.

        Args:
            black: Black player type
            white: White player type
        """
        # Find index for black player
        for i in range(self.ai_black_combo.count()):
            if self.ai_black_combo.itemText(i) == black:
                self.ai_black_combo.setCurrentIndex(i)
                break

        # Find index for white player
        for i in range(self.ai_white_combo.count()):
            if self.ai_white_combo.itemText(i) == white:
                self.ai_white_combo.setCurrentIndex(i)
                break
