"""Event definitions for Othello Engine."""

from enum import Enum
from typing import Optional


class EngineEventType(Enum):
    """Types of engine events."""

    MOVE_MADE = "move_made"
    PASS_OCCURRED = "pass_occurred"
    GAME_OVER = "game_over"
    STATE_UPDATED = "state_updated"


class EngineEvent:
    """
    Event class for engine-to-controller communication.

    Attributes:
        event_type: Type of event
        data: Optional event data
    """

    def __init__(
        self, event_type: EngineEventType, data: Optional[dict] = None
    ) -> None:
        """
        Initialize engine event.

        Args:
            event_type: Type of event
            data: Optional event data
        """
        self.event_type = event_type
        self.data = data or {}

    def __str__(self) -> str:
        """String representation of event."""
        return f"EngineEvent({self.event_type.value}, {self.data})"
