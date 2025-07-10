"""
Creative Python-themed Level Transition Animations
Provides engaging visual transitions between levels with Python code aesthetics
Optimized for smooth performance and error resilience
"""

import time
import random
import threading
import sys
import traceback
from typing import List, Dict, Any, Callable, Optional
from datetime import datetime

class PythonLevelAnimator:
    """Creates beautiful Python-themed animations for level transitions with error handling."""
    
    def __init__(self):
        self.animation_speed = 0.01  # seconds between frames (optimized for speed)
        self.width = 80  # console width
        self.height = 20  # console height
        self.fast_mode = False  # Enable for even faster animations
        self.colors = self._init_colors()
        self._validate_terminal()
        
    def _init_colors(self) -> Dict[str, str]:
        """Initialize color codes with fallback for unsupported terminals."""
        try:
            # Check if terminal supports colors
            if hasattr(sys.stdout, 'isatty') and sys.stdout.isatty():
                return {
                    'reset': '\033[0m',
                    'bold': '\033[1m',
                    'dim': '\033[2m',
                    'green': '\033[92m',
                    'blue': '\033[94m',
                    'cyan': '\033[96m',
                    'yellow': '\033[93m',
                    'magenta': '\033[95m',
                    'red': '\033[91m',
                    'white': '\033[97m',
                    'bg_black': '\033[40m',
                    'bg_blue': '\033[44m',
                    'bg_green': '\033[42m'
                }
            else:
                # Fallback for non-color terminals
                return {key: '' for key in [
                    'reset', 'bold', 'dim', 'green', 'blue', 'cyan', 
                    'yellow', 'magenta', 'red', 'white', 'bg_black', 
                    'bg_blue', 'bg_green'
                ]}
        except Exception:
            # Complete fallback
            return {key: '' for key in [
                'reset', 'bold', 'dim', 'green', 'blue', 'cyan', 
                'yellow', 'magenta', 'red', 'white', 'bg_black', 
                'bg_blue', 'bg_green'
            ]}
    
    def _validate_terminal(self):
        """Validate terminal capabilities and adjust settings."""
        try:
            import os
            size = os.get_terminal_size()
            self.width = min(max(size.columns, 40), 120)  # Reasonable bounds
            self.height = min(max(size.lines, 10), 50)
        except Exception:
            # Use safe defaults
            self.width = 80
            self.height = 20
    
    def clear_screen(self):
        """Clear the console screen efficiently with error handling."""
        try:
            import os
            if os.name == 'nt':  # Windows
                os.system('cls')
            else:  # Unix/Linux/MacOS
                print('\033[2J\033[H', end='', flush=True)
        except Exception:
            # Fallback: print newlines
            print('\n' * 50)
    
    def safe_sleep(self, duration: float):
        """Safe sleep with interruption handling."""
        try:
            time.sleep(max(0, duration))
        except KeyboardInterrupt:
            return  # Allow graceful interruption
        except Exception:
            pass  # Ignore other sleep errors
    
    def set_fast_mode(self, enabled: bool = True):
        """Enable or disable fast animation mode."""
        try:
            self.fast_mode = enabled
            if enabled:
                self.animation_speed = 0.005  # Ultra fast
            else:
                self.animation_speed = 0.02  # Normal fast
        except Exception:
            pass  # Maintain current settings on error
    
    def animate_level_completion(self, level_data: Dict[str, Any], player_stats: Dict[str, Any]):
        """Animate level completion with optimized performance and comprehensive error handling."""
        try:
            # Validate inputs
            if not isinstance(level_data, dict):
                level_data = {"id": 1, "topic": "Python Basics"}
            if not isinstance(player_stats, dict):
                player_stats = {"score": 0, "xp_earned": 0, "coins_earned": 0, "time_taken": 0, "accuracy": 0}
            
            # Use optimized single-phase animation for better performance
            if self.fast_mode:
                self._animate_completion_fast(level_data, player_stats)
            else:
                # Streamlined normal mode with reduced phases
                self._animate_code_compilation(level_data)
                self._animate_stats_display_fast(player_stats)
                self._animate_level_unlock_fast()
            
        except KeyboardInterrupt:
            print(f"\n{self.colors['yellow']}Animation interrupted by user{self.colors['reset']}")
        except Exception as e:
            print(f"\n{self.colors['red']}Animation error: {str(e)}{self.colors['reset']}")
            # Continue with simplified completion message
            print(f"{self.colors['green']}Level {level_data.get('id', '?')} completed!{self.colors['reset']}")
    
    def _animate_completion_fast(self, level_data: Dict[str, Any], player_stats: Dict[str, Any]):
        """Fast completion animation for quick mode."""
        print(f"{self.colors['green']}{self.colors['bold']}✅ Level {level_data.get('id', '?')} Complete!{self.colors['reset']}")
        print(f"{self.colors['cyan']}Score: {player_stats.get('score', 0)}% | XP: +{player_stats.get('xp_earned', 0)} | Coins: +{player_stats.get('coins_earned', 0)}{self.colors['reset']}")
        self.safe_sleep(1)

    def _animate_stats_display_fast(self, player_stats: Dict[str, Any]):
        """Fast stats display animation."""
        print(f"{self.colors['cyan']}{self.colors['bold']}📊 RESULTS{self.colors['reset']}")
        print(f"Score: {self.colors['green']}{player_stats.get('score', 0)}%{self.colors['reset']}")
        print(f"XP: {self.colors['blue']}+{player_stats.get('xp_earned', 0)}{self.colors['reset']}")
        print(f"Coins: {self.colors['yellow']}+{player_stats.get('coins_earned', 0)}{self.colors['reset']}")
        print(f"Time: {self.colors['cyan']}{player_stats.get('time_taken', 0)}s{self.colors['reset']}")
        self.safe_sleep(0.5)

    def _animate_level_unlock_fast(self):
        """Fast level unlock animation."""
        print(f"{self.colors['yellow']}🔓 Next level unlocked!{self.colors['reset']}")
        self.safe_sleep(0.3)
    
    def _animate_code_compilation(self, level_data: Dict[str, Any]):
        """Simulate Python code compilation with syntax highlighting."""
        print(f"{self.colors['cyan']}{self.colors['bold']}🐍 PYTHON INTERPRETER{self.colors['reset']}")
        print("=" * self.width)
        
        code_snippets = [
            "import success",
            f"from level_{level_data.get('id', 1)} import mastery",
            "class LearningProgress:",
            "    def __init__(self, knowledge):",
            "        self.understanding = knowledge",
            "        self.confidence += 1",
            "",
            "# Executing your solution...",
            f"result = solve_{level_data.get('topic', 'python').lower().replace(' ', '_')}()",
            "assert result == 'SUCCESS'",
            "",
            f"{self.colors['green']}✓ All tests passed!{self.colors['reset']}",
            f"{self.colors['green']}✓ Code compiled successfully!{self.colors['reset']}",
            f"{self.colors['green']}✓ Level {level_data.get('id', 1)} completed!{self.colors['reset']}"
        ]
        
        sleep_time = 0.02 if self.fast_mode else 0.05  # Much faster compilation display
        
        for line in code_snippets:
            if line.startswith("import") or line.startswith("from"):
                print(f"{self.colors['blue']}{line}{self.colors['reset']}")
            elif line.startswith("class") or line.startswith("def"):
                print(f"{self.colors['yellow']}{line}{self.colors['reset']}")
            elif line.startswith("#"):
                print(f"{self.colors['dim']}{line}{self.colors['reset']}")
            elif "assert" in line:
                print(f"{self.colors['magenta']}{line}{self.colors['reset']}")
            else:
                print(line)
            
            self.safe_sleep(sleep_time)
        
        self.safe_sleep(0.2 if self.fast_mode else 0.3)
    
    def _animate_success_celebration(self, player_stats: Dict[str, Any]):
        """Create a celebratory animation with Python symbols."""
        self.clear_screen()
        
        # Python logo ASCII art animation
        python_frames = [
            """
    🐍      ╔═══════════════════════╗
  ╔═══╗    ║     LEVEL COMPLETE!   ║
 ╔╝ ● ╚╗   ║                       ║
 ╚╗   ╔╝   ║    Great job, coder!  ║
  ╚═══╝    ╚═══════════════════════╝
            """,
            """
      🐍    ╔═══════════════════════╗
    ╔═══╗  ║     LEVEL COMPLETE!   ║
   ╔╝ ● ╚╗ ║                       ║
   ╚╗   ╔╝ ║    Great job, coder!  ║
    ╚═══╝  ╚═══════════════════════╝
            """,
            """
        🐍  ╔═══════════════════════╗
      ╔═══╗║     LEVEL COMPLETE!   ║
     ╔╝ ● ╚║                       ║
     ╚╗   ╔║    Great job, coder!  ║
      ╚═══╝╚═══════════════════════╝
            """
        ]
        
        # Optimized animated celebration
        iterations = 2 if self.fast_mode else 3
        frame_delay = 0.2 if self.fast_mode else 0.3
        
        for frame in python_frames * iterations:
            self.clear_screen()
            print(f"{self.colors['green']}{self.colors['bold']}")
            print(frame)
            print(f"{self.colors['reset']}")
            
            # Add some sparkles
            sparkles = "✨ ⭐ 🌟 💫 ✨ ⭐ 🌟 💫"
            print(f"{self.colors['yellow']}{sparkles}{self.colors['reset']}")
            print()
            
            self.safe_sleep(frame_delay)
    
    def _animate_stats_display(self, player_stats: Dict[str, Any]):
        """Animate the display of player statistics."""
        self.clear_screen()
        
        print(f"{self.colors['cyan']}{self.colors['bold']}")
        print("📊 PERFORMANCE ANALYTICS")
        print("=" * 50)
        print(f"{self.colors['reset']}")
        
        stats_items = [
            ("Score", player_stats.get('score', 0), "points", self.colors['green']),
            ("XP Gained", player_stats.get('xp_earned', 0), "XP", self.colors['blue']),
            ("Coins Earned", player_stats.get('coins_earned', 0), "coins", self.colors['yellow']),
            ("Time Taken", player_stats.get('time_taken', 0), "seconds", self.colors['cyan']),
            ("Accuracy", player_stats.get('accuracy', 0), "%", self.colors['magenta'])
        ]
        
        for stat_name, value, unit, color in stats_items:
            # Animated counter effect
            if isinstance(value, (int, float)):
                self._animate_counter(stat_name, value, unit, color)
            self.safe_sleep(0.3)
        
        self.safe_sleep(1)
    
    def _animate_counter(self, name: str, target_value: float, unit: str, color: str):
        """Animate a counting effect for numerical values."""
        print(f"{name}:", end=" ")
        
        if target_value == 0:
            print(f"{color}0 {unit}{self.colors['reset']}")
            return
        
        # Optimize counter animation
        if self.fast_mode:
            steps = min(10, int(target_value))  # Fewer steps in fast mode
            delay = 0.02
        else:
            steps = min(15, int(target_value))
            delay = 0.03
            
        increment = target_value / steps if steps > 0 else target_value
        
        current = 0
        for i in range(steps):
            current += increment
            print(f"\r{name}: {color}{current:.0f} {unit}{self.colors['reset']}", end="", flush=True)
            self.safe_sleep(delay)
        
        print(f"\r{name}: {color}{target_value:.0f} {unit}{self.colors['reset']}")
    
    def _animate_level_unlock(self):
        """Animate the unlocking of the next level."""
        self.clear_screen()
        
        print(f"{self.colors['yellow']}{self.colors['bold']}")
        print("🔓 UNLOCKING NEXT LEVEL...")
        print(f"{self.colors['reset']}")
        
        # Optimized progress bar animation
        bar_length = 30 if self.fast_mode else 40
        delay = 0.05 if self.fast_mode else 0.08
        
        for i in range(bar_length + 1):
            percentage = (i / bar_length) * 100
            filled = "█" * i
            empty = "░" * (bar_length - i)
            
            print(f"\r[{filled}{empty}] {percentage:.0f}%", end="", flush=True)
            self.safe_sleep(delay)
        
        print("\n")
        print(f"{self.colors['green']}{self.colors['bold']}✅ NEXT LEVEL UNLOCKED!{self.colors['reset']}")
        self.safe_sleep(0.5 if self.fast_mode else 1)
    
    def animate_level_transition(self, from_level: int, to_level: int, topic: str):
        """Animate transition between levels with Python code morphing."""
        self.clear_screen()
        
        # Phase 1: Code morphing effect
        self._animate_code_morphing(from_level, to_level, topic)
        
        # Phase 2: Level bridge
        self._animate_level_bridge(from_level, to_level)
        
        # Phase 3: New level introduction
        self._animate_new_level_intro(to_level, topic)
    
    def _animate_code_morphing(self, from_level: int, to_level: int, topic: str):
        """Animate Python code morphing from one concept to another."""
        print(f"{self.colors['blue']}{self.colors['bold']}🔄 TRANSITIONING...{self.colors['reset']}")
        print()
        
        # Original code
        old_code = f"""
def level_{from_level}_solution():
    knowledge = "fundamental concepts"
    return apply(knowledge)
        """
        
        # New code
        new_code = f"""
def level_{to_level}_solution():
    knowledge = "{topic.lower()}"
    mastery = learn(knowledge)
    return advance(mastery)
        """
        
        # Morphing animation
        lines_old = old_code.strip().split('\n')
        lines_new = new_code.strip().split('\n')
        
        for i in range(max(len(lines_old), len(lines_new))):
            self.clear_screen()
            print(f"{self.colors['blue']}{self.colors['bold']}🔄 TRANSITIONING...{self.colors['reset']}")
            print()
            
            # Show transition
            for j, (old_line, new_line) in enumerate(zip(lines_old, lines_new)):
                if j <= i:
                    print(f"{self.colors['green']}{new_line}{self.colors['reset']}")
                else:
                    print(f"{self.colors['dim']}{old_line}{self.colors['reset']}")
            
            self.safe_sleep(0.5)
        
        self.safe_sleep(1)
    
    def _animate_level_bridge(self, from_level: int, to_level: int):
        """Animate a bridge connecting two levels."""
        self.clear_screen()
        
        bridge_frames = [
            f"""
    Level {from_level}     ╭─────╮     Level {to_level}
        🏁          │  ?  │         🚀
    ════════         ╰─────╯     ════════
            """,
            f"""
    Level {from_level}     ╭─────╮     Level {to_level}
        🏁          │ ──→ │         🚀
    ════════         ╰─────╯     ════════
            """,
            f"""
    Level {from_level}     ╭─────╮     Level {to_level}
        🏁    ────→ │ ═══ │ ←──── 🚀
    ════════         ╰─────╯     ════════
            """
        ]
        
        for frame in bridge_frames:
            self.clear_screen()
            print(f"{self.colors['cyan']}{self.colors['bold']}")
            print("🌉 CROSSING TO NEXT LEVEL...")
            print(f"{self.colors['reset']}")
            print(frame)
            self.safe_sleep(0.8)
    
    def _animate_new_level_intro(self, level: int, topic: str):
        """Introduce the new level with excitement."""
        self.clear_screen()
        
        # Typewriter effect for level introduction
        intro_text = f"""
🎯 WELCOME TO LEVEL {level}!

📚 Topic: {topic}
🎓 Ready to expand your Python mastery?
💡 New concepts await your discovery!

Let's code something amazing! 🐍✨
        """
        
        print(f"{self.colors['yellow']}{self.colors['bold']}")
        for char in intro_text:
            print(char, end='', flush=True)
            if char in '.!?':
                self.safe_sleep(0.3)
            elif char == '\n':
                self.safe_sleep(0.1)
            else:
                self.safe_sleep(0.03)
        
        print(f"{self.colors['reset']}")
        self.safe_sleep(2)
    
    def animate_achievement_unlock(self, achievement: Dict[str, Any]):
        """Animate achievement unlock with celebration."""
        self.clear_screen()
        
        # Achievement banner
        achievement_frames = [
            "🎉 ACHIEVEMENT UNLOCKED! 🎉",
            "✨ ACHIEVEMENT UNLOCKED! ✨",
            "🌟 ACHIEVEMENT UNLOCKED! 🌟",
            "💫 ACHIEVEMENT UNLOCKED! 💫"
        ]
        
        for frame in achievement_frames * 2:
            self.clear_screen()
            print(f"{self.colors['yellow']}{self.colors['bold']}")
            print("=" * 60)
            print(f"           {frame}")
            print("=" * 60)
            print()
            print(f"{self.colors['green']}{achievement.get('name', 'Unknown Achievement')}{self.colors['reset']}")
            print(f"{self.colors['cyan']}{achievement.get('description', '')}{self.colors['reset']}")
            print()
            print(f"{self.colors['yellow']}+{achievement.get('points', 0)} points!{self.colors['reset']}")
            print("=" * 60)
            print(f"{self.colors['reset']}")
            self.safe_sleep(0.5)
        
        self.safe_sleep(2)
    
    def animate_coding_challenge(self, challenge_name: str):
        """Animate the start of a coding challenge."""
        self.clear_screen()
        
        # Hacker-style code rain effect (simplified)
        print(f"{self.colors['green']}{self.colors['bold']}")
        print("⚡ CODING CHALLENGE INITIATED ⚡")
        print(f"{self.colors['reset']}")
        
        # Matrix-like code falling
        code_chars = list("def class import if else for while try except return print lambda")
        
        for _ in range(10):
            line = ""
            for _ in range(20):
                line += random.choice(code_chars) + " "
            print(f"{self.colors['green']}{self.colors['dim']}{line}{self.colors['reset']}")
            self.safe_sleep(0.1)
        
        print()
        print(f"{self.colors['red']}{self.colors['bold']}")
        print(f">>> CHALLENGE: {challenge_name}")
        print(">>> Prepare your Python skills!")
        print(">>> May the code be with you! 🐍")
        print(f"{self.colors['reset']}")
        self.safe_sleep(2)
    
    def animate_loading_next_lesson(self, lesson_title: str):
        """Animate loading the next lesson with Python import style."""
        self.clear_screen()
        
        loading_frames = [
            ">>> import next_lesson",
            ">>> import next_lesson.",
            ">>> import next_lesson..",
            ">>> import next_lesson..."
        ]
        
        for frame in loading_frames * 3:
            self.clear_screen()
            print(f"{self.colors['blue']}{self.colors['bold']}")
            print("🐍 PYTHON LEARNING ENVIRONMENT")
            print("=" * 50)
            print(f"{self.colors['reset']}")
            print()
            print(f"{self.colors['cyan']}{frame}{self.colors['reset']}")
            print()
            print(f"{self.colors['dim']}Loading: {lesson_title}{self.colors['reset']}")
            self.safe_sleep(0.5)
        
        # Success message
        self.clear_screen()
        print(f"{self.colors['blue']}{self.colors['bold']}")
        print("🐍 PYTHON LEARNING ENVIRONMENT")
        print("=" * 50)
        print(f"{self.colors['reset']}")
        print()
        print(f"{self.colors['green']}>>> from next_lesson import knowledge{self.colors['reset']}")
        print(f"{self.colors['green']}>>> knowledge.loaded_successfully(){self.colors['reset']}")
        print(f"{self.colors['yellow']}True{self.colors['reset']}")
        print()
        print(f"{self.colors['white']}{self.colors['bold']}{lesson_title}{self.colors['reset']}")
        self.safe_sleep(1.5)


class AnimationController:
    """Controls when and how animations are played."""
    
    def __init__(self):
        self.animator = PythonLevelAnimator()
        self.animation_enabled = True
        self.current_animation = None
        self.non_blocking = False  # For web compatibility
    
    def set_non_blocking(self, enabled: bool = True):
        """Enable non-blocking animations for web interface."""
        self.non_blocking = enabled
    
    def set_fast_mode(self, enabled: bool = True):
        """Enable fast animation mode."""
        self.animator.set_fast_mode(enabled)
    
    def play_level_completion(self, level_data: Dict[str, Any], player_stats: Dict[str, Any]):
        """Play level completion animation."""
        if not self.animation_enabled:
            return
        
        if self.non_blocking:
            # Non-blocking mode - return immediately
            self.current_animation = threading.Thread(
                target=self.animator.animate_level_completion,
                args=(level_data, player_stats),
                daemon=True
            )
            self.current_animation.start()
        else:
            # Blocking mode - wait for completion
            self.current_animation = threading.Thread(
                target=self.animator.animate_level_completion,
                args=(level_data, player_stats)
            )
            self.current_animation.start()
            self.current_animation.join()
    
    def play_level_transition(self, from_level: int, to_level: int, topic: str):
        """Play level transition animation."""
        if not self.animation_enabled:
            return
        
        self.current_animation = threading.Thread(
            target=self.animator.animate_level_transition,
            args=(from_level, to_level, topic)
        )
        self.current_animation.start()
    
    def play_achievement_unlock(self, achievement: Dict[str, Any]):
        """Play achievement unlock animation."""
        if not self.animation_enabled:
            return
        
        self.current_animation = threading.Thread(
            target=self.animator.animate_achievement_unlock,
            args=(achievement,)
        )
        self.current_animation.start()
    
    def play_challenge_start(self, challenge_name: str):
        """Play coding challenge start animation."""
        if not self.animation_enabled:
            return
        
        self.current_animation = threading.Thread(
            target=self.animator.animate_coding_challenge,
            args=(challenge_name,)
        )
        self.current_animation.start()
    
    def play_lesson_loading(self, lesson_title: str):
        """Play lesson loading animation."""
        if not self.animation_enabled:
            return
        
        self.current_animation = threading.Thread(
            target=self.animator.animate_loading_next_lesson,
            args=(lesson_title,)
        )
        self.current_animation.start()
    
    def wait_for_animation(self):
        """Wait for current animation to complete."""
        if self.current_animation and self.current_animation.is_alive():
            self.current_animation.join()
    
    def skip_animation(self):
        """Skip current animation."""
        self.animation_enabled = False
        if self.current_animation and self.current_animation.is_alive():
            # Note: Threading doesn't support direct termination
            # Animation will complete naturally
            pass
    
    def enable_animations(self):
        """Enable animations."""
        self.animation_enabled = True
    
    def disable_animations(self):
        """Disable animations."""
        self.animation_enabled = False


# Example usage and integration
def create_web_animations():
    """Create JavaScript animations for web interface."""
    return """
<script>
class WebLevelAnimator {
    constructor() {
        this.animationDuration = 2000; // 2 seconds
    }
    
    animateLevelCompletion(levelData, playerStats) {
        const container = document.createElement('div');
        container.className = 'level-completion-animation';
        container.innerHTML = `
            <div class="python-logo-animation">
                <div class="python-snake">🐍</div>
                <div class="completion-text">Level Complete!</div>
            </div>
            <div class="stats-animation">
                <div class="stat-item" data-stat="score">Score: ${playerStats.score}</div>
                <div class="stat-item" data-stat="xp">XP: +${playerStats.xp_earned}</div>
                <div class="stat-item" data-stat="coins">Coins: +${playerStats.coins_earned}</div>
            </div>
        `;
        
        document.body.appendChild(container);
        
        // Animate stats counting up
        this.animateCounters(container);
        
        // Remove after animation
        setTimeout(() => {
            document.body.removeChild(container);
        }, this.animationDuration);
    }
    
    animateCounters(container) {
        const statItems = container.querySelectorAll('.stat-item');
        statItems.forEach((item, index) => {
            setTimeout(() => {
                item.classList.add('animate-in');
            }, index * 200);
        });
    }
    
    animateLevelTransition(fromLevel, toLevel, topic) {
        const overlay = document.createElement('div');
        overlay.className = 'level-transition-overlay';
        overlay.innerHTML = `
            <div class="transition-content">
                <div class="code-morphing">
                    <pre class="old-code">def level_${fromLevel}():\\n    return "completed"</pre>
                    <div class="arrow">→</div>
                    <pre class="new-code">def level_${toLevel}():\\n    topic = "${topic}"\\n    return learn(topic)</pre>
                </div>
                <div class="level-bridge">
                    <span class="level-from">Level ${fromLevel}</span>
                    <span class="bridge">═══════</span>
                    <span class="level-to">Level ${toLevel}</span>
                </div>
            </div>
        `;
        
        document.body.appendChild(overlay);
        
        setTimeout(() => {
            overlay.classList.add('fade-out');
            setTimeout(() => {
                document.body.removeChild(overlay);
            }, 500);
        }, this.animationDuration);
    }
}

// CSS for animations
const animationCSS = `
.level-completion-animation {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.9);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    z-index: 10000;
    color: white;
}

.python-logo-animation {
    text-align: center;
    margin-bottom: 2rem;
}

.python-snake {
    font-size: 4rem;
    animation: bounce 1s infinite;
}

.completion-text {
    font-size: 2rem;
    font-weight: bold;
    color: #4CAF50;
    margin-top: 1rem;
}

.stats-animation {
    display: flex;
    gap: 2rem;
}

.stat-item {
    padding: 1rem 2rem;
    background: #2196F3;
    border-radius: 10px;
    font-weight: bold;
    opacity: 0;
    transform: translateY(50px);
    transition: all 0.5s ease;
}

.stat-item.animate-in {
    opacity: 1;
    transform: translateY(0);
}

.level-transition-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(45deg, #1e3c72, #2a5298);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 10000;
    color: white;
}

.transition-content {
    text-align: center;
}

.code-morphing {
    display: flex;
    align-items: center;
    gap: 2rem;
    margin-bottom: 2rem;
}

.old-code, .new-code {
    background: rgba(0, 0, 0, 0.7);
    padding: 1rem;
    border-radius: 5px;
    font-family: 'Courier New', monospace;
}

.arrow {
    font-size: 2rem;
    color: #4CAF50;
    animation: pulse 1s infinite;
}

.level-bridge {
    display: flex;
    align-items: center;
    gap: 1rem;
    font-size: 1.5rem;
}

.bridge {
    color: #FFD700;
    animation: glow 2s infinite;
}

@keyframes bounce {
    0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
    40% { transform: translateY(-20px); }
    60% { transform: translateY(-10px); }
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

@keyframes glow {
    0%, 100% { text-shadow: 0 0 5px #FFD700; }
    50% { text-shadow: 0 0 20px #FFD700, 0 0 30px #FFD700; }
}

.fade-out {
    opacity: 0;
    transition: opacity 0.5s ease;
}
`;

// Inject CSS
const style = document.createElement('style');
style.textContent = animationCSS;
document.head.appendChild(style);

// Initialize animator
const webAnimator = new WebLevelAnimator();
</script>
    """

if __name__ == "__main__":
    # Demo the animations
    animator = AnimationController()
    
    # Test level completion
    level_data = {"id": 5, "topic": "Functions", "difficulty": "Intermediate"}
    player_stats = {"score": 95, "xp_earned": 150, "coins_earned": 75, "time_taken": 300, "accuracy": 95}
    
    print("🎬 Starting animation demo...")
    animator.play_level_completion(level_data, player_stats)
    animator.wait_for_animation()
    
    # Test level transition
    animator.play_level_transition(5, 6, "Classes and Objects")
    animator.wait_for_animation()
    
    # Test achievement unlock
    achievement = {"name": "🧠 Quiz Master", "description": "Score 100% on any test", "points": 25}
    animator.play_achievement_unlock(achievement)
    animator.wait_for_animation()
    
    print("🎬 Animation demo completed!")


class AdvancedPythonAnimations:
    """Advanced Python-themed animations for special occasions."""
    
    def __init__(self):
        self.animator = PythonLevelAnimator()
        self.colors = self.animator.colors
    
    def animate_python_zen(self):
        """Display the Zen of Python with animated text."""
        zen_lines = [
            "Beautiful is better than ugly.",
            "Explicit is better than implicit.",
            "Simple is better than complex.",
            "Complex is better than complicated.",
            "Flat is better than nested.",
            "Sparse is better than dense.",
            "Readability counts.",
            "Special cases aren't special enough to break the rules.",
            "Although practicality beats purity.",
            "Errors should never pass silently.",
            "Unless explicitly silenced.",
            "In the face of ambiguity, refuse the temptation to guess.",
            "There should be one-- and preferably only one --obvious way to do it.",
            "Although that way may not be obvious at first unless you're Dutch.",
            "Now is better than never.",
            "Although never is often better than *right* now.",
            "If the implementation is hard to explain, it's a bad idea.",
            "If the implementation is easy to explain, it may be a good idea.",
            "Namespaces are one honking great idea -- let's do more of those!"
        ]
        
        self.animator.clear_screen()
        print(f"{self.colors['cyan']}{self.colors['bold']}")
        print("🐍 THE ZEN OF PYTHON 🐍")
        print("by Tim Peters")
        print("=" * 60)
        print(f"{self.colors['reset']}")
        
        for line in zen_lines:
            print(f"{self.colors['yellow']}{line}{self.colors['reset']}")
            self.animator.safe_sleep(1.2)
        
        print()
        print(f"{self.colors['green']}{self.colors['bold']}May these principles guide your Python journey!{self.colors['reset']}")
        self.animator.safe_sleep(3)
    
    def animate_code_rain(self, duration: int = 5):
        """Create an optimized Matrix-style code rain effect with Python keywords."""
        import os
        
        python_keywords = [
            'def', 'class', 'if', 'for', 'while', 'try', 'import', 
            'return', 'print', 'lambda', 'True', 'False', 'None'
        ]
        
        # Get terminal size with fallback
        try:
            columns, rows = os.get_terminal_size().columns, os.get_terminal_size().lines
        except:
            columns, rows = 80, 24
        
        # Reduce duration in fast mode
        if hasattr(self.animator, 'fast_mode') and self.animator.fast_mode:
            duration = min(duration, 3)
        
        # Optimize: fewer falling characters for better performance
        num_columns = min(columns // 10, 15)  # Fewer columns
        falling_chars = []
        
        for i in range(num_columns):
            col = (i * columns) // num_columns
            falling_chars.append({
                'col': col,
                'row': random.randint(-5, 0),
                'char': random.choice(python_keywords),
                'speed': random.randint(1, 2)  # Reduced speed variation
            })
        
        start_time = time.time()
        frame_count = 0
        target_fps = 15 if hasattr(self.animator, 'fast_mode') and self.animator.fast_mode else 10
        frame_time = 1.0 / target_fps
        
        while time.time() - start_time < duration:
            frame_start = time.time()
            
            self.animator.clear_screen()
            
            # Simplified grid rendering
            for char_data in falling_chars:
                char_data['row'] += char_data['speed']
                
                if char_data['row'] >= rows:
                    char_data['row'] = random.randint(-5, -1)
                    char_data['char'] = random.choice(python_keywords)
                
                if 0 <= char_data['row'] < rows:
                    # Direct positioning instead of full grid
                    print(f"\033[{char_data['row']+1};{char_data['col']+1}H{self.colors['green']}{char_data['char']}{self.colors['reset']}", end="")
            
            frame_count += 1
            
            # Frame rate limiting
            elapsed = time.time() - frame_start
            if elapsed < frame_time:
                time.sleep(frame_time - elapsed)
    
    def animate_typing_challenge(self, code_snippet: str):
        """Animate a typing challenge with optimized syntax highlighting."""
        self.animator.clear_screen()
        
        print(f"{self.colors['yellow']}{self.colors['bold']}")
        print("⌨️  TYPING CHALLENGE")
        print("Type the following Python code:")
        print("=" * 50)
        print(f"{self.colors['reset']}")
        
        # Show target code with optimized syntax highlighting
        lines = code_snippet.strip().split('\n')
        for line in lines:
            highlighted_line = self._syntax_highlight(line)
            print(highlighted_line)
        
        print("\n" + "=" * 50)
        print(f"{self.colors['cyan']}Start typing below:{self.colors['reset']}")
        
        # Optimized typing simulation for demo
        if hasattr(self.animator, 'fast_mode') and self.animator.fast_mode:
            # Fast mode: show chunks instead of character by character
            chunk_size = 10
            for i in range(0, len(code_snippet), chunk_size):
                chunk = code_snippet[i:i+chunk_size]
                typed_chars = code_snippet[:i+len(chunk)]
                self._display_typing_progress(code_snippet, typed_chars)
                self.animator.safe_sleep(0.1)
        else:
            # Normal mode: character by character but faster
            typed_chars = ""
            for char in code_snippet:
                typed_chars += char
                self._display_typing_progress(code_snippet, typed_chars)
                self.animator.safe_sleep(0.02)  # Faster typing simulation
    
    def _syntax_highlight(self, line: str) -> str:
        """Optimized syntax highlighting for Python code."""
        if not line.strip():
            return line
            
        # Pre-compiled patterns for better performance
        import re
        
        # Highlight keywords (faster lookup)
        keywords = {'def', 'class', 'import', 'from', 'if', 'else', 'for', 'while', 'try', 'except', 'return'}
        words = line.split()
        highlighted_words = []
        
        for word in words:
            clean_word = word.strip('():,')
            if clean_word in keywords:
                highlighted_words.append(word.replace(clean_word, f"{self.colors['blue']}{clean_word}{self.colors['reset']}"))
            else:
                highlighted_words.append(word)
        
        result = ' '.join(highlighted_words)
        
        # Highlight strings (optimized regex)
        result = re.sub(r'(["\'])([^"\']*?)\1', f"{self.colors['green']}\\1\\2\\1{self.colors['reset']}", result)
        
        # Highlight comments
        if '#' in result:
            result = re.sub(r'(#.*)', f"{self.colors['dim']}\\1{self.colors['reset']}", result)
        
        return result
    
    def _display_typing_progress(self, target: str, typed: str):
        """Display typing progress with correct/incorrect highlighting."""
        print("\033[2J\033[H")  # Clear screen and move cursor to top
        
        print(f"{self.colors['yellow']}{self.colors['bold']}⌨️  TYPING CHALLENGE{self.colors['reset']}")
        print("=" * 50)
        
        # Show progress
        correct_chars = 0
        for i, char in enumerate(typed):
            if i < len(target) and char == target[i]:
                correct_chars += 1
        
        accuracy = (correct_chars / len(typed) * 100) if typed else 100
        print(f"Progress: {len(typed)}/{len(target)} characters")
        print(f"Accuracy: {accuracy:.1f}%")
        print()
        
        # Show typed text with highlighting
        result = ""
        for i, char in enumerate(typed):
            if i < len(target):
                if char == target[i]:
                    result += f"{self.colors['green']}{char}{self.colors['reset']}"
                else:
                    result += f"{self.colors['red']}{char}{self.colors['reset']}"
            else:
                result += f"{self.colors['red']}{char}{self.colors['reset']}"
        
        print(result)
    
    def animate_error_debugging(self, error_type: str, error_message: str):
        """Animate a debugging scenario with error analysis."""
        self.animator.clear_screen()
        
        print(f"{self.colors['red']}{self.colors['bold']}")
        print("🐛 DEBUG MODE ACTIVATED")
        print("=" * 50)
        print(f"{self.colors['reset']}")
        
        # Simulate error detection
        print(f"{self.colors['yellow']}Analyzing code...{self.colors['reset']}")
        self.animator.safe_sleep(1)
        
        print(f"{self.colors['yellow']}Scanning for errors...{self.colors['reset']}")
        for i in range(3):
            print(".", end="", flush=True)
            self.animator.safe_sleep(0.5)
        print()
        
        # Show error
        print(f"{self.colors['red']}{self.colors['bold']}")
        print(f"❌ {error_type}: {error_message}")
        print(f"{self.colors['reset']}")
        
        # Show debugging steps
        debugging_steps = [
            "🔍 Examining stack trace...",
            "📝 Identifying error location...",
            "💡 Suggesting solution...",
            "✅ Ready to fix!"
        ]
        
        for step in debugging_steps:
            print(f"{self.colors['cyan']}{step}{self.colors['reset']}")
            self.animator.safe_sleep(1)
    
    def animate_level_boss_fight(self, boss_name: str, boss_difficulty: str):
        """Animate a boss fight for major milestone levels with optimized performance."""
        self.animator.clear_screen()
        
        # Boss introduction
        boss_art = f"""
        ⚔️  BOSS CHALLENGE  ⚔️
        
        A wild {boss_name} appears!
        
           🐉
          /|\\    Difficulty: {boss_difficulty}
         / | \\   
        
        Prepare for the ultimate coding battle!
        """
        
        print(f"{self.colors['red']}{self.colors['bold']}")
        print(boss_art)
        print(f"{self.colors['reset']}")
        
        # Optimized battle phases
        phases = [
            "🗡️  Phase 1: Logic Challenges",
            "🛡️  Phase 2: Algorithm Design", 
            "✨ Phase 3: Code Optimization",
            "👑 Final Phase: Creative Problem Solving"
        ]
        
        progress_steps = 10 if hasattr(self.animator, 'fast_mode') and self.animator.fast_mode else 20
        step_delay = 0.05 if hasattr(self.animator, 'fast_mode') and self.animator.fast_mode else 0.08
        
        for i, phase in enumerate(phases):
            print(f"{self.colors['yellow']}{phase}{self.colors['reset']}")
            
            # Optimized progress bar for each phase
            for j in range(progress_steps + 1):
                percentage = (j / progress_steps) * 100
                filled_length = int(j * 20 / progress_steps)
                progress = "█" * filled_length + "░" * (20 - filled_length)
                print(f"\r[{progress}] {percentage:.0f}%", end="", flush=True)
                self.animator.safe_sleep(step_delay)
            print(f" ✅ Complete!")
            self.animator.safe_sleep(0.2)
        
        # Victory celebration
        print(f"\n{self.colors['green']}{self.colors['bold']}")
        print("🎉 BOSS DEFEATED! 🎉")
        print("You are truly a Python master!")
        print(f"{self.colors['reset']}")
        self.animator.safe_sleep(1 if hasattr(self.animator, 'fast_mode') and self.animator.fast_mode else 2)
    
    def animate_skill_tree_unlock(self, skill_name: str, prerequisites: List[str]):
        """Animate skill tree progression with node connections."""
        self.animator.clear_screen()
        
        print(f"{self.colors['cyan']}{self.colors['bold']}")
        print("🌳 SKILL TREE PROGRESSION")
        print("=" * 50)
        print(f"{self.colors['reset']}")
        
        # Show prerequisites
        if prerequisites:
            print(f"{self.colors['green']}Prerequisites mastered:{self.colors['reset']}")
            for prereq in prerequisites:
                print(f"  ✅ {prereq}")
            print()
        
        # Animate skill unlock
        print(f"{self.colors['yellow']}Unlocking new skill...{self.colors['reset']}")
        
        # Draw skill tree branch
        tree_art = f"""
        
        🌿 {prerequisites[0] if prerequisites else "Foundation"}
         |
         └─── 🌱 {skill_name}
              |
              └─── 🔒 Next Skills
        
        """
        
        lines = tree_art.strip().split('\n')
        for line in lines:
            print(f"{self.colors['green']}{line}{self.colors['reset']}")
            self.animator.safe_sleep(0.3)
        
        print(f"{self.colors['yellow']}{self.colors['bold']}")
        print(f"🎯 {skill_name} UNLOCKED!")
        print("New learning paths are now available!")
        print(f"{self.colors['reset']}")
        self.animator.safe_sleep(2)


class InteractiveAnimations:
    """Interactive animations that respond to user input."""
    
    def __init__(self):
        self.animator = PythonLevelAnimator()
        self.advanced = AdvancedPythonAnimations()
        self.colors = self.animator.colors
    
    def interactive_code_builder(self):
        """Interactive animation for building Python code step by step."""
        self.animator.clear_screen()
        
        print(f"{self.colors['cyan']}{self.colors['bold']}")
        print("🔧 INTERACTIVE CODE BUILDER")
        print("Build a Python function step by step!")
        print("=" * 50)
        print(f"{self.colors['reset']}")
        
        code_parts = [
            ("Function definition", "def calculate_area(length, width):"),
            ("Docstring", '    """Calculate the area of a rectangle."""'),
            ("Calculation", "    area = length * width"),
            ("Return statement", "    return area"),
            ("Function call", "result = calculate_area(5, 3)"),
            ("Output", "print(f'Area: {result}')")
        ]
        
        built_code = []
        
        for i, (description, code_line) in enumerate(code_parts):
            print(f"\n{self.colors['yellow']}Step {i+1}: {description}{self.colors['reset']}")
            print(f"Adding: {self.colors['green']}{code_line}{self.colors['reset']}")
            
            input("Press Enter to add this line...")
            
            built_code.append(code_line)
            
            # Show current code
            self.animator.clear_screen()
            print(f"{self.colors['cyan']}{self.colors['bold']}BUILDING YOUR FUNCTION:{self.colors['reset']}\n")
            
            for line in built_code:
                print(f"{self.colors['blue']}{line}{self.colors['reset']}")
            
            if i < len(code_parts) - 1:
                print(f"\n{self.colors['dim']}...more to come...{self.colors['reset']}")
        
        # Final celebration
        print(f"\n{self.colors['green']}{self.colors['bold']}")
        print("🎉 FUNCTION COMPLETE!")
        print("You've built a working Python function!")
        print(f"{self.colors['reset']}")
    
    def python_quiz_wheel(self, questions: List[Dict[str, Any]]):
        """Animated quiz wheel for selecting random questions."""
        self.animator.clear_screen()
        
        print(f"{self.colors['yellow']}{self.colors['bold']}")
        print("🎰 PYTHON KNOWLEDGE WHEEL")
        print("Spin the wheel to get your question!")
        print("=" * 40)
        print(f"{self.colors['reset']}")
        
        # Wheel segments
        wheel_segments = [
            "Variables", "Functions", "Loops", "Classes", 
            "Modules", "Exceptions", "File I/O", "Decorators"
        ]
        
        input("Press Enter to spin the wheel...")
        
        # Spinning animation
        for _ in range(20):
            selected = random.choice(wheel_segments)
            print(f"\r🎯 {selected}     ", end="", flush=True)
            self.animator.safe_sleep(0.1)
        
        final_topic = random.choice(wheel_segments)
        print(f"\r🎯 {final_topic}! ✨")
        
        # Find matching question
        matching_questions = [q for q in questions if final_topic.lower() in q.get('topic', '').lower()]
        
        if matching_questions:
            question = random.choice(matching_questions)
            print(f"\n{self.colors['cyan']}Your question about {final_topic}:{self.colors['reset']}")
            print(f"\n{question.get('question', 'Sample question')}")
            
            if 'options' in question:
                for i, option in enumerate(question['options'], 1):
                    print(f"{i}. {option}")
        
        self.animator.safe_sleep(3)


# Integration function for web animations
def generate_web_animation_script():
    """Generate enhanced JavaScript animation script for web interface."""
    return """
<script>
// Enhanced Web Animations for Python Learning Game
class EnhancedWebAnimator {
    constructor() {
        this.particles = [];
        this.canvas = null;
        this.ctx = null;
        this.setupCanvas();
    }
    
    setupCanvas() {
        this.canvas = document.createElement('canvas');
        this.canvas.id = 'animation-canvas';
        this.canvas.style.position = 'fixed';
        this.canvas.style.top = '0';
        this.canvas.style.left = '0';
        this.canvas.style.pointerEvents = 'none';
        this.canvas.style.zIndex = '9999';
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
        this.ctx = this.canvas.getContext('2d');
        document.body.appendChild(this.canvas);
    }
    
    createParticleExplosion(x, y, color = '#4CAF50') {
        for (let i = 0; i < 20; i++) {
            this.particles.push({
                x: x,
                y: y,
                vx: (Math.random() - 0.5) * 10,
                vy: (Math.random() - 0.5) * 10,
                life: 1.0,
                color: color,
                size: Math.random() * 5 + 2
            });
        }
        this.animateParticles();
    }
    
    animateParticles() {
        const animate = () => {
            this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
            
            this.particles = this.particles.filter(particle => {
                particle.x += particle.vx;
                particle.y += particle.vy;
                particle.vy += 0.2; // gravity
                particle.life -= 0.02;
                
                this.ctx.save();
                this.ctx.globalAlpha = particle.life;
                this.ctx.fillStyle = particle.color;
                this.ctx.beginPath();
                this.ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
                this.ctx.fill();
                this.ctx.restore();
                
                return particle.life > 0;
            });
            
            if (this.particles.length > 0) {
                requestAnimationFrame(animate);
            }
        };
        animate();
    }
    
    showFloatingText(text, x, y, color = '#FFD700', duration = 2000) {
        const textElement = document.createElement('div');
        textElement.style.position = 'fixed';
        textElement.style.left = x + 'px';
        textElement.style.top = y + 'px';
        textElement.style.color = color;
        textElement.style.fontSize = '24px';
        textElement.style.fontWeight = 'bold';
        textElement.style.pointerEvents = 'none';
        textElement.style.zIndex = '10000';
        textElement.style.transition = 'all 2s ease-out';
        textElement.textContent = text;
        
        document.body.appendChild(textElement);
        
        setTimeout(() => {
            textElement.style.transform = 'translateY(-100px)';
            textElement.style.opacity = '0';
            
            setTimeout(() => {
                document.body.removeChild(textElement);
            }, 2000);
        }, 100);
    }
    
    animateXPGain(amount, targetElement) {
        const rect = targetElement.getBoundingClientRect();
        this.showFloatingText(`+${amount} XP`, rect.right, rect.top, '#4CAF50');
        this.createParticleExplosion(rect.right, rect.top, '#4CAF50');
    }
    
    animateCoinsEarned(amount, targetElement) {
        const rect = targetElement.getBoundingClientRect();
        this.showFloatingText(`+${amount} coins`, rect.right, rect.top, '#FFD700');
        this.createParticleExplosion(rect.right, rect.top, '#FFD700');
    }
    
    cleanup() {
        if (this.canvas) {
            document.body.removeChild(this.canvas);
        }
    }
}

// Initialize enhanced animator
window.enhancedAnimator = new EnhancedWebAnimator();

// Auto-cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (window.enhancedAnimator) {
        window.enhancedAnimator.cleanup();
    }
});
</script>
    """
