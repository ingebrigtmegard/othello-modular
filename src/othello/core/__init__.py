"""Core engine package."""

from .core.board import Board
from .core.constants import BoardSize, PlayerColor
from .core.engine import IEngineObserver, OthelloEngine
from .core.events import EngineEvent, EngineEventType
from .core.rules import RulesValidator

__all__ = [
    "PlayerColor",
    "BoardSize",
    "Board",
    "RulesValidator",
    "OthelloEngine",
    "IEngineObserver",
    "EngineEvent",
    "EngineEventType",
]
