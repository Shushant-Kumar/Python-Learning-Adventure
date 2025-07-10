"""
Main Game Logic Coordinator
Coordinates all game logic modules and provides a unified interface
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import time

from .achievements import AchievementManager
from .level_loader import LevelLoader  
from .animations import AnimationController
from .player_state import PlayerStateManager, PlayerState
from .event_dispatcher import GameEventManager, EventType


class GameLogicCoordinator:
    """Main coordinator that manages all game logic modules."""
    
    def __init__(self, data_directory: str = "player_data"):
        # Initialize all subsystems
        self.achievement_manager = AchievementManager()
        self.level_loader = LevelLoader()
        self.animation_controller = AnimationController()
        self.player_manager = PlayerStateManager(data_directory)
        self.event_manager = GameEventManager()
        
        # Setup event handlers
        self._setup_event_handlers()
        
        # Performance tracking
        self.performance_metrics = {
            'level_completions': 0,
            'achievements_awarded': 0,
            'animations_played': 0,
            'total_session_time': 0
        }
        self.session_start_time = time.time()
    
    def _setup_event_handlers(self):
        """Setup event handlers between modules."""
        # Achievement events trigger animations
        self.event_manager.subscribe_to_event(
            EventType.ACHIEVEMENT_UNLOCKED,
            self._handle_achievement_animation
        )
        
        # Level completion events trigger multiple actions
        self.event_manager.subscribe_to_event(
            EventType.LEVEL_COMPLETED,
            self._handle_level_completion_effects
        )
        
        # Player stats updates trigger achievement checks
        self.event_manager.subscribe_to_event(
            EventType.PLAYER_STATS_UPDATED,
            self._handle_stats_achievement_check
        )
    
    def _handle_achievement_animation(self, event):
        """Handle achievement unlock animation."""
        achievement_data = event.data.get('achievement_data', {})
        self.animation_controller.play_achievement_unlock(achievement_data)
        self.performance_metrics['animations_played'] += 1
    
    def _handle_level_completion_effects(self, event):
        """Handle all effects of level completion."""
        level_id = event.data.get('level_id')
        player_id = event.data.get('player_id')
        passed = event.data.get('passed', False)
        
        if passed and level_id:
            # Check for newly unlocked levels
            next_level = level_id + 1
            level_data = self.level_loader.get_level_data(next_level)
            if level_data:
                self.event_manager.level_unlocked(next_level, player_id, level_id)
        
        self.performance_metrics['level_completions'] += 1
    
    def _handle_stats_achievement_check(self, event):
        """Check for new achievements when stats are updated."""
        player_id = event.data.get('player_id')
        if player_id:
            player = self.player_manager.load_player(player_id)
            if player:
                new_achievements = self.achievement_manager.check_new_achievements(player)
                if new_achievements:
                    self.achievement_manager.award_achievements(player, new_achievements)
                    for achievement in new_achievements:
                        self.event_manager.achievement_unlocked(
                            achievement['id'], player_id, achievement
                        )
                    self.performance_metrics['achievements_awarded'] += len(new_achievements)
    
    # Player Management
    def create_player(self, username: str) -> PlayerState:
        """Create a new player."""
        player = self.player_manager.create_new_player(username)
        self.event_manager.player_registered(player.id, username)
        return player
    
    def load_player(self, player_id: str) -> Optional[PlayerState]:
        """Load an existing player."""
        player = self.player_manager.load_player(player_id)
        if player:
            self.event_manager.player_login(player.id, player.username)
        return player
    
    def save_player(self, player: PlayerState):
        """Save player data."""
        self.player_manager.save_player(player)
    
    # Level Management
    def get_level_data(self, level_id: int, player: PlayerState) -> Optional[Dict[str, Any]]:
        """Get level data with player-specific customizations."""
        level_data = self.level_loader.get_level_data(level_id, player)
        if level_data and self.level_loader.is_level_available(level_id, player):
            # Log level access
            self.event_manager.level_started(level_id, player.id, level_data.get('topic', ''))
            
            # Play loading animation
            self.animation_controller.play_lesson_loading(level_data)
            
            return level_data
        return None
    
    def get_level_map(self, player: PlayerState) -> List[Dict[str, Any]]:
        """Get all levels with unlock status."""
        return self.level_loader.get_level_map(player)
    
    def get_next_available_level(self, player: PlayerState) -> Optional[Dict[str, Any]]:
        """Get the next available level for the player."""
        return self.level_loader.get_next_available_level(player)
    
    def get_recommended_levels(self, player: PlayerState, count: int = 3) -> List[Dict[str, Any]]:
        """Get recommended levels for the player."""
        return self.level_loader.get_recommended_levels(player, count)
    
    # Level Completion
    def complete_level(self, player: PlayerState, level_id: int, 
                      quiz_answers: List[Any]) -> Dict[str, Any]:
        """Process level completion with full integration."""
        start_time = time.time()
        
        # Get level data and validate
        level_data = self.level_loader.get_level_data(level_id, player)
        if not level_data:
            return {"success": False, "message": "Level not found"}
        
        # Validate quiz answers
        quiz_questions = level_data.get('quiz_questions', level_data.get('quiz', []))
        if not quiz_questions:
            return {"success": False, "message": "No quiz questions found"}
        
        if not quiz_answers or len(quiz_answers) != len(quiz_questions):
            return {"success": False, "message": "Invalid quiz answers"}
        
        # Calculate score
        correct_answers = 0
        for i, answer in enumerate(quiz_answers):
            if quiz_questions[i].get('correct') == answer:
                correct_answers += 1
        
        score_percentage = (correct_answers / len(quiz_questions)) * 100
        time_taken = int(time.time() - start_time)
        passed = score_percentage >= 70  # 70% passing threshold
        
        # Update player progress
        progress_update = self.player_manager.update_player_progress(
            player, level_id, score_percentage, time_taken, passed
        )
        
        # Calculate rewards
        rewards = level_data.get('rewards', {})
        coins_earned = rewards.get('coins', 0) if passed else 0
        xp_earned = rewards.get('xp', 0) if passed else 0
        
        if passed:
            player.add_coins(coins_earned)
            player.add_xp(xp_earned)
        
        # Dispatch completion event
        self.event_manager.level_completed(
            level_id, player.id, score_percentage, passed, time_taken
        )
        
        # Play completion animation
        player_stats = {
            'score': score_percentage,
            'xp_earned': xp_earned,
            'coins_earned': coins_earned,
            'time_taken': time_taken,
            'accuracy': score_percentage
        }
        
        self.animation_controller.play_level_completion(level_data, player_stats)
        
        # Check for achievements
        new_achievements = self.achievement_manager.check_new_achievements(player)
        if new_achievements:
            achievement_rewards = self.achievement_manager.award_achievements(player, new_achievements)
            for achievement in new_achievements:
                self.event_manager.achievement_unlocked(achievement['id'], player.id, achievement)
        
        # Save player state
        self.player_manager.save_player(player)
        
        # Update stats event
        stats = self.player_manager.get_player_stats(player)
        self.event_manager.player_stats_updated(player.id, stats.__dict__)
        
        return {
            "success": True,
            "passed": passed,
            "score": score_percentage,
            "correct_answers": correct_answers,
            "total_questions": len(quiz_questions),
            "coins_earned": coins_earned,
            "xp_earned": xp_earned,
            "new_achievements": new_achievements,
            "time_taken": time_taken,
            "message": f"Level {'completed' if passed else 'failed'}! Score: {score_percentage:.1f}%"
        }
    
    # Answer Submission
    def submit_level_answers(self, player_id: str, level_id: int, answers: list) -> Dict[str, Any]:
        """
        Submit answers for a level and get comprehensive feedback.
        
        Args:
            player_id: Player's unique identifier
            level_id: Level being attempted  
            answers: List of submitted answers
            
        Returns:
            Comprehensive feedback and progression data
        """
        # Load player
        player = self.player_manager.load_player(player_id)
        if not player:
            return {
                "success": False,
                "error": "Player not found",
                "feedback": {
                    "type": "error",
                    "title": "Account Error",
                    "message": "Your account could not be found. Please try logging in again.",
                    "show_retry": False
                }
            }
        
        # Validate level availability
        if not self.level_loader.is_level_available(level_id, player):
            return {
                "success": False,
                "error": "Level not available",
                "feedback": {
                    "type": "error", 
                    "title": "Level Locked",
                    "message": "This level is not yet available. Complete previous levels first.",
                    "show_retry": False
                }
            }
        
        # Validate answers using level loader
        validation_result = self.level_loader.validate_answer_submission(level_id, player, answers)
        
        if not validation_result.get("success"):
            return validation_result
        
        # If level was passed, trigger related events and updates
        if validation_result.get("passed"):
            # Update player state
            player_update_result = self.player_manager.update_player_progress(
                player, level_id, validation_result['score_percentage'], 
                time_taken=0, passed=True  # time_taken could be tracked separately
            )
            
            # Trigger level completion event
            self.event_manager.level_completed(
                level_id, player.id, 
                score=validation_result['score_percentage'],
                passed=True,
                time_taken=0  # time_taken could be tracked separately
            )
            
            # Check for achievements
            new_achievements = self.achievement_manager.check_new_achievements(player)
            if new_achievements:
                self.achievement_manager.award_achievements(player, new_achievements)
                for achievement in new_achievements:
                    self.event_manager.achievement_unlocked(
                        achievement['id'], player.id, achievement
                    )
            
            # Update performance metrics
            self.performance_metrics['level_completions'] += 1
            if new_achievements:
                self.performance_metrics['achievements_awarded'] += len(new_achievements)
        
        # Add dashboard redirect data if level passed
        if validation_result.get("passed"):
            from .feedback_handler import DashboardRedirect
            redirect_data = DashboardRedirect.generate_redirect_data(player, level_id)
            validation_result['redirect_data'] = redirect_data
            
            # Add unlock notification if next level is unlocked
            progression = validation_result.get('progression', {})
            if progression.get('next_level_unlocked'):
                unlock_notification = DashboardRedirect.generate_level_unlock_notification(
                    progression.get('next_level_id')
                )
                validation_result['unlock_notification'] = unlock_notification
        
        return validation_result
    
    def get_level_feedback_data(self, player_id: str, level_id: int) -> Dict[str, Any]:
        """Get feedback and UI data for a level."""
        player = self.player_manager.load_player(player_id)
        if not player:
            return {"error": "Player not found"}
        
        level_data = self.level_loader.get_level_data(level_id, player)
        if not level_data:
            return {"error": "Level not found"}
        
        return {
            "level_data": level_data,
            "can_retry": self.level_loader._can_retry_level(player, level_id),
            "attempt_count": getattr(player, 'level_attempts', {}).get(str(level_id), 0),
            "max_attempts": self.level_loader.progression_rules['max_retries'],
            "is_available": self.level_loader.is_level_available(level_id, player)
        }

    # Achievement Management
    def get_player_achievements(self, player: PlayerState) -> List[Dict[str, Any]]:
        """Get player achievements."""
        return self.achievement_manager.get_player_achievements(player)
    
    def get_achievement_progress(self, player: PlayerState) -> List[Dict[str, Any]]:
        """Get achievement progress."""
        return self.achievement_manager.get_achievement_progress(player)
    
    def get_available_rewards(self, player: PlayerState) -> List[Dict[str, Any]]:
        """Get available rewards for purchase."""
        return self.achievement_manager.get_available_rewards(player)
    
    def purchase_reward(self, player: PlayerState, reward_id: str) -> Dict[str, Any]:
        """Purchase a reward."""
        result = self.achievement_manager.purchase_reward(player, reward_id)
        if result['success']:
            self.player_manager.save_player(player)
        return result
    
    # Statistics and Analytics
    def get_player_stats(self, player: PlayerState) -> Dict[str, Any]:
        """Get comprehensive player statistics."""
        stats = self.player_manager.get_player_stats(player)
        total_levels = len(self.level_loader.levels)
        return {
            'levels_completed': len(stats.levels_completed),
            'total_score': stats.total_score,
            'total_xp': stats.total_xp,
            'total_coins': stats.total_coins,
            'learning_streak': stats.learning_streak,
            'total_time_spent': stats.total_time_spent,
            'average_score': stats.average_score,
            'perfect_scores': stats.perfect_scores,
            'achievements_count': stats.achievements_count,
            'last_active': stats.last_active,
            'progress_percentage': (len(stats.levels_completed) / total_levels) * 100 if total_levels > 0 else 0
        }
    
    def get_leaderboard(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get leaderboard data."""
        return self.player_manager.get_leaderboard_data(limit)
    
    def get_system_performance(self) -> Dict[str, Any]:
        """Get system performance metrics."""
        current_time = time.time()
        session_time = current_time - self.session_start_time
        
        return {
            'session_time': session_time,
            'performance_metrics': self.performance_metrics,
            'event_stats': self.event_manager.get_system_stats(),
            'animation_stats': self.animation_controller.get_animation_stats(),
            'memory_usage': self._get_memory_usage()
        }
    
    def _get_memory_usage(self) -> Dict[str, Any]:
        """Get memory usage information."""
        try:
            import psutil
            process = psutil.Process()
            memory_info = process.memory_info()
            return {
                'rss': memory_info.rss / 1024 / 1024,  # MB
                'vms': memory_info.vms / 1024 / 1024,  # MB
                'percent': process.memory_percent()
            }
        except ImportError:
            return {'error': 'psutil not available'}
    
    # Animation Control
    def set_fast_animations(self, player: PlayerState, enabled: bool):
        """Enable or disable fast animations."""
        self.animation_controller.set_fast_mode(enabled)
        self.player_manager.update_player_preferences(player, {'fast_animations': enabled})
    
    def play_level_transition(self, from_level: int, to_level: int, topic: str):
        """Play level transition animation."""
        self.animation_controller.play_level_transition(from_level, to_level, topic)
    
    # Utility Methods
    def get_hint(self, player: PlayerState, level_id: int) -> str:
        """Get a hint for a specific level."""
        level_data = self.level_loader.get_level_data(level_id, player)
        if not level_data:
            return "Level not found. Try reviewing the basics!"
        
        topic = level_data.get('topic', '').lower()
        
        # Log hint request
        self.event_manager.hint_requested(level_id, player.id, 'general')
        
        # Topic-specific hints
        hints = {
            'variable': [
                "Remember: variable names should be descriptive and use snake_case",
                "Variables in Python don't need to be declared with a type",
                "Try using meaningful names like 'user_name' instead of 'x'"
            ],
            'string': [
                "String methods like .upper(), .lower(), and .strip() are very useful",
                "Use f-strings for formatting: f'Hello {name}!'",
                "Remember that strings are immutable in Python"
            ],
            'list': [
                "Lists use square brackets [] and can contain any type of data",
                "Use .append() to add items and [index] to access them",
                "Remember: list indices start at 0!"
            ]
        }
        
        import random
        for key in hints:
            if key in topic:
                return random.choice(hints[key])
        
        return "Take your time and read the instructions carefully. Don't be afraid to experiment!"
    
    def backup_player_data(self, player: PlayerState) -> str:
        """Create a backup of player data."""
        return self.player_manager.backup_player_data(player)
    
    def shutdown(self):
        """Shutdown the game logic system."""
        self.event_manager.shutdown()
        
        # Log final performance metrics
        print("\nGame Logic System Shutdown")
        print("=" * 40)
        performance = self.get_system_performance()
        print(f"Session time: {performance['session_time']:.1f} seconds")
        print(f"Level completions: {self.performance_metrics['level_completions']}")
        print(f"Achievements awarded: {self.performance_metrics['achievements_awarded']}")
        print(f"Animations played: {self.performance_metrics['animations_played']}")


# Convenience class for backward compatibility
class AdvancedGameLogic(GameLogicCoordinator):
    """Backward compatibility wrapper for the original AdvancedGameLogic class."""
    pass
