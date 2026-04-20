"""Game engine module - manages game state and flow."""

from typing import Dict, List, Optional, Protocol, Tuple, runtime_checkable

from .board import Board
from .constants import BoardSize, PlayerColor
from .events import EngineEvent, EngineEventType
from .rules import RulesValidator


@runtime_checkable
class IEngineObserver(Protocol):
    """Protocol for engine observers (duck typing instead of ABC)."""

    def on_engine_event(self, event: EngineEvent) -> None:
        """
        Handle engine event.

        Args:
            event: Engine event
        """
        ...


class OthelloEngine:
    """
    Main game engine managing state, turns, and rules.

    Attributes:
        board: Current game board
        current_player: Player whose turn it is
        valid_moves_cache: Cached valid moves for both players
        game_over: Game termination flag
        observers: List of observers to notify of events
    """

    def __init__(self) -> None:
        """Initialize the game engine."""
        self.board = Board()
        self.current_player = PlayerColor.BLACK
        self.valid_moves_cache: Dict[PlayerColor, List[Tuple[int, int]]] = {
            PlayerColor.BLACK: [],
            PlayerColor.WHITE: [],
        }
        self.game_over = False
        self.validator = RulesValidator()
        self.observers: List[IEngineObserver] = []

        # Initial valid moves calculation
        self._recalculate_valid_moves()

    def add_observer(self, observer: IEngineObserver) -> None:
        """
        Add an observer to the engine.

        Args:
            observer: Engine observer instance
        """
        if observer not in self.observers:
            self.observers.append(observer)

    def remove_observer(self, observer: IEngineObserver) -> None:
        """
        Remove an observer from the engine.

        Args:
            observer: Engine observer instance
        """
        if observer in self.observers:
            self.observers.remove(observer)

    def _emit_event(self, event: EngineEvent) -> None:
        """
        Emit event to all observers.

        Args:
            event: Engine event to emit
        """
        for observer in self.observers:
            observer.on_engine_event(event)

    def _recalculate_valid_moves(self) -> None:
        """Recalculate valid moves for both players."""
        self.valid_moves_cache[PlayerColor.BLACK] = []
        self.valid_moves_cache[PlayerColor.WHITE] = []

        for r in range(BoardSize.ROWS):
            for c in range(BoardSize.COLS):
                if self.board.is_empty(r, c):
                    if self.validator.is_valid_move(
                        self.board, r, c, PlayerColor.BLACK
                    ):
                        self.valid_moves_cache[PlayerColor.BLACK].append((r, c))
                    if self.validator.is_valid_move(
                        self.board, r, c, PlayerColor.WHITE
                    ):
                        self.valid_moves_cache[PlayerColor.WHITE].append((r, c))

    def get_valid_moves(self, player: PlayerColor) -> List[Tuple[int, int]]:
        """
        Get the cached list of valid moves for a player.

        Args:
            player: Player color

        Returns:
            List of (row, col) tuples
        """
        return self.valid_moves_cache[player]

    def execute_move(self, coord: Tuple[int, int]) -> Tuple[bool, List[Tuple[int, int]]]:
        """
        Execute a move at the given coordinate.

        Args:
            coord: (row, col) tuple

        Returns:
            Tuple of (success: bool, flips: List[Tuple[int, int]])
        """
        if self.game_over:
            return False, []

        row, col = coord

        # Check if move is valid
        if not self.validator.is_valid_move(self.board, row, col, self.current_player):
            return False, []

        # Execute the flip AND GET THE FLIPS
        flips = self.validator.flip_discs(self.board, row, col, self.current_player)

        # Recalculate valid moves
        self._recalculate_valid_moves()

        # Always switch turn to opponent after a valid move
        self.current_player = self._get_opponent(self.current_player)

        # Check game end conditions (includes auto-pass logic)
        self._check_game_end()

        # Emit state updated event
        self._emit_event(EngineEvent(EngineEventType.STATE_UPDATED))

        return True, flips

    def _check_game_end(self) -> None:
        """
        Check if game should end (double pass).
        Handles automatic pass when current player has no moves.

        Note: Board full scenario is handled naturally by double-pass logic
        since both players will have no valid moves when board is full.
        """
        if self.game_over:
            return

        # Check if current player has no moves
        current_moves = len(self.valid_moves_cache[self.current_player])

        if current_moves == 0:
            # Current player must pass, switch to opponent
            self.current_player = self._get_opponent(self.current_player)

            # Emit pass event BEFORE checking if game over
            self._emit_event(
                EngineEvent(
                    EngineEventType.PASS_OCCURRED,
                    {"player": self.current_player, "message": "Pass"},
                )
            )

            # Check if opponent also has no moves (double pass = game over)
            opponent_moves = len(self.valid_moves_cache[self.current_player])

            if opponent_moves == 0:
                self.game_over = True
                self._emit_event(EngineEvent(EngineEventType.GAME_OVER))

    def _get_opponent(self, player: PlayerColor) -> PlayerColor:
        """Get the opponent color."""
        return PlayerColor.WHITE if player == PlayerColor.BLACK else PlayerColor.BLACK

    def get_score(self, player: PlayerColor) -> int:
        """
        Count discs for a player.

        Args:
            player: Player color

        Returns:
            Number of discs
        """
        count = 0
        for r in range(BoardSize.ROWS):
            for c in range(BoardSize.COLS):
                if self.board.get_cell(r, c) == player:
                    count += 1
        return count

    def get_winner(self) -> Optional[PlayerColor]:
        """
        Determine the winner (only call when game_over is True).

        Returns:
            PlayerColor of winner or None for draw
        """
        if not self.game_over:
            return None

        black_score = self.get_score(PlayerColor.BLACK)
        white_score = self.get_score(PlayerColor.WHITE)

        if black_score > white_score:
            return PlayerColor.BLACK
        elif white_score > black_score:
            return PlayerColor.WHITE
        else:
            return None

    def reset(self) -> None:
        """Reset the game to initial state."""
        self.board = Board()
        self.current_player = PlayerColor.BLACK
        self.game_over = False
        self._recalculate_valid_moves()
        self._emit_event(EngineEvent(EngineEventType.STATE_UPDATED))
