# src/othello/core/game_state.py

import json
from dataclasses import dataclass, asdict
from typing import Dict, List, Tuple

from .core.constants import PlayerColor

@dataclass
class GameSave:
    """Serializable game state."""
    board: List[List[int]]
    current_player: int
    black_score: int
    white_score: int
    game_over: bool
    last_move: Tuple[int, int]

class GameStateManager:
    """Manages save/load functionality."""
    
    @staticmethod
    def save_game(engine: 'OthelloEngine', filepath: str) -> bool:
        """Save game state to JSON file."""
        try:
            save_data = GameSave(
                board=engine.board.to_list(),
                current_player=engine.current_player.value,
                black_score=engine.get_score(PlayerColor.BLACK),
                white_score=engine.get_score(PlayerColor.WHITE),
                game_over=engine.game_over,
                last_move=engine.last_move if hasattr(engine, 'last_move') else (0, 0)
            )
            with open(filepath, 'w') as f:
                json.dump(asdict(save_data), f)
            return True
        except Exception as e:
            print(f"Save error: {e}")
            return False
    
    @staticmethod
    def load_game(engine: 'OthelloEngine', filepath: str) -> bool:
        """Load game state from JSON file."""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            # Rebuild board
            for r in range(8):
                for c in range(8):
                    engine.board.set_cell(r, c, PlayerColor(data['board'][r][c]))
            
            engine.current_player = PlayerColor(data['current_player'])
            engine.game_over = data['game_over']
            engine.last_move = tuple(data['last_move'])
            
            engine._recalculate_valid_moves()
            return True
        except Exception as e:
            print(f"Load error: {e}")
            return False
