"""
Game Animations Module
Controls all game animations and ensures smooth rendering transitions
"""

import time
import threading
import sys
import random
from typing import Dict, Any, Optional, Callable
from concurrent.futures import ThreadPoolExecutor


class AnimationManager:
    """Manages all game animations with performance optimization."""
    
    def __init__(self):
        self.animation_speed = 0.01  # Optimized for speed
        self.fast_mode = False
        self.animation_queue = []
        self.is_playing = False
        self.colors = self._init_colors()
        self.width = 80
        self.height = 20
        self._validate_terminal()
        
    def _init_colors(self) -> Dict[str, str]:
        """Initialize color codes with fallback for unsupported terminals."""
        try:
            if hasattr(sys.stdout, 'isatty') and sys.stdout.isatty():
                return {
                    'reset': '\033[0m',
                    'bold': '\033[1m',
                    'green': '\033[92m',
                    'blue': '\033[94m',
                    'cyan': '\033[96m',
                    'yellow': '\033[93m',
                    'magenta': '\033[95m',
                    'red': '\033[91m',
                    'white': '\033[97m'
                }
            else:
                return {key: '' for key in ['reset', 'bold', 'green', 'blue', 'cyan', 'yellow', 'magenta', 'red', 'white']}
        except Exception:
            return {key: '' for key in ['reset', 'bold', 'green', 'blue', 'cyan', 'yellow', 'magenta', 'red', 'white']}
    
    def _validate_terminal(self):
        """Validate terminal capabilities and adjust settings."""
        try:
            import os
            size = os.get_terminal_size()
            self.width = min(max(size.columns, 40), 120)
            self.height = min(max(size.lines, 10), 50)
        except Exception:
            self.width = 80
            self.height = 20
    
    def set_fast_mode(self, enabled: bool = True):
        """Enable or disable fast animation mode."""
        self.fast_mode = enabled
        self.animation_speed = 0.005 if enabled else 0.01
    
    def safe_sleep(self, duration: float):
        """Safe sleep with interruption handling."""
        try:
            time.sleep(max(0, duration))
        except KeyboardInterrupt:
            return
        except Exception:
            pass
    
    def clear_screen(self):
        """Clear console screen efficiently."""
        try:
            import os
            if os.name == 'nt':  # Windows
                os.system('cls')
            else:  # Unix/Linux/MacOS
                print('\033[2J\033[H', end='', flush=True)
        except Exception:
            print('\n' * 20)  # Fallback
    
    def play_level_completion(self, level_data: Dict[str, Any], player_stats: Dict[str, Any]):
        """Play level completion animation with optimized performance."""
        try:
            if self.fast_mode:
                self._play_completion_fast(level_data, player_stats)
            else:
                self._play_completion_normal(level_data, player_stats)
        except Exception as e:
            print(f"{self.colors['green']}Level {level_data.get('id', '?')} completed!{self.colors['reset']}")
    
    def _play_completion_fast(self, level_data: Dict[str, Any], player_stats: Dict[str, Any]):
        """Ultra-fast completion animation."""
        print(f"{self.colors['cyan']}{self.colors['bold']}🐍 PYTHON INTERPRETER{self.colors['reset']}")
        print("=" * 40)
        print(f"{self.colors['green']}✓ Level {level_data.get('id', 1)} completed!{self.colors['reset']}")
        print(f"{self.colors['blue']}Score: {player_stats.get('score', 0)} | XP: {player_stats.get('xp_earned', 0)}{self.colors['reset']}")
        print(f"{self.colors['yellow']}🔓 Next level unlocked!{self.colors['reset']}")
        self.safe_sleep(0.5)
    
    def _play_completion_normal(self, level_data: Dict[str, Any], player_stats: Dict[str, Any]):
        """Normal speed completion animation."""
        print(f"{self.colors['cyan']}{self.colors['bold']}🐍 PYTHON INTERPRETER{self.colors['reset']}")
        print("=" * self.width)
        
        # Quick code compilation effect
        code_lines = [
            "import success",
            f"from level_{level_data.get('id', 1)} import mastery",
            f"result = solve_{level_data.get('topic', 'python').lower().replace(' ', '_')}()",
            f"{self.colors['green']}✓ All tests passed!{self.colors['reset']}",
            f"{self.colors['green']}✓ Level {level_data.get('id', 1)} completed!{self.colors['reset']}"
        ]
        
        for line in code_lines:
            print(line)
            self.safe_sleep(0.02 if self.fast_mode else 0.05)
        
        # Quick stats display
        print(f"\n{self.colors['cyan']}📊 PERFORMANCE SUMMARY{self.colors['reset']}")
        print("-" * 30)
        stats = [
            (f"Score: {self.colors['green']}{player_stats.get('score', 0)}{self.colors['reset']}"),
            (f"XP: {self.colors['blue']}{player_stats.get('xp_earned', 0)}{self.colors['reset']}"),
            (f"Coins: {self.colors['yellow']}{player_stats.get('coins_earned', 0)}{self.colors['reset']}")
        ]
        
        for stat in stats:
            print(stat)
            self.safe_sleep(0.1)
        
        print(f"{self.colors['yellow']}🔓 Next level unlocked!{self.colors['reset']}")
        self.safe_sleep(0.2)
    
    def play_level_transition(self, from_level: int, to_level: int, topic: str):
        """Play level transition animation."""
        try:
            if self.fast_mode:
                self._play_transition_fast(from_level, to_level, topic)
            else:
                self._play_transition_normal(from_level, to_level, topic)
        except Exception:
            print(f"Transitioning from Level {from_level} to Level {to_level}")
    
    def _play_transition_fast(self, from_level: int, to_level: int, topic: str):
        """Fast transition animation."""
        print(f"{self.colors['cyan']}📚 Loading Level {to_level}: {topic}{self.colors['reset']}")
        self.safe_sleep(0.3)
    
    def _play_transition_normal(self, from_level: int, to_level: int, topic: str):
        """Normal transition animation."""
        self.clear_screen()
        print(f"{self.colors['cyan']}{self.colors['bold']}")
        print("🚀 LEVEL TRANSITION")
        print("=" * 50)
        print(f"{self.colors['reset']}")
        
        print(f"From: Level {from_level}")
        print(f"To:   Level {to_level} - {topic}")
        
        # Simple loading bar
        print("\nLoading...")
        for i in range(21):
            percentage = (i / 20) * 100
            filled = "█" * i
            empty = "░" * (20 - i)
            print(f"\r[{filled}{empty}] {percentage:.0f}%", end="", flush=True)
            self.safe_sleep(0.02)
        
        print(f"\n{self.colors['green']}Ready to start Level {to_level}!{self.colors['reset']}")
        self.safe_sleep(0.5)
    
    def play_achievement_unlock(self, achievement: Dict[str, Any]):
        """Play achievement unlock animation."""
        try:
            if self.fast_mode:
                self._play_achievement_fast(achievement)
            else:
                self._play_achievement_normal(achievement)
        except Exception:
            print(f"🏆 Achievement Unlocked: {achievement.get('name', 'Unknown')}")
    
    def _play_achievement_fast(self, achievement: Dict[str, Any]):
        """Fast achievement animation."""
        icon = achievement.get('icon', '🏆')
        name = achievement.get('name', 'Achievement')
        print(f"{self.colors['yellow']}{icon} Achievement Unlocked: {name}!{self.colors['reset']}")
        self.safe_sleep(0.5)
    
    def _play_achievement_normal(self, achievement: Dict[str, Any]):
        """Normal achievement animation."""
        self.clear_screen()
        
        icon = achievement.get('icon', '🏆')
        name = achievement.get('name', 'Achievement')
        description = achievement.get('description', 'Great job!')
        
        # Achievement banner
        banner = f"""
{self.colors['yellow']}{self.colors['bold']}
    ╔══════════════════════════════════════╗
    ║            🎉 ACHIEVEMENT 🎉          ║
    ║              UNLOCKED!               ║
    ╚══════════════════════════════════════╝
{self.colors['reset']}

    {icon} {self.colors['bold']}{name}{self.colors['reset']}
    
    {description}
    
    {self.colors['green']}Congratulations!{self.colors['reset']}
        """
        
        print(banner)
        self.safe_sleep(1.0 if not self.fast_mode else 0.5)
    
    def play_challenge_start(self, challenge_data: Dict[str, Any]):
        """Play challenge level start animation."""
        try:
            if self.fast_mode:
                print(f"{self.colors['red']}⚡ Challenge Level: {challenge_data.get('title', 'Unknown')}{self.colors['reset']}")
                self.safe_sleep(0.3)
            else:
                self._play_challenge_normal(challenge_data)
        except Exception:
            print(f"Challenge: {challenge_data.get('title', 'Unknown')}")
    
    def _play_challenge_normal(self, challenge_data: Dict[str, Any]):
        """Normal challenge start animation."""
        self.clear_screen()
        
        title = challenge_data.get('title', 'Challenge Level')
        description = challenge_data.get('description', 'A difficult challenge awaits!')
        
        challenge_banner = f"""
{self.colors['red']}{self.colors['bold']}
    ⚡⚡⚡ CHALLENGE LEVEL ⚡⚡⚡
    
    {title}
    
    {self.colors['reset']}{description}
    
    {self.colors['yellow']}Are you ready for the challenge?{self.colors['reset']}
        """
        
        print(challenge_banner)
        self.safe_sleep(1.5)
    
    def play_lesson_loading(self, lesson_data: Dict[str, Any]):
        """Play lesson loading animation."""
        try:
            topic = lesson_data.get('topic', 'Python Concepts')
            if self.fast_mode:
                print(f"{self.colors['blue']}📚 Loading: {topic}{self.colors['reset']}")
                self.safe_sleep(0.2)
            else:
                self._play_lesson_loading_normal(lesson_data)
        except Exception:
            print(f"Loading lesson: {lesson_data.get('topic', 'Unknown')}")
    
    def _play_lesson_loading_normal(self, lesson_data: Dict[str, Any]):
        """Normal lesson loading animation."""
        topic = lesson_data.get('topic', 'Python Concepts')
        estimated_time = lesson_data.get('estimated_time', 15)
        
        print(f"{self.colors['blue']}{self.colors['bold']}")
        print("📚 LESSON LOADING")
        print("=" * 40)
        print(f"{self.colors['reset']}")
        
        print(f"Topic: {topic}")
        print(f"Estimated Time: {estimated_time} minutes")
        print("\nPreparing lesson content...")
        
        # Simple dots animation
        for i in range(3):
            print(".", end="", flush=True)
            self.safe_sleep(0.3)
        
        print(f"\n{self.colors['green']}Lesson ready!{self.colors['reset']}")
        self.safe_sleep(0.5)
    
    def play_error_animation(self, error_message: str):
        """Play error animation."""
        try:
            print(f"{self.colors['red']}❌ Error: {error_message}{self.colors['reset']}")
            if not self.fast_mode:
                self.safe_sleep(0.5)
        except Exception:
            print(f"Error: {error_message}")
    
    def play_success_animation(self, message: str):
        """Play success animation."""
        try:
            print(f"{self.colors['green']}✅ {message}{self.colors['reset']}")
            if not self.fast_mode:
                self.safe_sleep(0.3)
        except Exception:
            print(f"Success: {message}")
    
    def play_loading_animation(self, message: str, duration: float = 1.0):
        """Play a generic loading animation."""
        try:
            print(f"{message}...", end="", flush=True)
            
            if self.fast_mode:
                duration = min(duration, 0.5)
            
            steps = max(1, int(duration / 0.1))
            for i in range(steps):
                print(".", end="", flush=True)
                self.safe_sleep(0.1)
            
            print(" Done!")
        except Exception:
            print(f"{message}... Done!")
    
    def queue_animation(self, animation_func: Callable, *args, **kwargs):
        """Queue an animation to be played."""
        self.animation_queue.append((animation_func, args, kwargs))
    
    def play_queued_animations(self):
        """Play all queued animations."""
        while self.animation_queue:
            animation_func, args, kwargs = self.animation_queue.pop(0)
            try:
                animation_func(*args, **kwargs)
            except Exception as e:
                print(f"Animation error: {e}")
    
    def play_concurrent_animations(self, animations: list):
        """Play multiple animations concurrently."""
        try:
            with ThreadPoolExecutor(max_workers=3) as executor:
                futures = []
                for animation_func, args, kwargs in animations:
                    future = executor.submit(animation_func, *args, **kwargs)
                    futures.append(future)
                
                # Wait for all animations to complete
                for future in futures:
                    future.result()
        except Exception as e:
            print(f"Concurrent animation error: {e}")
    
    def stop_all_animations(self):
        """Stop all running animations."""
        self.is_playing = False
        self.animation_queue.clear()
    
    def get_animation_performance_stats(self) -> Dict[str, Any]:
        """Get animation performance statistics."""
        return {
            'fast_mode': self.fast_mode,
            'animation_speed': self.animation_speed,
            'queue_length': len(self.animation_queue),
            'terminal_size': f"{self.width}x{self.height}",
            'colors_supported': bool(self.colors.get('reset'))
        }


class AnimationController:
    """High-level animation controller that manages the AnimationManager."""
    
    def __init__(self):
        self.manager = AnimationManager()
        self.animation_history = []
    
    def play_level_completion(self, level_data: Dict[str, Any], player_stats: Dict[str, Any]):
        """Play level completion animation."""
        self._log_animation('level_completion', level_data.get('id'))
        self.manager.play_level_completion(level_data, player_stats)
    
    def play_level_transition(self, from_level: int, to_level: int, topic: str):
        """Play level transition animation."""
        self._log_animation('level_transition', f"{from_level} -> {to_level}")
        self.manager.play_level_transition(from_level, to_level, topic)
    
    def play_achievement_unlock(self, achievement: Dict[str, Any]):
        """Play achievement unlock animation."""
        self._log_animation('achievement_unlock', achievement.get('id'))
        self.manager.play_achievement_unlock(achievement)
    
    def play_challenge_start(self, challenge_data: Dict[str, Any]):
        """Play challenge start animation."""
        self._log_animation('challenge_start', challenge_data.get('id'))
        self.manager.play_challenge_start(challenge_data)
    
    def play_lesson_loading(self, lesson_data: Dict[str, Any]):
        """Play lesson loading animation."""
        self._log_animation('lesson_loading', lesson_data.get('id'))
        self.manager.play_lesson_loading(lesson_data)
    
    def set_fast_mode(self, enabled: bool):
        """Enable or disable fast animation mode."""
        self.manager.set_fast_mode(enabled)
    
    def wait_for_animation(self):
        """Wait for current animation to complete."""
        # This is a placeholder - in a real implementation, 
        # you might track active animations
        time.sleep(0.1)
    
    def _log_animation(self, animation_type: str, context: Any):
        """Log animation for debugging and performance tracking."""
        self.animation_history.append({
            'type': animation_type,
            'context': context,
            'timestamp': time.time()
        })
        
        # Keep only recent history
        if len(self.animation_history) > 100:
            self.animation_history = self.animation_history[-50:]
    
    def get_animation_stats(self) -> Dict[str, Any]:
        """Get animation statistics."""
        return {
            'total_animations': len(self.animation_history),
            'recent_animations': self.animation_history[-10:],
            'performance_stats': self.manager.get_animation_performance_stats()
        }
