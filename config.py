"""
Configuration module for game settings
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class GameConfig:
    """Game configuration settings"""
    max_players: int = 4
    min_players: int = 2
    max_rounds: int = 10
    min_rounds: int = 3
    dice_count: int = 12
    rolls_per_turn: int = 3
    use_official_rules: bool = True
    enable_challenges: bool = False
    auto_save: bool = True
    visualization_enabled: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'max_players': self.max_players,
            'min_players': self.min_players,
            'max_rounds': self.max_rounds,
            'min_rounds': self.min_rounds,
            'dice_count': self.dice_count,
            'rolls_per_turn': self.rolls_per_turn,
            'use_official_rules': self.use_official_rules,
            'enable_challenges': self.enable_challenges,
            'auto_save': self.auto_save,
            'visualization_enabled': self.visualization_enabled
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Create from dictionary"""
        return cls(**{k: v for k, v in data.items() if hasattr(cls, k)})


class ConfigManager:
    """Manages configuration loading and saving"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.default_config = GameConfig()
    
    def load_config(self) -> GameConfig:
        """Load configuration from file"""
        import json
        import os
        
        if not os.path.exists(self.config_file):
            return self.default_config
        
        try:
            with open(self.config_file, 'r') as f:
                data = json.load(f)
            return GameConfig.from_dict(data)
        except:
            return self.default_config
    
    def save_config(self, config: GameConfig):
        """Save configuration to file"""
        import json
        
        with open(self.config_file, 'w') as f:
            json.dump(config.to_dict(), f, indent=2)
    
    def get_default_config(self) -> GameConfig:
        """Get default configuration"""
        return self.default_config