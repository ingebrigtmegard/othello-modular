# src/othello/gui/board_widget.py

from typing import List, Tuple

from PyQt6.QtCore import Qt, QTimer, pyqtSignal  # ADDED QTimer for single-shot timing
from PyQt6.QtGui import QBrush, QColor, QPainter, QPen
from PyQt6.QtWidgets import QGridLayout, QLabel, QWidget

from othello.core.constants import PlayerColor

# REMOVED: import time  # BLOCKING CALLS REMOVED


class CellLabel(QLabel):
    """Individual cell widget on the board."""

    # Custom signal for cell clicks
    cell_clicked = pyqtSignal(int, int)

    def __init__(self, row: int, col: int, parent: QWidget = None) -> None:
        """
        Initialize cell label.

        Args:
            row: Row index (0-7)
            col: Column index (0-7)
            parent: Parent widget
        """
        super().__init__(parent)
        self.row = row
        self.col = col
        self.piece_color: PlayerColor = PlayerColor.EMPTY
        self.is_valid_move = False
        self.setFixedSize(60, 60)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def set_piece(self, color: PlayerColor) -> None:
        """
        Set the piece color for this cell.

        Args:
            color: PlayerColor enum value
        """
        self.piece_color = color
        self.update()

    def set_valid_move(self, valid: bool) -> None:
        """
        Mark this cell as a valid move.

        Args:
            valid: True if this is a valid move
        """
        self.is_valid_move = valid
        self.update()

    def paintEvent(self, event) -> None:
        """Custom paint event for drawing cell and piece."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw background
        bg_color = (
            QColor("#228B22")
            if self.piece_color == PlayerColor.EMPTY
            else QColor("#1A521A")
        )
        if self.is_valid_move:
            bg_color = QColor("#32CD32")  # Highlight valid moves
        painter.setBrush(QBrush(bg_color))
        painter.setPen(QPen(QColor("#000000"), 1))
        painter.drawRect(0, 0, self.width(), self.height())

        # Draw piece
        if self.piece_color != PlayerColor.EMPTY:
            margin = 5
            piece_color = (
                QColor("#000000")
                if self.piece_color == PlayerColor.BLACK
                else QColor("#FFFFFF")
            )
            painter.setBrush(QBrush(piece_color))
            painter.setPen(QPen(QColor("#000000"), 1))
            painter.drawEllipse(
                margin, margin, self.width() - 2 * margin, self.height() - 2 * margin
            )

    def mousePressEvent(self, event) -> None:
        """Handle mouse click on cell."""
        if self.is_valid_move:
            # Emit custom signal with row and col
            self.cell_clicked.emit(self.row, self.col)
            super().mousePressEvent(event)


class BoardWidget(QWidget):
    """
    Widget representing the 8x8 Othello board.

    Attributes:
        cell_labels: 2D array of CellLabel widgets
    """

    def __init__(self, parent: QWidget = None) -> None:
        """
        Initialize board widget.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.cell_labels: list[list[CellLabel]] = []
        self._create_board()
        self._connect_signals()
        # NO ANIMATION TIMER NEEDED - WE USE QTimer.singleShot FOR EACH CELL

    def _create_board(self) -> None:
        """Create the 8x8 grid of cell labels."""
        layout = QGridLayout()
        layout.setSpacing(1)
        layout.setContentsMargins(1, 1, 1, 1)

        for row in range(8):
            row_labels = []
            for col in range(8):
                cell = CellLabel(row, col, self)
                layout.addWidget(cell, row, col)
                row_labels.append(cell)
            self.cell_labels.append(row_labels)

        self.setLayout(layout)

    def _connect_signals(self) -> None:
        """Connect cell click signals to parent."""
        for row in range(8):
            for col in range(8):
                self.cell_labels[row][col].cell_clicked.connect(
                    lambda r, c: self._on_cell_clicked(r, c)
                )

    def _on_cell_clicked(self, row: int, col: int) -> None:
        """
        Handle cell click event.

        Args:
            row: Row index
            col: Column index
        """
        if self.cell_labels[row][col].is_valid_move:
            self.cell_clicked.emit(row, col)

    def update_board(self, board_state: dict) -> None:
        """
        Update board display from board state.

        Args:
            board_state: Dict with cell colors {(row, col): PlayerColor}
        """
        for row in range(8):
            for col in range(8):
                color = board_state.get((row, col), PlayerColor.EMPTY)
                self.cell_labels[row][col].set_piece(color)

    def set_valid_moves(self, valid_moves: list[tuple[int, int]]) -> None:
        """
        Highlight valid move cells.

        Args:
            valid_moves: List of (row, col) tuples
        """
        valid_set = set(valid_moves)
        for row in range(8):
            for col in range(8):
                is_valid = (row, col) in valid_set
                self.cell_labels[row][col].set_valid_move(is_valid)

    def clear_valid_moves(self) -> None:
        """Clear all valid move highlights."""
        for row in range(8):
            for col in range(8):
                self.cell_labels[row][col].set_valid_move(False)

    def get_current_player_color(self) -> PlayerColor:
        """
        Get the current player's color from UI.

        Returns:
            PlayerColor enum value
        """
        # This would be set by the controller
        return PlayerColor.BLACK

    # Custom signal for cell clicks (emitted by BoardWidget)
    cell_clicked = pyqtSignal(int, int)

    def highlight_invalid_move(self, row: int, col: int) -> None:
        """
        Highlight invalid move with red flash (for error feedback).

        Args:
            row: Row index
            col: Column index
        """
        cell = self.cell_labels[row][col]
        original_color = cell.piece_color
        cell.piece_color = PlayerColor.WHITE  # Temporarily flash white
        cell.update()
        # REMOVED: time.sleep(0.1)  # BLOCKING CALL
        # ADDED: Non-blocking flash using QTimer
        QTimer.singleShot(100, lambda: self._restore_cell_color(cell, original_color))

    def _restore_cell_color(self, cell: CellLabel, original_color: PlayerColor) -> None:
        """Helper to restore cell color after invalid move flash."""
        cell.piece_color = original_color
        cell.update()

    # ======================
    # RIPPLE ANIMATION SYSTEM
    # ======================

    def start_ripple_animation(
        self,
        placed_coord: Tuple[int, int],
        flips: List[Tuple[int, int]],
        mover_color: PlayerColor,
    ) -> None:
        """
        Start ripple flash animation for flipped pieces.
        Propagates outward from placed piece with direction-based timing:
        - Horizontal/vertical: 50ms per grid step
        - Diagonal: 75ms per grid step

        Args:
            placed_coord: (row, col) where the new piece was placed
            flips: List of (row, col) tuples that were flipped
            mover_color: PlayerColor of the player who made the move
        """
        placed_r, placed_c = placed_coord

        for r, c in flips:
            # Calculate grid distances
            dr = abs(r - placed_r)
            dc = abs(c - placed_c)

            # Calculate propagation delay based on direction
            if dr == 0 or dc == 0:  # Horizontal/vertical (same row or column)
                delay = (dr + dc) * 50  # Manhattan distance * 50ms
            elif dr == dc:  # True diagonal (equal row/col distance)
                delay = dr * 75  # Diagonal steps * 75ms
            else:
                # Fallback for non-standard directions (shouldn't occur in Othello)
                delay = max(dr, dc) * 50

            # Schedule the flash for this specific cell
            QTimer.singleShot(
                delay, lambda r=r, c=c: self._execute_ripple_flash(r, c, mover_color)
            )

    def _execute_ripple_flash(
        self, row: int, col: int, target_color: PlayerColor
    ) -> None:
        """
        Execute the 3-frame flash sequence for a single cell:
        [target color] → [opposite color] → [target color]
        Each phase lasts 50ms (total 150ms flash duration)
        """
        cell = self.cell_labels[row][col]

        # Phase 0: Show target color immediately when timer fires
        cell.set_piece(target_color)
        cell.update()

        # Phase 1: Show opposite color after 50ms
        QTimer.singleShot(50, lambda: self._flash_phase_two(cell, target_color))

        # Phase 2: Show target color after 100ms
        QTimer.singleShot(100, lambda: self._flash_phase_three(cell, target_color))

    def _flash_phase_two(self, cell: CellLabel, target_color: PlayerColor) -> None:
        """Middle phase: flash the opponent color."""
        cell.set_piece(self._get_opponent(target_color))
        cell.update()

    def _flash_phase_three(self, cell: CellLabel, target_color: PlayerColor) -> None:
        """Final phase: settle to target color."""
        cell.set_piece(target_color)
        cell.update()

    def _get_opponent(self, color: PlayerColor) -> PlayerColor:
        """Get the opposite color."""
        return PlayerColor.WHITE if color == PlayerColor.BLACK else PlayerColor.BLACK
