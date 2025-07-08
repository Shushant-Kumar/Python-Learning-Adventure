"""
Player class to manage user progress, achievements, and rewards
"""

from datetime import datetime
from typing import Dict, List, Any

class Player:
    """Represents a player in the Python learning game."""
    
    def __init__(self, name: str):
        self.name = name
        self.level = 1
        self.experience = 0
        self.coins = 0
        self.streak = 0
        self.last_play_date = None
        self.completed_lessons = []
        self.achievements = []
        self.test_scores = {}
        self.unlocked_rewards = []
        self.total_playtime = 0
        self.created_date = datetime.now().isoformat()
        
    def add_experience(self, points: int):
        """Add experience points and handle level up."""
        self.experience += points
        self.coins += points // 10  # 1 coin per 10 XP
        
        # Level up logic
        required_xp = self.level * 100
        if self.experience >= required_xp:
            self.level += 1
            self.coins += 50  # Level up bonus
            return True  # Level up occurred
        return False
    
    def complete_lesson(self, lesson_id: str):
        """Mark a lesson as completed."""
        if lesson_id not in self.completed_lessons:
            self.completed_lessons.append(lesson_id)
            self.add_experience(25)
            self.update_streak()
            return True
        return False
    
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
    
    def add_achievement(self, achievement_name: str):
        """Add an achievement to the player."""
        if achievement_name not in self.achievements:
            self.achievements.append(achievement_name)
            self.coins += 25  # Achievement bonus
            return True
        return False
    
    def record_test_score(self, test_name: str, score: int, max_score: int):
        """Record a test score."""
        percentage = (score / max_score) * 100
        self.test_scores[test_name] = {
            'score': score,
            'max_score': max_score,
            'percentage': percentage,
            'date': datetime.now().isoformat()
        }
        
        # Award XP based on performance
        if percentage >= 90:
            self.add_experience(50)
        elif percentage >= 75:
            self.add_experience(35)
        elif percentage >= 60:
            self.add_experience(20)
        else:
            self.add_experience(10)
    
    def can_unlock_reward(self, reward_cost: int) -> bool:
        """Check if player can afford a reward."""
        return self.coins >= reward_cost
    
    def unlock_reward(self, reward_name: str, cost: int):
        """Unlock a reward if player can afford it."""
        if self.can_unlock_reward(cost):
            self.coins -= cost
            self.unlocked_rewards.append(reward_name)
            return True
        return False
    
    def get_progress_summary(self) -> Dict[str, Any]:
        """Get a summary of player progress."""
        return {
            'name': self.name,
            'level': self.level,
            'experience': self.experience,
            'coins': self.coins,
            'streak': self.streak,
            'lessons_completed': len(self.completed_lessons),
            'achievements_count': len(self.achievements),
            'tests_taken': len(self.test_scores),
            'average_test_score': self._calculate_average_test_score(),
            'rewards_unlocked': len(self.unlocked_rewards)
        }
    
    def _calculate_average_test_score(self) -> float:
        """Calculate average test score percentage."""
        if not self.test_scores:
            return 0.0
        
        total = sum(test['percentage'] for test in self.test_scores.values())
        return round(total / len(self.test_scores), 2)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert player to dictionary for saving."""
        return {
            'name': self.name,
            'level': self.level,
            'experience': self.experience,
            'coins': self.coins,
            'streak': self.streak,
            'last_play_date': self.last_play_date,
            'completed_lessons': self.completed_lessons,
            'achievements': self.achievements,
            'test_scores': self.test_scores,
            'unlocked_rewards': self.unlocked_rewards,
            'total_playtime': self.total_playtime,
            'created_date': self.created_date
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Player':
        """Create player from dictionary."""
        player = cls(data['name'])
        player.level = data.get('level', 1)
        player.experience = data.get('experience', 0)
        player.coins = data.get('coins', 0)
        player.streak = data.get('streak', 0)
        player.last_play_date = data.get('last_play_date')
        player.completed_lessons = data.get('completed_lessons', [])
        player.achievements = data.get('achievements', [])
        player.test_scores = data.get('test_scores', {})
        player.unlocked_rewards = data.get('unlocked_rewards', [])
        player.total_playtime = data.get('total_playtime', 0)
        player.created_date = data.get('created_date', datetime.now().isoformat())
        return player
