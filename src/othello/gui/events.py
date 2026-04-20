"""Event definitions for GUI-Engine communication."""

from enum import Enum
from typing import Optional


class GameEventType(Enum):
    """Types of game events."""

    MOVE_MADE = "move_made"
    TURN_CHANGED = "turn_changed"
    GAME_OVER = "game_over"
    PASS_OCCURRED = "pass_occurred"
    STATE_UPDATED = "state_updated"
    ERROR_INVALID_MOVE = "error_invalid_move"


class GameEvent:
    """
    Event class for communicating between Engine and GUI.

    Attributes:
        event_type: Type of event
        data: Optional event data (e.g., move coordinates, player info)
    """

    def __init__(self, event_type: GameEventType, data: Optional[dict] = None) -> None:
        """
        Initialize game event.

        Args:
            event_type: Type of event
            data: Optional event data
        """
        self.event_type = event_type
        self.data = data or {}

    def __str__(self) -> str:
        """String representation of event."""
        return f"GameEvent({self.event_type.value}, {self.data})"
