"""Controller connecting GUI and Engine."""

import threading

from PyQt6.QtCore import QObject, QTimer, pyqtSignal

from .core.constants import PlayerColor
from .core.engine import OthelloEngine
from .core.events import EngineEvent, EngineEventType
from .gui.board_widget import BoardWidget
from .gui.menu_widget import MenuWidget
from .gui.score_widget import ScoreWidget
from .players.ai_player import AiPlayer
from .players.human_adapter import HumanPlayerAdapter
from .players.interfaces import IPlayer

# Optional sound import
try:
    from .utils.sounds import SoundManager

    SOUND_AVAILABLE = True
except ImportError:
    SOUND_AVAILABLE = False


class GameController(QObject):
    """
    Controller managing interaction between GUI and Engine.
    """

    ai_move_ready = pyqtSignal(tuple)  # (row, col)

    def __init__(
        self,
        board_widget: BoardWidget,
        score_widget: ScoreWidget,
        menu_widget: MenuWidget,
    ) -> None:
        """
        Initialize game controller.

        Args:
            board_widget: Board display widget
            score_widget: Score display widget
            menu_widget: Menu widget
        """
        super().__init__()

        # Initialize sound manager (optional, None if not available)
        if SOUND_AVAILABLE:
            try:
                self.sound_manager = SoundManager()
            except Exception:
                self.sound_manager = None
        else:
            self.sound_manager = None

        # FIX: Add active flag to prevent moves during teardown
        self._active = True

        self.engine = OthelloEngine()
        self.engine.add_observer(self)  # Register as observer
        self.board_widget = board_widget
        self.score_widget = score_widget
        self.menu_widget = menu_widget
        self.players: dict[PlayerColor, IPlayer] = {}

        # Connect GUI signals
        self._connect_signals()

        # Connect AI move signal to handler
        self.ai_move_ready.connect(self._execute_ai_move)

        # Update players from menu
        self._update_players_from_menu()

        # Update display
        self._update_display()

        # Timer for pass notification (1 second)
        self.pass_timer = QTimer()
        self.pass_timer.setSingleShot(True)
        self.pass_timer.timeout.connect(self._hide_pass_notification)

        # FIX: Don't trigger AI turn in __init__ - wait for New Game or window shown
        # self._check_ai_turn()  # COMMENTED OUT

    def _connect_signals(self) -> None:
        """Connect GUI signals to controller methods."""
        self.board_widget.cell_clicked.connect(self._on_cell_clicked)
        self.menu_widget.new_game_btn.clicked.connect(self._on_new_game)
        self.menu_widget.quit_btn.clicked.connect(self._on_quit)
        self.menu_widget.player_config_changed.connect(self._on_player_config_changed)

    def _on_player_config_changed(self, black_player: str, white_player: str) -> None:
        """Handle player configuration change."""
        self._update_players_from_menu()

    def _update_players_from_menu(self) -> None:
        """Update players based on menu configuration."""
        black_type, white_type = self.menu_widget.get_player_config()
        self.players = {}

        if black_type == "Human":
            self.players[PlayerColor.BLACK] = HumanPlayerAdapter(PlayerColor.BLACK)
        else:
            difficulty = (
                "easy"
                if "Easy" in black_type
                else "hard" if "Hard" in black_type else "medium"
            )
            self.players[PlayerColor.BLACK] = AiPlayer(PlayerColor.BLACK, difficulty)

        if white_type == "Human":
            self.players[PlayerColor.WHITE] = HumanPlayerAdapter(PlayerColor.WHITE)
        else:
            difficulty = (
                "easy"
                if "Easy" in white_type
                else "hard" if "Hard" in white_type else "medium"
            )
            self.players[PlayerColor.WHITE] = AiPlayer(PlayerColor.WHITE, difficulty)

    def on_engine_event(self, event: EngineEvent) -> None:
        """Handle engine event (observer pattern)."""
        if not self._active:
            return

        if event.event_type == EngineEventType.PASS_OCCURRED:
            self._show_pass_notification(event.data.get("player"))
            # FIX: Check if sound_manager exists before playing
            if self.sound_manager:
                self.sound_manager.play("pass")
        elif event.event_type == EngineEventType.GAME_OVER:
            self._update_display()
            if self.sound_manager:
                self.sound_manager.play("game_over")
        elif event.event_type == EngineEventType.STATE_UPDATED:
            self._update_display()
            self._check_ai_turn()  # Trigger next AI turn

    def _show_pass_notification(self, player: PlayerColor) -> None:
        """Show pass notification for 1 second."""
        if not self._active:
            return
        self.score_widget.show_pass(player)
        self.pass_timer.start(1000)

    def _hide_pass_notification(self) -> None:
        """Hide pass notification."""
        if self._active:
            self.score_widget.hide_pass()

    def _on_cell_clicked(self, row: int, col: int) -> None:
        if not self._active or self.engine.game_over:
            return

        coord = (row, col)

        # Validate move FIRST
        if coord not in self.engine.get_valid_moves(self.engine.current_player):
            self.board_widget.highlight_invalid_move(row, col)
            return

        # CAPTURE MOVER COLOR BEFORE MOVE (critical!)
        mover_color = self.engine.current_player
        success, flips = self.engine.execute_move(coord)

        if success:
            # UPDATE DISPLAY IMMEDIATELY (shows new state)
            self._update_display()

            # START RIPPLE ANIMATION WITH PLACED COORDINATE
            self.board_widget.start_ripple_animation(coord, flips, mover_color)
            self._check_ai_turn()
        else:
            self.score_widget.show_error("Invalid move")

    def _check_ai_turn(self) -> None:
        """Check if current player is AI and make move."""
        if not self._active or self.engine.game_over:
            return

        current_player = self.engine.current_player

        if current_player not in self.players:
            return

        player = self.players[current_player]

        # Skip Human players - they wait for GUI input
        if isinstance(player, HumanPlayerAdapter):
            return

        valid_moves = self.engine.get_valid_moves(current_player)

        if not valid_moves:
            return

        # Run AI in separate thread
        thread = threading.Thread(target=self._make_ai_move, args=(player, valid_moves))
        thread.daemon = True
        thread.start()

    def _make_ai_move(
        self, player: IPlayer, valid_moves: list[tuple[int, int]]
    ) -> None:
        """Make AI move in separate thread."""
        if not valid_moves:
            return

        import time

        # Slower for easier difficulty, faster for harder
        delay = {"easy": 0.5, "medium": 0.3, "hard": 0.2}.get(player.difficulty, 0.3)
        time.sleep(delay)

        try:
            move = player.get_move(valid_moves)
            # Emit signal to main thread with the move
            self.ai_move_ready.emit(move)
        except Exception as e:
            print(f"AI move error: {e}")

    def _execute_ai_move(self, move: tuple[int, int]) -> None:
        if not self._active:
            return

        # CAPTURE MOVER COLOR BEFORE MOVE
        mover_color = self.engine.current_player
        success, flips = self.engine.execute_move(move)

        if success:
            # UPDATE DISPLAY IMMEDIATELY
            self._update_display()

            # START RIPPLE ANIMATION
            self.board_widget.start_ripple_animation(move, flips, mover_color)
            self._check_ai_turn()

    def customEvent(self, event) -> None:
        """Handle custom events from AI thread (no longer needed)."""
        pass

    def _update_display(self) -> None:
        """Update all UI components with current game state."""
        if not self._active:
            return

        board_state = {}
        for row in range(8):
            for col in range(8):
                board_state[(row, col)] = self.engine.board.get_cell(row, col)
        self.board_widget.update_board(board_state)

        valid_moves = self.engine.get_valid_moves(self.engine.current_player)
        self.board_widget.set_valid_moves(valid_moves)

        black_score = self.engine.get_score(PlayerColor.BLACK)
        white_score = self.engine.get_score(PlayerColor.WHITE)
        self.score_widget.update_scores(black_score, white_score)

        self.score_widget.set_turn(self.engine.current_player)

        if self.engine.game_over:
            winner = self.engine.get_winner()
            self.score_widget.show_game_over(winner)
            self.board_widget.clear_valid_moves()

    def set_players(self, players: dict[PlayerColor, IPlayer]) -> None:
        """Set player instances."""
        self.players = players

    def _on_new_game(self) -> None:
        """Handle new game button click."""
        if not self._active:
            return
        self.engine.reset()
        self._update_display()
        self._check_ai_turn()  # Trigger AI turn after reset

    def _on_quit(self) -> None:
        """Handle quit button click."""
        import sys

        sys.exit(0)

    def deactivate(self) -> None:
        """Deactivate controller (called on window close)."""
        self._active = False
        self.pass_timer.stop()
