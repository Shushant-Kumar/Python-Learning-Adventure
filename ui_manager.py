"""
UI Manager for the Python Learning Game
Handles all user interface interactions and display formatting
"""

import os
from typing import Dict, List, Any
from player import Player

class UIManager:
    """Manages all user interface interactions."""
    
    def __init__(self):
        self.colors = {
            'header': '\033[95m',
            'blue': '\033[94m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'red': '\033[91m',
            'end': '\033[0m',
            'bold': '\033[1m',
            'underline': '\033[4m'
        }
    
    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_main_menu(self, player: Player) -> str:
        """Display the main menu and get user choice."""
        print(f"\n{self.colors['header']}🎮 PYTHON LEARNING ADVENTURE{self.colors['end']}")
        print(f"Welcome back, {self.colors['bold']}{player.name}{self.colors['end']}!")
        print(f"Level: {player.level} | XP: {player.experience} | Coins: 💰{player.coins} | Streak: 🔥{player.streak}")
        print("-" * 60)
        
        menu_options = [
            "1. 📚 Start Learning (Play Levels)",
            "2. 📝 Take a Test",
            "3. 📊 View Progress & Achievements",
            "4. 🏆 View Rewards Shop",
            "5. ⚙️ Settings",
            "6. 🚪 Save & Exit"
        ]
        
        for option in menu_options:
            print(option)
        
        print("-" * 60)
        return input("Choose an option (1-6): ").strip()
    
    def show_level_menu(self, available_levels: List[Dict[str, Any]]) -> str:
        """Display available levels and get user choice."""
        print(f"\n{self.colors['blue']}📚 LEARNING LEVELS{self.colors['end']}")
        print("-" * 40)
        
        for i, level in enumerate(available_levels, 1):
            status = "✅" if level.get('completed', False) else "🔒" if level.get('locked', True) else "📖"
            difficulty = level.get('difficulty', 'Beginner')
            
            print(f"{i}. {status} {level['title']}")
            print(f"   Difficulty: {difficulty} | Topic: {level['topic']}")
            print(f"   Description: {level['description']}")
            print()
        
        print("0. ⬅️ Back to Main Menu")
        print("-" * 40)
        return input("Choose a level (0 to go back): ").strip()
    
    def show_lesson_content(self, lesson: Dict[str, Any]):
        """Display lesson content."""
        print(f"\n{self.colors['header']}📖 LESSON: {lesson['title']}{self.colors['end']}")
        print("=" * 60)
        
        print(f"\n{self.colors['bold']}Topic:{self.colors['end']} {lesson['topic']}")
        print(f"{self.colors['bold']}Difficulty:{self.colors['end']} {lesson['difficulty']}")
        print(f"{self.colors['bold']}Estimated Time:{self.colors['end']} {lesson.get('duration', '15 minutes')}")
        
        print(f"\n{self.colors['blue']}📝 CONTENT:{self.colors['end']}")
        print(lesson['content'])
        
        if 'code_example' in lesson:
            print(f"\n{self.colors['green']}💻 CODE EXAMPLE:{self.colors['end']}")
            print(f"```python\n{lesson['code_example']}\n```")
        
        if 'tips' in lesson:
            print(f"\n{self.colors['yellow']}💡 TIPS:{self.colors['end']}")
            for tip in lesson['tips']:
                print(f"• {tip}")
        
        print("\n" + "=" * 60)
    
    def show_quiz_question(self, question: Dict[str, Any], question_num: int, total_questions: int) -> str:
        """Display a quiz question and get user answer."""
        print(f"\n{self.colors['header']}❓ QUESTION {question_num}/{total_questions}{self.colors['end']}")
        print("-" * 50)
        
        print(f"\n{question['question']}")
        
        if question['type'] == 'multiple_choice':
            print(f"\n{self.colors['blue']}Options:{self.colors['end']}")
            for i, option in enumerate(question['options'], 1):
                print(f"{i}. {option}")
            
            return input(f"\nYour answer (1-{len(question['options'])}): ").strip()
        
        elif question['type'] == 'code':
            print(f"\n{self.colors['green']}Write your code below:{self.colors['end']}")
            print("(Type 'DONE' on a new line when finished)")
            
            code_lines = []
            while True:
                line = input()
                if line.strip() == 'DONE':
                    break
                code_lines.append(line)
            
            return '\n'.join(code_lines)
        
        else:  # text answer
            return input("Your answer: ").strip()
    
    def show_quiz_result(self, score: int, total: int, feedback: List[str]):
        """Display quiz results."""
        percentage = (score / total) * 100
        
        print(f"\n{self.colors['header']}📊 QUIZ RESULTS{self.colors['end']}")
        print("=" * 40)
        
        if percentage >= 90:
            grade = f"{self.colors['green']}A+ Excellent!{self.colors['end']}"
            emoji = "🌟"
        elif percentage >= 80:
            grade = f"{self.colors['green']}A Good Job!{self.colors['end']}"
            emoji = "⭐"
        elif percentage >= 70:
            grade = f"{self.colors['yellow']}B Not Bad!{self.colors['end']}"
            emoji = "👍"
        elif percentage >= 60:
            grade = f"{self.colors['yellow']}C Keep Trying!{self.colors['end']}"
            emoji = "💪"
        else:
            grade = f"{self.colors['red']}F Need More Practice{self.colors['end']}"
            emoji = "📚"
        
        print(f"\n{emoji} Score: {score}/{total} ({percentage:.1f}%)")
        print(f"Grade: {grade}")
        
        if feedback:
            print(f"\n{self.colors['blue']}📝 FEEDBACK:{self.colors['end']}")
            for fb in feedback:
                print(f"• {fb}")
        
        print("\n" + "=" * 40)
    
    def show_progress(self, player: Player):
        """Display player progress and achievements."""
        print(f"\n{self.colors['header']}📊 YOUR PROGRESS{self.colors['end']}")
        print("=" * 60)
        
        progress = player.get_progress_summary()
        
        print(f"\n{self.colors['bold']}Player Profile:{self.colors['end']}")
        print(f"Name: {progress['name']}")
        print(f"Level: {progress['level']}")
        print(f"Experience: {progress['experience']} XP")
        print(f"Coins: 💰{progress['coins']}")
        print(f"Current Streak: 🔥{progress['streak']} days")
        
        print(f"\n{self.colors['bold']}Learning Stats:{self.colors['end']}")
        print(f"Lessons Completed: {progress['lessons_completed']}")
        print(f"Tests Taken: {progress['tests_taken']}")
        print(f"Average Test Score: {progress['average_test_score']:.1f}%")
        
        print(f"\n{self.colors['bold']}🏆 Achievements ({progress['achievements_count']}):{self.colors['end']}")
        if player.achievements:
            for achievement in player.achievements:
                print(f"• {achievement}")
        else:
            print("No achievements yet. Keep learning!")
        
        print(f"\n{self.colors['bold']}🎁 Rewards Unlocked ({progress['rewards_unlocked']}):{self.colors['end']}")
        if player.unlocked_rewards:
            for reward in player.unlocked_rewards:
                print(f"• {reward}")
        else:
            print("No rewards unlocked yet. Earn more coins!")
        
        input(f"\n{self.colors['blue']}Press Enter to continue...{self.colors['end']}")
    
    def show_rewards(self, player: Player):
        """Display the rewards shop."""
        print(f"\n{self.colors['header']}🏆 REWARDS SHOP{self.colors['end']}")
        print("=" * 50)
        print(f"Your Coins: 💰{player.coins}")
        print("-" * 50)
        
        rewards = [
            {"name": "🎨 Custom Theme", "cost": 100, "description": "Personalize your learning experience"},
            {"name": "🚀 XP Booster", "cost": 150, "description": "Double XP for next 3 lessons"},
            {"name": "🏅 Achievement Badge", "cost": 200, "description": "Show off your Python skills"},
            {"name": "📚 Bonus Content", "cost": 300, "description": "Access advanced Python topics"},
            {"name": "🎯 Skill Certificate", "cost": 500, "description": "Official Python proficiency certificate"}
        ]
        
        for i, reward in enumerate(rewards, 1):
            status = "✅ OWNED" if reward['name'] in player.unlocked_rewards else f"💰{reward['cost']}"
            print(f"{i}. {reward['name']} - {status}")
            print(f"   {reward['description']}")
            print()
        
        print("0. ⬅️ Back to Main Menu")
        print("-" * 50)
        
        choice = input("Choose a reward to purchase (0 to go back): ").strip()
        
        if choice.isdigit() and 1 <= int(choice) <= len(rewards):
            reward = rewards[int(choice) - 1]
            if reward['name'] in player.unlocked_rewards:
                print(f"\n{self.colors['yellow']}You already own this reward!{self.colors['end']}")
            elif player.unlock_reward(reward['name'], reward['cost']):
                print(f"\n{self.colors['green']}🎉 Congratulations! You unlocked: {reward['name']}{self.colors['end']}")
            else:
                print(f"\n{self.colors['red']}❌ Not enough coins! You need {reward['cost'] - player.coins} more coins.{self.colors['end']}")
            
            input(f"\n{self.colors['blue']}Press Enter to continue...{self.colors['end']}")
    
    def show_settings(self):
        """Display settings menu."""
        print(f"\n{self.colors['header']}⚙️ SETTINGS{self.colors['end']}")
        print("=" * 30)
        print("1. 🔊 Sound Effects: ON")
        print("2. 🎨 Theme: Default")
        print("3. 💾 Reset Progress")
        print("4. ❓ Help & Tutorial")
        print("0. ⬅️ Back to Main Menu")
        print("-" * 30)
        
        choice = input("Choose an option: ").strip()
        
        if choice == "4":
            self.show_help()
        elif choice == "3":
            confirm = input(f"\n{self.colors['red']}⚠️ Are you sure you want to reset ALL progress? (yes/no): {self.colors['end']}")
            if confirm.lower() == 'yes':
                print(f"{self.colors['green']}Progress reset! (Feature not implemented yet){self.colors['end']}")
        
        input(f"\n{self.colors['blue']}Press Enter to continue...{self.colors['end']}")
    
    def show_help(self):
        """Display help information."""
        print(f"\n{self.colors['header']}❓ HELP & TUTORIAL{self.colors['end']}")
        print("=" * 50)
        
        help_text = """
🎮 HOW TO PLAY:
1. Complete lessons to earn XP and coins
2. Take tests to check your knowledge
3. Earn achievements for milestones
4. Spend coins in the rewards shop
5. Maintain your daily streak for bonuses

📚 LEARNING TIPS:
• Read each lesson carefully
• Practice the code examples
• Don't skip the exercises
• Review incorrect answers
• Ask questions when stuck

🏆 ACHIEVEMENTS:
• First Steps - Complete your first lesson
• Quiz Master - Get 100% on any test
• Streak Master - Maintain 7-day streak
• Level Up - Reach level 5
• Python Pro - Complete all lessons

💰 EARNING COINS:
• 1 coin per 10 XP earned
• 25 coins per achievement
• 50 coins per level up
• Bonus coins for high test scores
        """
        
        print(help_text)
        input(f"\n{self.colors['blue']}Press Enter to continue...{self.colors['end']}")
    
    def show_level_completed(self, level_title: str, xp_earned: int, coins_earned: int):
        """Display level completion message."""
        print(f"\n{self.colors['green']}🎉 LEVEL COMPLETED!{self.colors['end']}")
        print("=" * 40)
        print(f"✅ {level_title}")
        print(f"🌟 XP Earned: +{xp_earned}")
        print(f"💰 Coins Earned: +{coins_earned}")
        print("=" * 40)
        
        input(f"\n{self.colors['blue']}Press Enter to continue...{self.colors['end']}")
    
    def show_achievement_unlocked(self, achievement_name: str):
        """Display achievement unlocked message."""
        print(f"\n{self.colors['yellow']}🏆 ACHIEVEMENT UNLOCKED!{self.colors['end']}")
        print(f"🎯 {achievement_name}")
        print(f"💰 Bonus: +25 coins")
        
        input(f"\n{self.colors['blue']}Press Enter to continue...{self.colors['end']}")
    
    def show_level_up(self, new_level: int):
        """Display level up message."""
        print(f"\n{self.colors['header']}🌟 LEVEL UP!{self.colors['end']}")
        print(f"🎊 Congratulations! You reached Level {new_level}!")
        print(f"💰 Level up bonus: +50 coins")
        
        input(f"\n{self.colors['blue']}Press Enter to continue...{self.colors['end']}")
