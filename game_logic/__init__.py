"""
Game Logic Package
Modular game logic system for Python Learning Adventure

This package provides a comprehensive, modular game logic system with the following components:

- achievements.py: Achievement tracking, unlocking, and reward processing
- level_loader.py: Sequential loading of levels and progression management  
- animations.py: Game animations and smooth rendering transitions
- player_state.py: Player data management and state persistence
- event_dispatcher.py: Event handling and system-wide communication
- coordinator.py: Main coordinator that integrates all modules

Usage:
    from game_logic import GameLogicCoordinator
    
    # Initialize the game logic system
    game = GameLogicCoordinator()
    
    # Create or load a player
    player = game.create_player("username")
    
    # Get level data and complete levels
    level_data = game.get_level_data(1, player)
    result = game.complete_level(player, 1, [1, 0, 2])  # Quiz answers
    
    # Manage achievements and rewards
    achievements = game.get_player_achievements(player)
    rewards = game.get_available_rewards(player)
"""

from .coordinator import GameLogicCoordinator, AdvancedGameLogic
from .achievements import AchievementManager
from .level_loader import LevelLoader
from .animations import AnimationController, AnimationManager
from .player_state import PlayerStateManager, PlayerState, PlayerStats
from .event_dispatcher import GameEventManager, EventDispatcher, EventType, Event

# Version information
__version__ = "2.0.0"
__author__ = "Python Learning Adventure Team"

# Public API
__all__ = [
    # Main classes
    "GameLogicCoordinator",
    "AdvancedGameLogic",  # Backward compatibility
    
    # Component managers
    "AchievementManager",
    "LevelLoader", 
    "AnimationController",
    "AnimationManager",
    "PlayerStateManager",
    "GameEventManager",
    
    # Data structures
    "PlayerState",
    "PlayerStats",
    "Event",
    "EventType",
    "EventDispatcher",
]

# Default configurations
DEFAULT_CONFIG = {
    'data_directory': 'player_data',
    'fast_animations': False,
    'auto_save': True,
    'event_logging': True,
    'performance_tracking': True
}

from typing import Optional

def create_game_logic(config: Optional[dict] = None) -> GameLogicCoordinator:
    """
    Factory function to create a configured GameLogicCoordinator instance.
    
    Args:
        config: Optional configuration dictionary
        
    Returns:
        Configured GameLogicCoordinator instance
    """
    if config is None:
        config = DEFAULT_CONFIG.copy()
    else:
        # Merge with defaults
        merged_config = DEFAULT_CONFIG.copy()
        merged_config.update(config)
        config = merged_config
    
    # Create coordinator with configuration
    coordinator = GameLogicCoordinator(
        data_directory=config.get('data_directory', 'player_data')
    )
    
    # Apply configuration settings
    if config.get('fast_animations', False):
        coordinator.animation_controller.set_fast_mode(True)
    
    return coordinator

def get_version_info() -> dict:
    """Get version and component information."""
    return {
        'version': __version__,
        'author': __author__,
        'components': {
            'achievements': 'Achievement tracking and rewards',
            'level_loader': 'Level management and progression',
            'animations': 'Game animations and transitions',
            'player_state': 'Player data and persistence',
            'event_dispatcher': 'Event handling and communication',
            'coordinator': 'Main system coordinator'
        },
        'features': [
            'Modular architecture',
            'Event-driven design', 
            'Performance optimization',
            'Comprehensive achievement system',
            'Adaptive level progression',
            'Smooth animations',
            'Player state persistence',
            'Real-time statistics'
        ]
    }
