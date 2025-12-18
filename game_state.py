"""
Game state management for save/load functionality
"""

import json
import pickle
from datetime import datetime
from typing import Dict, Any, List
import os


class GameState:
    """Represents a game state for saving/loading"""
    
    def __init__(self, players_data: List[Dict], current_round: int, 
                 max_rounds: int, game_date: str = None):
        self.players_data = players_data
        self.current_round = current_round
        self.max_rounds = max_rounds
        self.game_date = game_date or datetime.now().isoformat()
        self.version = "1.0"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'players_data': self.players_data,
            'current_round': self.current_round,
            'max_rounds': self.max_rounds,
            'game_date': self.game_date,
            'version': self.version
        }
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), indent=2)
    
    def to_pickle(self) -> bytes:
        """Convert to pickle bytes"""
        return pickle.dumps(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Create from dictionary"""
        return cls(
            players_data=data['players_data'],
            current_round=data['current_round'],
            max_rounds=data['max_rounds'],
            game_date=data.get('game_date')
        )
    
    @classmethod
    def from_json(cls, json_str: str):
        """Create from JSON string"""
        data = json.loads(json_str)
        return cls.from_dict(data)


class GameStateManager:
    """Manages game state operations"""
    
    def __init__(self, save_dir: str = "saves"):
        self.save_dir = save_dir
        os.makedirs(save_dir, exist_ok=True)
    
    def save_game(self, game_state: GameState, filename: str = "save.json") -> str:
        """Save game state to file"""
        filepath = os.path.join(self.save_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(game_state.to_json())
        
        return filepath
    
    def load_game(self, filename: str = "save.json") -> GameState:
        """Load game state from file"""
        filepath = os.path.join(self.save_dir, filename)
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Save file not found: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            json_str = f.read()
        
        return GameState.from_json(json_str)
    
    def list_saves(self) -> List[str]:
        """List all save files"""
        if not os.path.exists(self.save_dir):
            return []
        
        saves = []
        for file in os.listdir(self.save_dir):
            if file.endswith('.json'):
                saves.append(file)
        
        return sorted(saves)