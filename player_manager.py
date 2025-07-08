"""
Player Manager for Python Learning Adventure
Handles player data, persistence, and leaderboard
"""

import json
import os
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

class Player:
    """Player class to store player data."""
    
    def __init__(self, name: str):
        self.id = str(uuid.uuid4())
        self.name = name
        self.current_level = 1
        self.player_level = 1
        self.total_xp = 0
        self.coins = 100  # Starting coins
        self.completed_levels = []
        self.level_stars = {}  # level_id -> stars (1-3)
        self.achievements = []
        self.purchased_rewards = []
        self.streak = 0
        self.last_play_date = None
        self.created_date = datetime.now().isoformat()
        self.total_playtime = 0
        self.test_scores = {}  # level_id -> score_percentage
    
    def update_streak(self):
        """Update the daily streak."""
        today = datetime.now().date()
        if self.last_play_date:
            last_date = datetime.fromisoformat(self.last_play_date).date()
            if today == last_date:
                return  # Already played today
            elif (today - last_date).days == 1:
                self.streak += 1
            else:
                self.streak = 1
        else:
            self.streak = 1
        
        self.last_play_date = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert player to dictionary for saving."""
        return {
            'id': self.id,
            'name': self.name,
            'current_level': self.current_level,
            'player_level': self.player_level,
            'total_xp': self.total_xp,
            'coins': self.coins,
            'completed_levels': self.completed_levels,
            'level_stars': self.level_stars,
            'achievements': self.achievements,
            'purchased_rewards': self.purchased_rewards,
            'streak': self.streak,
            'last_play_date': self.last_play_date,
            'created_date': self.created_date,
            'total_playtime': self.total_playtime,
            'test_scores': self.test_scores
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Player':
        """Create player from dictionary."""
        player = cls(data['name'])
        player.id = data.get('id', str(uuid.uuid4()))
        player.current_level = data.get('current_level', 1)
        player.player_level = data.get('player_level', 1)
        player.total_xp = data.get('total_xp', 0)
        player.coins = data.get('coins', 100)
        player.completed_levels = data.get('completed_levels', [])
        player.level_stars = data.get('level_stars', {})
        player.achievements = data.get('achievements', [])
        player.purchased_rewards = data.get('purchased_rewards', [])
        player.streak = data.get('streak', 0)
        player.last_play_date = data.get('last_play_date')
        player.created_date = data.get('created_date', datetime.now().isoformat())
        player.total_playtime = data.get('total_playtime', 0)
        player.test_scores = data.get('test_scores', {})
        return player

class PlayerManager:
    """Manages player data and persistence."""
    
    def __init__(self):
        self.players_dir = 'player_data'
        self.leaderboard_file = os.path.join(self.players_dir, 'leaderboard.json')
        self.ensure_directories()
    
    def ensure_directories(self):
        """Create necessary directories."""
        os.makedirs(self.players_dir, exist_ok=True)
    
    def create_or_get_player(self, name: str) -> Player:
        """Create a new player or get existing one by name."""
        # Check if player exists
        existing_player = self.get_player_by_name(name)
        if existing_player:
            existing_player.update_streak()
            self.save_player(existing_player)
            return existing_player
        
        # Create new player
        player = Player(name)
        player.update_streak()
        self.save_player(player)
        self.update_leaderboard(player)
        return player
    
    def get_player(self, player_id: str) -> Optional[Player]:
        """Get player by ID."""
        player_file = os.path.join(self.players_dir, f"{player_id}.json")
        
        if not os.path.exists(player_file):
            return None
        
        try:
            with open(player_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return Player.from_dict(data)
        except (json.JSONDecodeError, KeyError):
            return None
    
    def get_player_by_name(self, name: str) -> Optional[Player]:
        """Get player by name."""
        # This is inefficient for large numbers of players
        # In production, use a database with proper indexing
        for filename in os.listdir(self.players_dir):
            if filename.endswith('.json') and filename != 'leaderboard.json':
                try:
                    with open(os.path.join(self.players_dir, filename), 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if data.get('name') == name:
                            return Player.from_dict(data)
                except (json.JSONDecodeError, KeyError):
                    continue
        return None
    
    def save_player(self, player: Player):
        """Save player data to file."""
        player_file = os.path.join(self.players_dir, f"{player.id}.json")
        
        try:
            with open(player_file, 'w', encoding='utf-8') as f:
                json.dump(player.to_dict(), f, indent=2, ensure_ascii=False)
            
            # Update leaderboard
            self.update_leaderboard(player)
        except Exception as e:
            print(f"Error saving player {player.id}: {e}")
    
    def update_leaderboard(self, player: Player):
        """Update the leaderboard with player data."""
        leaderboard = self.get_leaderboard_data()
        
        # Update or add player entry
        player_entry = {
            'id': player.id,
            'name': player.name,
            'current_level': player.current_level,
            'player_level': player.player_level,
            'total_xp': player.total_xp,
            'coins': player.coins,
            'completed_levels': len(player.completed_levels),
            'total_stars': sum(player.level_stars.values()),
            'achievements': len(player.achievements),
            'streak': player.streak,
            'last_play_date': player.last_play_date
        }
        
        # Remove existing entry if present
        leaderboard = [entry for entry in leaderboard if entry['id'] != player.id]
        
        # Add updated entry
        leaderboard.append(player_entry)
        
        # Sort by multiple criteria
        leaderboard.sort(key=lambda x: (
            x['current_level'],
            x['total_xp'],
            x['total_stars'],
            x['completed_levels']
        ), reverse=True)
        
        # Keep only top 100
        leaderboard = leaderboard[:100]
        
        # Save leaderboard
        try:
            with open(self.leaderboard_file, 'w', encoding='utf-8') as f:
                json.dump(leaderboard, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error updating leaderboard: {e}")
    
    def get_leaderboard_data(self) -> List[Dict[str, Any]]:
        """Get leaderboard data."""
        if not os.path.exists(self.leaderboard_file):
            return []
        
        try:
            with open(self.leaderboard_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def get_leaderboard(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top players for leaderboard."""
        leaderboard = self.get_leaderboard_data()
        
        # Add ranking
        for i, entry in enumerate(leaderboard[:limit], 1):
            entry['rank'] = i
        
        return leaderboard[:limit]
    
    def get_player_rank(self, player_id: str) -> Optional[int]:
        """Get player's rank in leaderboard."""
        leaderboard = self.get_leaderboard_data()
        
        for i, entry in enumerate(leaderboard, 1):
            if entry['id'] == player_id:
                return i
        
        return None
    
    def get_all_players(self) -> List[Player]:
        """Get all players (for admin purposes)."""
        players = []
        
        for filename in os.listdir(self.players_dir):
            if filename.endswith('.json') and filename != 'leaderboard.json':
                try:
                    with open(os.path.join(self.players_dir, filename), 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        players.append(Player.from_dict(data))
                except (json.JSONDecodeError, KeyError):
                    continue
        
        return players
    
    def delete_player(self, player_id: str) -> bool:
        """Delete a player (for admin purposes)."""
        player_file = os.path.join(self.players_dir, f"{player_id}.json")
        
        if os.path.exists(player_file):
            try:
                os.remove(player_file)
                
                # Remove from leaderboard
                leaderboard = self.get_leaderboard_data()
                leaderboard = [entry for entry in leaderboard if entry['id'] != player_id]
                
                with open(self.leaderboard_file, 'w', encoding='utf-8') as f:
                    json.dump(leaderboard, f, indent=2, ensure_ascii=False)
                
                return True
            except Exception as e:
                print(f"Error deleting player {player_id}: {e}")
                return False
        
        return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get general statistics."""
        players = self.get_all_players()
        
        if not players:
            return {
                'total_players': 0,
                'active_players': 0,
                'total_levels_completed': 0,
                'total_xp_earned': 0,
                'average_level': 0,
                'top_streak': 0
            }
        
        # Calculate statistics
        total_players = len(players)
        
        # Active players (played in last 7 days)
        active_players = 0
        week_ago = datetime.now() - timedelta(days=7)
        
        for player in players:
            if player.last_play_date:
                last_play = datetime.fromisoformat(player.last_play_date)
                if last_play >= week_ago:
                    active_players += 1
        
        total_levels_completed = sum(len(player.completed_levels) for player in players)
        total_xp_earned = sum(player.total_xp for player in players)
        average_level = sum(player.current_level for player in players) / total_players
        top_streak = max(player.streak for player in players) if players else 0
        
        return {
            'total_players': total_players,
            'active_players': active_players,
            'total_levels_completed': total_levels_completed,
            'total_xp_earned': total_xp_earned,
            'average_level': round(average_level, 2),
            'top_streak': top_streak
        }
