"""
Achievement System Module
Handles achievement tracking, unlocking, and reward processing
"""

from datetime import datetime
from typing import List, Dict, Any, Optional
import json


class AchievementManager:
    """Manages player achievements and rewards."""
    
    def __init__(self):
        self.achievement_definitions = self._load_achievement_definitions()
        self.reward_calculations = {
            'bronze': {'coins': 50, 'xp': 25},
            'silver': {'coins': 100, 'xp': 50},
            'gold': {'coins': 200, 'xp': 100},
            'platinum': {'coins': 500, 'xp': 250}
        }
    
    def _load_achievement_definitions(self) -> List[Dict[str, Any]]:
        """Load all available achievement definitions."""
        return [
            {
                'id': 'first_steps',
                'name': 'First Steps',
                'description': 'Complete your first level',
                'condition': 'levels_completed >= 1',
                'tier': 'bronze',
                'icon': '🏁',
                'hidden': False
            },
            {
                'id': 'getting_started', 
                'name': 'Getting Started',
                'description': 'Complete 5 levels',
                'condition': 'levels_completed >= 5',
                'tier': 'bronze',
                'icon': '🚀',
                'hidden': False
            },
            {
                'id': 'python_enthusiast',
                'name': 'Python Enthusiast',
                'description': 'Complete 10 levels',
                'condition': 'levels_completed >= 10',
                'tier': 'silver',
                'icon': '🐍',
                'hidden': False
            },
            {
                'id': 'code_warrior',
                'name': 'Code Warrior',
                'description': 'Complete 25 levels',
                'condition': 'levels_completed >= 25',
                'tier': 'gold',
                'icon': '⚔️',
                'hidden': False
            },
            {
                'id': 'python_master',
                'name': 'Python Master',
                'description': 'Complete 50 levels',
                'condition': 'levels_completed >= 50',
                'tier': 'platinum',
                'icon': '👑',
                'hidden': False
            },
            {
                'id': 'perfectionist',
                'name': 'Perfectionist',
                'description': 'Get a perfect score on any level',
                'condition': 'perfect_scores >= 1',
                'tier': 'silver',
                'icon': '💯',
                'hidden': False
            },
            {
                'id': 'streak_master',
                'name': 'Streak Master',
                'description': 'Maintain a 7-day learning streak',
                'condition': 'learning_streak >= 7',
                'tier': 'gold',
                'icon': '🔥',
                'hidden': False
            },
            {
                'id': 'speed_demon',
                'name': 'Speed Demon',
                'description': 'Complete a level in under 2 minutes',
                'condition': 'fast_completion >= 1',
                'tier': 'silver',
                'icon': '⚡',
                'hidden': False
            },
            {
                'id': 'dedicated_learner',
                'name': 'Dedicated Learner',
                'description': 'Spend over 10 hours learning',
                'condition': 'total_time_hours >= 10',
                'tier': 'gold',
                'icon': '📚',
                'hidden': False
            },
            {
                'id': 'challenge_conqueror',
                'name': 'Challenge Conqueror',
                'description': 'Complete all challenge levels',
                'condition': 'challenge_levels_completed >= 4',
                'tier': 'platinum',
                'icon': '🏆',
                'hidden': False
            },
            {
                'id': 'night_owl',
                'name': 'Night Owl',
                'description': 'Complete levels after 10 PM',
                'condition': 'night_completions >= 5',
                'tier': 'bronze',
                'icon': '🦉',
                'hidden': True
            },
            {
                'id': 'early_bird',
                'name': 'Early Bird',
                'description': 'Complete levels before 7 AM',
                'condition': 'early_completions >= 5',
                'tier': 'bronze',
                'icon': '🐦',
                'hidden': True
            }
        ]
    
    def get_player_achievements(self, player) -> List[Dict[str, Any]]:
        """Get all achievements for a player."""
        return getattr(player, 'achievements', [])
    
    def check_new_achievements(self, player) -> List[Dict[str, Any]]:
        """Check for newly earned achievements."""
        current_achievements = self.get_player_achievements(player)
        current_ids = [ach.get('id') if isinstance(ach, dict) else ach for ach in current_achievements]
        
        new_achievements = []
        player_stats = self._calculate_player_stats(player)
        
        for achievement in self.achievement_definitions:
            if achievement['id'] not in current_ids:
                if self._check_achievement_condition(achievement, player_stats):
                    earned_achievement = self._create_earned_achievement(achievement)
                    new_achievements.append(earned_achievement)
        
        return new_achievements
    
    def award_achievements(self, player, new_achievements: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Award new achievements to player and calculate rewards."""
        if not new_achievements:
            return {'achievements_added': 0, 'total_rewards': {'coins': 0, 'xp': 0}}
        
        # Add achievements to player
        if not hasattr(player, 'achievements'):
            player.achievements = []
        
        total_rewards = {'coins': 0, 'xp': 0}
        
        for achievement in new_achievements:
            player.achievements.append(achievement)
            
            # Calculate rewards
            tier = achievement.get('tier', 'bronze')
            rewards = self.reward_calculations.get(tier, self.reward_calculations['bronze'])
            total_rewards['coins'] += rewards['coins']
            total_rewards['xp'] += rewards['xp']
        
        # Update player totals
        if hasattr(player, 'total_coins'):
            player.total_coins = getattr(player, 'total_coins', 0) + total_rewards['coins']
        if hasattr(player, 'total_xp'):
            player.total_xp = getattr(player, 'total_xp', 0) + total_rewards['xp']
        
        return {
            'achievements_added': len(new_achievements),
            'new_achievements': new_achievements,
            'total_rewards': total_rewards
        }
    
    def _calculate_player_stats(self, player) -> Dict[str, Any]:
        """Calculate comprehensive player statistics for achievement checking."""
        completed_levels = getattr(player, 'completed_levels', [])
        performance_history = getattr(player, 'performance_history', [])
        
        stats = {
            'levels_completed': len(completed_levels),
            'perfect_scores': 0,
            'learning_streak': getattr(player, 'learning_streak', 0),
            'total_time_hours': getattr(player, 'total_time_spent', 0) / 3600,  # Convert seconds to hours
            'fast_completion': 0,
            'challenge_levels_completed': 0,
            'night_completions': 0,
            'early_completions': 0
        }
        
        # Analyze performance history
        for record in performance_history:
            # Perfect scores
            if record.get('score_percentage', 0) == 100:
                stats['perfect_scores'] += 1
            
            # Fast completions (under 2 minutes = 120 seconds)
            if record.get('completion_time', float('inf')) < 120:
                stats['fast_completion'] += 1
            
            # Challenge levels
            if record.get('level_type') == 'challenge':
                stats['challenge_levels_completed'] += 1
            
            # Time-based achievements
            completion_time = record.get('timestamp')
            if completion_time:
                try:
                    dt = datetime.fromisoformat(completion_time.replace('Z', '+00:00'))
                    hour = dt.hour
                    if hour >= 22 or hour < 6:  # 10 PM to 6 AM
                        stats['night_completions'] += 1
                    elif hour < 7:  # Before 7 AM
                        stats['early_completions'] += 1
                except:
                    pass  # Skip if timestamp parsing fails
        
        return stats
    
    def _check_achievement_condition(self, achievement: Dict[str, Any], stats: Dict[str, Any]) -> bool:
        """Check if achievement condition is met."""
        condition = achievement['condition']
        
        try:
            # Replace condition variables with actual values
            for key, value in stats.items():
                condition = condition.replace(key, str(value))
            
            # Evaluate the condition safely
            return eval(condition, {"__builtins__": {}})
        except:
            return False
    
    def _create_earned_achievement(self, achievement: Dict[str, Any]) -> Dict[str, Any]:
        """Create an earned achievement record."""
        return {
            'id': achievement['id'],
            'name': achievement['name'],
            'description': achievement['description'],
            'tier': achievement['tier'],
            'icon': achievement['icon'],
            'earned_at': datetime.now().isoformat(),
            'rewards': self.reward_calculations.get(achievement['tier'], self.reward_calculations['bronze'])
        }
    
    def get_achievement_progress(self, player) -> List[Dict[str, Any]]:
        """Get progress towards all achievements."""
        current_achievements = self.get_player_achievements(player)
        current_ids = [ach.get('id') if isinstance(ach, dict) else ach for ach in current_achievements]
        
        stats = self._calculate_player_stats(player)
        progress_list = []
        
        for achievement in self.achievement_definitions:
            if not achievement.get('hidden', False) or achievement['id'] in current_ids:
                progress = {
                    'id': achievement['id'],
                    'name': achievement['name'],
                    'description': achievement['description'],
                    'tier': achievement['tier'],
                    'icon': achievement['icon'],
                    'earned': achievement['id'] in current_ids,
                    'progress_percentage': self._calculate_progress_percentage(achievement, stats)
                }
                
                if progress['earned']:
                    earned_achievement = next(
                        (ach for ach in current_achievements if 
                         (ach.get('id') if isinstance(ach, dict) else ach) == achievement['id']), 
                        None
                    )
                    if isinstance(earned_achievement, dict):
                        progress['earned_at'] = earned_achievement.get('earned_at')
                
                progress_list.append(progress)
        
        return progress_list
    
    def _calculate_progress_percentage(self, achievement: Dict[str, Any], stats: Dict[str, Any]) -> float:
        """Calculate progress percentage towards an achievement."""
        condition = achievement['condition']
        
        try:
            # Extract the target value from the condition
            if '>=' in condition:
                parts = condition.split('>=')
                stat_name = parts[0].strip()
                target_value = float(parts[1].strip())
                current_value = stats.get(stat_name, 0)
                
                return min(100.0, (current_value / target_value) * 100)
            
            return 0.0
        except:
            return 0.0
    
    def get_available_rewards(self, player) -> List[Dict[str, Any]]:
        """Get rewards available for purchase."""
        player_coins = getattr(player, 'total_coins', 0)
        
        return [
            {
                'id': 'hint_pack',
                'name': 'Hint Pack',
                'description': 'Get 5 hints for difficult questions',
                'cost': 100,
                'type': 'consumable',
                'available': player_coins >= 100,
                'icon': '💡'
            },
            {
                'id': 'time_bonus',
                'name': 'Time Bonus',
                'description': 'Get extra time for tests',
                'cost': 150,
                'type': 'consumable',
                'available': player_coins >= 150,
                'icon': '⏰'
            },
            {
                'id': 'skip_level',
                'name': 'Skip Level',
                'description': 'Skip one difficult level',
                'cost': 300,
                'type': 'consumable',
                'available': player_coins >= 300,
                'icon': '⏭️'
            },
            {
                'id': 'double_points',
                'name': 'Double Points',
                'description': 'Double points for next level',
                'cost': 200,
                'type': 'buff',
                'available': player_coins >= 200,
                'icon': '⭐'
            },
            {
                'id': 'theme_dark',
                'name': 'Dark Theme',
                'description': 'Unlock dark theme for the interface',
                'cost': 250,
                'type': 'cosmetic',
                'available': player_coins >= 250,
                'icon': '🌙'
            }
        ]
    
    def purchase_reward(self, player, reward_id: str) -> Dict[str, Any]:
        """Process reward purchase."""
        available_rewards = self.get_available_rewards(player)
        reward = next((r for r in available_rewards if r['id'] == reward_id), None)
        
        if not reward:
            return {"success": False, "message": "Reward not found"}
        
        if not reward['available']:
            return {"success": False, "message": "Insufficient coins"}
        
        player_coins = getattr(player, 'total_coins', 0)
        if player_coins < reward['cost']:
            return {"success": False, "message": "Insufficient coins"}
        
        # Deduct coins
        player.total_coins = player_coins - reward['cost']
        
        # Add reward to player's inventory
        if not hasattr(player, 'purchased_rewards'):
            player.purchased_rewards = []
        
        player.purchased_rewards.append({
            'id': reward_id,
            'name': reward['name'],
            'type': reward['type'],
            'purchased_at': datetime.now().isoformat()
        })
        
        return {
            "success": True,
            "message": f"Successfully purchased {reward['name']}!",
            "remaining_coins": player.total_coins,
            "reward": reward
        }
    
    def get_leaderboard_data(self, player) -> Dict[str, Any]:
        """Get data for leaderboard display."""
        achievements = self.get_player_achievements(player)
        achievement_points = sum(
            self.reward_calculations.get(ach.get('tier', 'bronze'), {'xp': 0})['xp']
            for ach in achievements if isinstance(ach, dict)
        )
        
        return {
            'total_achievements': len(achievements),
            'achievement_points': achievement_points,
            'levels_completed': len(getattr(player, 'completed_levels', [])),
            'total_xp': getattr(player, 'total_xp', 0),
            'learning_streak': getattr(player, 'learning_streak', 0)
        }
