"""Score display widget."""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget

from othello.core.constants import PlayerColor


class ScoreWidget(QWidget):
    """
    Widget for displaying scores and turn information.

    Attributes:
        black_score_label: Label for Black score
        white_score_label: Label for White score
        turn_label: Label showing whose turn it is
        pass_label: Label for pass notifications
    """

    def __init__(self, parent: QWidget = None) -> None:
        """
        Initialize score widget.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the UI components."""
        layout = QVBoxLayout()
        layout.setSpacing(10)

        # Header
        header = QLabel("OTHELLO")
        header.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)

        # Score layout
        score_layout = QHBoxLayout()

        # Black score
        black_label = QLabel("BLACK:")
        black_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        black_label.setStyleSheet("color: black;")
        self.black_score_label = QLabel("2")
        self.black_score_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        self.black_score_label.setStyleSheet("color: black;")
        black_layout = QVBoxLayout()
        black_layout.addWidget(black_label)
        black_layout.addWidget(self.black_score_label)
        black_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        score_layout.addLayout(black_layout)

        # Spacer
        score_layout.addStretch()

        # White score
        white_label = QLabel("WHITE:")
        white_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        white_label.setStyleSheet("color: white;")
        self.white_score_label = QLabel("2")
        self.white_score_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        self.white_score_label.setStyleSheet("color: white;")
        white_layout = QVBoxLayout()
        white_layout.addWidget(white_label)
        white_layout.addWidget(self.white_score_label)
        white_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        score_layout.addLayout(white_layout)

        layout.addLayout(score_layout)

        # Turn indicator
        self.turn_label = QLabel("Turn: BLACK")
        self.turn_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.turn_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.turn_label.setStyleSheet(
            "background-color: #333333; color: white; padding: 5px;"
        )
        layout.addWidget(self.turn_label)

        # Pass notification
        self.pass_label = QLabel("")
        self.pass_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.pass_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pass_label.setStyleSheet(
            "color: #FFD700; background-color: #333333; padding: 5px;"
        )
        self.pass_label.setFixedHeight(30)
        layout.addWidget(self.pass_label)

        self.setLayout(layout)

    def update_scores(self, black_score: int, white_score: int) -> None:
        """
        Update score display.

        Args:
            black_score: Black player score
            white_score: White player score
        """
        self.black_score_label.setText(str(black_score))
        self.white_score_label.setText(str(white_score))

    def set_turn(self, player: PlayerColor) -> None:
        """
        Set current turn indicator.

        Args:
            player: Current player color
        """
        color_name = "BLACK" if player == PlayerColor.BLACK else "WHITE"
        self.turn_label.setText(f"Turn: {color_name}")
        self.turn_label.setStyleSheet(
            "background-color: #333333; color: white; padding: 5px;"
        )

    def show_pass(self, player: PlayerColor) -> None:
        """
        Show pass notification.

        Args:
            player: Player who passed
        """
        color_name = "Black" if player == PlayerColor.BLACK else "White"
        self.pass_label.setText(f"{color_name} has no moves. Passing turn...")

    def hide_pass(self) -> None:
        """Hide pass notification."""
        self.pass_label.setText("")

    def show_game_over(self, winner: PlayerColor | None) -> None:
        """
        Show game over message.

        Args:
            winner: Winner color or None for draw
        """
        if winner is None:
            self.turn_label.setText("GAME OVER - DRAW")
        else:
            color_name = "BLACK" if winner == PlayerColor.BLACK else "WHITE"
            self.turn_label.setText(f"GAME OVER - {color_name} WINS!")
        self.pass_label.setText("")
