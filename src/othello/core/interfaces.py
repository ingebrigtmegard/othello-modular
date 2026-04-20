"""Core Engine Interfaces"""

from abc import ABC, abstractmethod
from typing import List, Tuple


class IGameEngine(ABC):
    @abstractmethod
    def initialize(self) -> None:
        pass

    @abstractmethod
    def get_valid_moves(self, player: int) -> List[Tuple[int, int]]:
        pass

    @abstractmethod
    def execute_move(self, coord: Tuple[int, int]) -> bool:
        pass
