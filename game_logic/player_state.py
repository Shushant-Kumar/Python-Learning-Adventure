"""
Player State Management Module
Handles player data, progress tracking, and state persistence
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, TYPE_CHECKING
from dataclasses import dataclass, asdict
import uuid

if TYPE_CHECKING:
    from typing import Self


@dataclass
class PlayerStats:
    """Player statistics data structure."""
    levels_completed: List[int]
    total_score: float
    total_xp: int
    total_coins: int
    learning_streak: int
    total_time_spent: int  # in seconds
    average_score: float
    perfect_scores: int
    achievements_count: int
    last_active: str


class PlayerStateManager:
    """Manages player state, progress, and persistence."""
    
    def __init__(self, data_directory: str = "player_data"):
        self.data_directory = data_directory
        self.ensure_data_directory()
        self.session_start_time = datetime.now()
        
    def ensure_data_directory(self):
        """Ensure the player data directory exists."""
        if not os.path.exists(self.data_directory):
            os.makedirs(self.data_directory)
    
    def create_new_player(self, username: str) -> 'PlayerState':
        """Create a new player with default values."""
        player_id = str(uuid.uuid4())
        
        player = PlayerState(
            id=player_id,
            username=username,
            created_at=datetime.now().isoformat(),
            last_login=datetime.now().isoformat()
        )
        
        self.save_player(player)
        return player
    
    def load_player(self, player_id: str) -> Optional['PlayerState']:
        """Load player data from file."""
        file_path = os.path.join(self.data_directory, f"{player_id}.json")
        
        if not os.path.exists(file_path):
            return None
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            player = PlayerState.from_dict(data)
            player.last_login = datetime.now().isoformat()
            self.save_player(player)  # Update last login
            
            return player
        except (json.JSONDecodeError, IOError, KeyError) as e:
            print(f"Error loading player {player_id}: {e}")
            return None
    
    def save_player(self, player: 'PlayerState'):
        """Save player data to file."""
        file_path = os.path.join(self.data_directory, f"{player.id}.json")
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(player.to_dict(), f, indent=2, ensure_ascii=False)
        except (IOError, TypeError) as e:
            print(f"Error saving player {player.id}: {e}")
    
    def update_player_progress(self, player: 'PlayerState', level_id: int, 
                             score: float, time_taken: int, passed: bool) -> Dict[str, Any]:
        """Update player progress after completing a level."""
        # Add to performance history
        performance_record = {
            'level_id': level_id,
            'score_percentage': score,
            'time_taken': time_taken,
            'passed': passed,
            'timestamp': datetime.now().isoformat(),
            'session_id': self.get_current_session_id()
        }
        
        player.performance_history.append(performance_record)
        
        # Update completed levels if passed
        if passed and level_id not in player.completed_levels:
            player.completed_levels.append(level_id)
        
        # Update learning streak
        self.update_learning_streak(player)
        
        # Update totals
        player.total_time_spent += time_taken
        
        # Recalculate statistics
        self.recalculate_player_stats(player)
        
        # Save updated state
        self.save_player(player)
        
        return {
            'level_completed': passed,
            'new_best_score': self.is_new_best_score(player, level_id, score),
            'streak_updated': True,
            'total_time': player.total_time_spent
        }
    
    def update_learning_streak(self, player: 'PlayerState'):
        """Update the player's learning streak."""
        today = datetime.now().date()
        
        if not player.performance_history:
            player.learning_streak = 1
            player.last_activity_date = today.isoformat()
            return
        
        # Get the last activity date
        last_activity = player.last_activity_date
        if last_activity:
            last_date = datetime.fromisoformat(last_activity).date()
            
            if last_date == today:
                # Already counted today
                return
            elif last_date == today - timedelta(days=1):
                # Consecutive day
                player.learning_streak += 1
            else:
                # Streak broken
                player.learning_streak = 1
        else:
            player.learning_streak = 1
        
        player.last_activity_date = today.isoformat()
    
    def is_new_best_score(self, player: 'PlayerState', level_id: int, score: float) -> bool:
        """Check if this is a new best score for the level."""
        level_scores = [
            record['score_percentage'] 
            for record in player.performance_history 
            if record.get('level_id') == level_id
        ]
        
        if not level_scores:
            return True
        
        return score > max(level_scores[:-1]) if len(level_scores) > 1 else True
    
    def recalculate_player_stats(self, player: 'PlayerState'):
        """Recalculate all player statistics."""
        if not player.performance_history:
            return
        
        scores = [record['score_percentage'] for record in player.performance_history]
        passed_levels = [record for record in player.performance_history if record.get('passed', False)]
        
        # Basic stats
        player.total_score = sum(scores)
        player.average_score = player.total_score / len(scores) if scores else 0
        player.perfect_scores = len([s for s in scores if s == 100])
        
        # Level completion stats
        completed_level_ids = list(set(
            record['level_id'] for record in passed_levels
        ))
        # Store the count of completed levels, not the list
        player.completed_levels = completed_level_ids if hasattr(player, 'completed_levels') else []
        
        # Update level stars based on best scores
        player.level_stars = {}
        for level_id in set(record['level_id'] for record in player.performance_history):
            level_scores = [
                record['score_percentage'] 
                for record in player.performance_history 
                if record['level_id'] == level_id and record.get('passed', False)
            ]
            
            if level_scores:
                best_score = max(level_scores)
                if best_score >= 90:
                    stars = 3
                elif best_score >= 80:
                    stars = 2
                elif best_score >= 70:
                    stars = 1
                else:
                    stars = 0
                
                player.level_stars[str(level_id)] = stars
    
    def get_player_stats(self, player: 'PlayerState') -> PlayerStats:
        """Get comprehensive player statistics."""
        completed_levels = list(set(
            record['level_id'] 
            for record in player.performance_history 
            if record.get('passed', False)
        ))
        
        return PlayerStats(
            levels_completed=completed_levels,
            total_score=player.total_score,
            total_xp=player.total_xp,
            total_coins=player.total_coins,
            learning_streak=player.learning_streak,
            total_time_spent=player.total_time_spent,
            average_score=player.average_score,
            perfect_scores=player.perfect_scores,
            achievements_count=len(player.achievements),
            last_active=player.last_login
        )
    
    def get_current_session_id(self) -> str:
        """Get current session identifier."""
        return f"session_{self.session_start_time.strftime('%Y%m%d_%H%M%S')}"
    
    def get_player_preferences(self, player: 'PlayerState') -> Dict[str, Any]:
        """Get player preferences and settings."""
        return {
            'fast_animations': player.preferences.get('fast_animations', False),
            'sound_enabled': player.preferences.get('sound_enabled', True),
            'theme': player.preferences.get('theme', 'default'),
            'difficulty_preference': player.preferences.get('difficulty_preference', 'adaptive'),
            'hint_frequency': player.preferences.get('hint_frequency', 'normal')
        }
    
    def update_player_preferences(self, player: 'PlayerState', preferences: Dict[str, Any]):
        """Update player preferences."""
        player.preferences.update(preferences)
        self.save_player(player)
    
    def backup_player_data(self, player: 'PlayerState') -> str:
        """Create a backup of player data."""
        backup_dir = os.path.join(self.data_directory, "backups")
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = os.path.join(backup_dir, f"{player.id}_backup_{timestamp}.json")
        
        try:
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(player.to_dict(), f, indent=2, ensure_ascii=False)
            return backup_file
        except (IOError, TypeError) as e:
            print(f"Error creating backup: {e}")
            return ""
    
    def get_leaderboard_data(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get leaderboard data from all players."""
        leaderboard = []
        
        if not os.path.exists(self.data_directory):
            return leaderboard
        
        for filename in os.listdir(self.data_directory):
            if filename.endswith('.json') and not filename.startswith('backup'):
                file_path = os.path.join(self.data_directory, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        player_data = json.load(f)
                    
                    leaderboard.append({
                        'username': player_data.get('username', 'Unknown'),
                        'total_xp': player_data.get('total_xp', 0),
                        'levels_completed': len(player_data.get('completed_levels', [])),
                        'achievements': len(player_data.get('achievements', [])),
                        'learning_streak': player_data.get('learning_streak', 0),
                        'average_score': player_data.get('average_score', 0)
                    })
                except (json.JSONDecodeError, IOError, KeyError) as e:
                    print(f"Error reading player data from {filename}: {e}")
                    continue
        
        # Sort by total XP and return top players
        leaderboard.sort(key=lambda x: x['total_xp'], reverse=True)
        return leaderboard[:limit]


class PlayerState:
    """Player state class that holds all player data."""
    
    def __init__(self, id: str, username: str, created_at: str, last_login: str):
        self.id = id
        self.username = username
        self.created_at = created_at
        self.last_login = last_login
        self.last_activity_date: Optional[str] = None
        
        # Progress tracking
        self.completed_levels = []
        self.current_level = 1
        self.performance_history = []
        self.level_stars = {}
        self.level_attempts = {}
        
        # Statistics
        self.total_score = 0.0
        self.total_xp = 0
        self.total_coins = 0
        self.learning_streak = 0
        self.total_time_spent = 0
        self.average_score = 0.0
        self.perfect_scores = 0
        
        # Achievements and rewards
        self.achievements = []
        self.purchased_rewards = []
        
        # Preferences and settings
        self.preferences = {
            'fast_animations': False,
            'sound_enabled': True,
            'theme': 'default',
            'difficulty_preference': 'adaptive',
            'hint_frequency': 'normal'
        }
        
        # Learning analytics
        self.learning_style = 'balanced'  # visual, practical, theoretical, balanced
        self.weak_topics = []
        self.strong_topics = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert player state to dictionary for serialization."""
        return {
            'id': self.id,
            'username': self.username,
            'created_at': self.created_at,
            'last_login': self.last_login,
            'last_activity_date': self.last_activity_date,
            'completed_levels': self.completed_levels,
            'current_level': self.current_level,
            'performance_history': self.performance_history,
            'level_stars': self.level_stars,
            'level_attempts': self.level_attempts,
            'total_score': self.total_score,
            'total_xp': self.total_xp,
            'total_coins': self.total_coins,
            'learning_streak': self.learning_streak,
            'total_time_spent': self.total_time_spent,
            'average_score': self.average_score,
            'perfect_scores': self.perfect_scores,
            'achievements': self.achievements,
            'purchased_rewards': self.purchased_rewards,
            'preferences': self.preferences,
            'learning_style': self.learning_style,
            'weak_topics': self.weak_topics,
            'strong_topics': self.strong_topics
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PlayerState':
        """Create PlayerState from dictionary."""
        player = cls(
            id=data.get('id', ''),
            username=data.get('username', ''),
            created_at=data.get('created_at', ''),
            last_login=data.get('last_login', '')
        )
        
        # Load all attributes
        player.last_activity_date = data.get('last_activity_date')
        player.completed_levels = data.get('completed_levels', [])
        player.current_level = data.get('current_level', 1)
        player.performance_history = data.get('performance_history', [])
        player.level_stars = data.get('level_stars', {})
        player.level_attempts = data.get('level_attempts', {})
        player.total_score = data.get('total_score', 0.0)
        player.total_xp = data.get('total_xp', 0)
        player.total_coins = data.get('total_coins', 0)
        player.learning_streak = data.get('learning_streak', 0)
        player.total_time_spent = data.get('total_time_spent', 0)
        player.average_score = data.get('average_score', 0.0)
        player.perfect_scores = data.get('perfect_scores', 0)
        player.achievements = data.get('achievements', [])
        player.purchased_rewards = data.get('purchased_rewards', [])
        player.preferences = data.get('preferences', {
            'fast_animations': False,
            'sound_enabled': True,
            'theme': 'default',
            'difficulty_preference': 'adaptive',
            'hint_frequency': 'normal'
        })
        player.learning_style = data.get('learning_style', 'balanced')
        player.weak_topics = data.get('weak_topics', [])
        player.strong_topics = data.get('strong_topics', [])
        
        return player
    
    def add_xp(self, amount: int):
        """Add XP to player total."""
        self.total_xp += amount
    
    def add_coins(self, amount: int):
        """Add coins to player total."""
        self.total_coins += amount
    
    def spend_coins(self, amount: int) -> bool:
        """Spend coins if available."""
        if self.total_coins >= amount:
            self.total_coins -= amount
            return True
        return False
    
    def get_level_best_score(self, level_id: int) -> float:
        """Get best score for a specific level."""
        level_scores = [
            record['score_percentage'] 
            for record in self.performance_history 
            if record.get('level_id') == level_id
        ]
        return max(level_scores) if level_scores else 0.0
    
    def get_topic_performance(self, topic: str) -> Dict[str, Any]:
        """Get performance statistics for a specific topic."""
        topic_records = [
            record for record in self.performance_history 
            if topic.lower() in record.get('topic', '').lower()
        ]
        
        if not topic_records:
            return {'average_score': 0, 'attempts': 0, 'best_score': 0}
        
        scores = [record['score_percentage'] for record in topic_records]
        return {
            'average_score': sum(scores) / len(scores),
            'attempts': len(topic_records),
            'best_score': max(scores),
            'improvement_trend': self._calculate_improvement_trend(topic_records)
        }
    
    def _calculate_improvement_trend(self, records: List[Dict[str, Any]]) -> str:
        """Calculate if player is improving in a topic."""
        if len(records) < 3:
            return 'insufficient_data'
        
        recent_scores = [r['score_percentage'] for r in records[-3:]]
        older_scores = [r['score_percentage'] for r in records[:-3]]
        
        if not older_scores:
            return 'insufficient_data'
        
        recent_avg = sum(recent_scores) / len(recent_scores)
        older_avg = sum(older_scores) / len(older_scores)
        
        if recent_avg > older_avg + 5:
            return 'improving'
        elif recent_avg < older_avg - 5:
            return 'declining'
        else:
            return 'stable'
