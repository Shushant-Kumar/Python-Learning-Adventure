"""
Game Logic for Python Learning Adventure
Handles level progression, tests, rewards, and achievements
"""

import json
import random
from typing import Dict, List, Any, Optional
from datetime import datetime

class GameLogic:
    """Core game logic for the Python learning adventure."""
    
    def __init__(self):
        self.levels = self._load_levels()
        self.tests = self._load_tests()
        self.rewards = self._load_rewards()
        self.achievements = self._load_achievements()
    
    def _load_levels(self) -> List[Dict[str, Any]]:
        """Load level data - 100 levels with tests every 10 levels."""
        levels = []
        
        # Level topics cycle
        topics = [
            "Python Basics", "Variables & Data Types", "Strings & Input", 
            "Operators", "Control Flow", "If Statements", "Loops", 
            "Functions", "Lists", "Dictionaries", "Sets", "Tuples",
            "File Handling", "Error Handling", "Classes & Objects",
            "Inheritance", "Modules", "Advanced Topics"
        ]
        
        difficulties = ["Beginner", "Easy", "Medium", "Hard", "Expert"]
        
        for i in range(1, 101):  # 100 levels
            is_test_level = (i % 10 == 0)  # Every 10th level is a test
            topic_index = ((i - 1) // 6) % len(topics)
            difficulty_index = min((i - 1) // 20, len(difficulties) - 1)
            
            if is_test_level:
                level = {
                    "id": i,
                    "type": "test",
                    "title": f"Test Level {i}",
                    "topic": f"{topics[topic_index]} - Assessment",
                    "difficulty": difficulties[difficulty_index],
                    "description": f"Test your knowledge of {topics[topic_index]}",
                    "questions": self._generate_test_questions(i, topics[topic_index]),
                    "rewards": {
                        "stars": 3,
                        "coins": 100 + (i // 10) * 50,
                        "xp": 200 + (i // 10) * 25
                    }
                }
            else:
                level = {
                    "id": i,
                    "type": "lesson",
                    "title": f"Level {i}: {topics[topic_index]}",
                    "topic": topics[topic_index],
                    "difficulty": difficulties[difficulty_index],
                    "description": f"Learn about {topics[topic_index]}",
                    "content": self._generate_lesson_content(i, topics[topic_index]),
                    "code_example": self._generate_code_example(i, topics[topic_index]),
                    "quiz": self._generate_quiz_questions(i, topics[topic_index]),
                    "rewards": {
                        "stars": 1,
                        "coins": 20 + (i // 10) * 5,
                        "xp": 50 + (i // 10) * 10
                    }
                }
            
            levels.append(level)
        
        return levels
    
    def _generate_lesson_content(self, level_id: int, topic: str) -> str:
        """Generate lesson content based on level and topic."""
        content_templates = {
            "Python Basics": f"""
            Welcome to Python Level {level_id}!
            
            Python is a powerful, easy-to-learn programming language. In this level, we'll explore:
            
            • What makes Python special
            • Basic syntax rules
            • How to write your first program
            • Understanding Python's philosophy
            
            Key Points:
            - Python is interpreted, not compiled
            - Indentation matters in Python
            - Python is case-sensitive
            - Use meaningful variable names
            """,
            
            "Variables & Data Types": f"""
            Level {level_id}: Understanding Variables and Data Types
            
            Variables are containers that store data values. Python has several built-in data types:
            
            • int: Integer numbers (1, 2, 3)
            • float: Decimal numbers (1.5, 2.7)
            • str: Text strings ("Hello", 'World')
            • bool: True or False values
            • list: Ordered collections [1, 2, 3]
            • dict: Key-value pairs {{'name': 'John'}}
            
            Remember: Python determines the type automatically!
            """,
            
            "Strings & Input": f"""
            Level {level_id}: Working with Strings and User Input
            
            Strings are sequences of characters. Learn how to:
            
            • Create strings with quotes
            • Use string methods (.upper(), .lower(), .strip())
            • Format strings with f-strings
            • Get user input with input()
            • Handle string operations
            
            Pro Tip: Always validate user input!
            """,
            
            "Control Flow": f"""
            Level {level_id}: Controlling Program Flow
            
            Control flow statements determine the order of execution:
            
            • if statements: Make decisions
            • elif statements: Multiple conditions
            • else statements: Default actions
            • Comparison operators: ==, !=, <, >, <=, >=
            • Logical operators: and, or, not
            
            Master these to create intelligent programs!
            """,
            
            "Loops": f"""
            Level {level_id}: Mastering Loops
            
            Loops allow you to repeat code efficiently:
            
            • for loops: Iterate over sequences
            • while loops: Repeat while condition is True
            • range(): Generate number sequences
            • break: Exit loops early
            • continue: Skip to next iteration
            
            Loops are essential for automation!
            """,
            
            "Functions": f"""
            Level {level_id}: Creating and Using Functions
            
            Functions are reusable blocks of code:
            
            • def keyword: Define functions
            • Parameters: Input values
            • Return values: Output results
            • Scope: Local vs global variables
            • Docstrings: Document your functions
            
            Good functions make code clean and maintainable!
            """
        }
        
        return content_templates.get(topic, f"Level {level_id}: {topic} - Advanced Python concepts and practical applications.")
    
    def _generate_code_example(self, level_id: int, topic: str) -> str:
        """Generate code examples for lessons."""
        examples = {
            "Python Basics": """# Your first Python program
print("Hello, Python World!")
print(f"This is level {level_id}")

# Python is interactive
name = "Learner"
print(f"Welcome, {name}!")""",
            
            "Variables & Data Types": """# Variables and data types
name = "Alice"          # String
age = 25               # Integer
height = 5.6           # Float
is_student = True      # Boolean

# Check types
print(type(name))      # <class 'str'>
print(type(age))       # <class 'int'>

# Lists and dictionaries
grades = [85, 92, 78]  # List
student = {"name": "Bob", "age": 20}  # Dictionary""",
            
            "Strings & Input": """# Working with strings
message = "Hello, World!"
print(message.upper())     # HELLO, WORLD!
print(message.lower())     # hello, world!
print(len(message))        # 13

# F-strings (formatted strings)
name = "Python"
version = 3.9
print(f"I'm learning {name} {version}!")

# User input
user_name = input("What's your name? ")
print(f"Nice to meet you, {user_name}!")""",
            
            "Control Flow": """# If statements
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "F"

print(f"Your grade is: {grade}")

# Logical operators
age = 20
has_license = True

if age >= 18 and has_license:
    print("You can drive!")
else:
    print("You cannot drive yet.")""",
            
            "Loops": """# For loops
for i in range(5):
    print(f"Count: {i}")

# Loop through a list
fruits = ["apple", "banana", "orange"]
for fruit in fruits:
    print(f"I like {fruit}")

# While loop
count = 0
while count < 3:
    print(f"Count: {count}")
    count += 1

# Loop with break
for i in range(10):
    if i == 5:
        break
    print(i)""",
            
            "Functions": """# Define a function
def greet(name):
    \"\"\"Greet someone by name\"\"\"
    return f"Hello, {name}!"

# Call the function
message = greet("Alice")
print(message)

# Function with multiple parameters
def calculate_area(length, width):
    \"\"\"Calculate rectangle area\"\"\"
    return length * width

area = calculate_area(5, 3)
print(f"Area: {area}")

# Function with default parameter
def greet_with_title(name, title="Mr."):
    return f"Hello, {title} {name}!"

print(greet_with_title("Smith"))"""
        }
        
        return examples.get(topic, f"# Level {level_id}: {topic}\n# Advanced Python example\nprint('Keep learning!')")
    
    def _generate_quiz_questions(self, level_id: int, topic: str) -> List[Dict[str, Any]]:
        """Generate quiz questions for lessons."""
        questions = []
        
        if "Python Basics" in topic:
            questions = [
                {
                    "question": "What is the correct way to print 'Hello World' in Python?",
                    "type": "multiple_choice",
                    "options": ["print('Hello World')", "echo('Hello World')", "printf('Hello World')", "console.log('Hello World')"],
                    "correct": 0,
                    "explanation": "In Python, we use the print() function to display output."
                },
                {
                    "question": "Which of these is a valid Python variable name?",
                    "type": "multiple_choice",
                    "options": ["2name", "user-name", "user_name", "user name"],
                    "correct": 2,
                    "explanation": "Variable names cannot start with numbers, contain hyphens, or have spaces."
                }
            ]
        
        elif "Variables" in topic:
            questions = [
                {
                    "question": "What data type is 3.14?",
                    "type": "multiple_choice",
                    "options": ["int", "float", "str", "bool"],
                    "correct": 1,
                    "explanation": "3.14 is a decimal number, which is a float data type."
                },
                {
                    "question": "How do you check the type of a variable in Python?",
                    "type": "multiple_choice",
                    "options": ["typeof(variable)", "type(variable)", "variable.type()", "check_type(variable)"],
                    "correct": 1,
                    "explanation": "Use the type() function to check a variable's data type."
                }
            ]
        
        elif "Strings" in topic:
            questions = [
                {
                    "question": "What does len('Python') return?",
                    "type": "multiple_choice",
                    "options": ["5", "6", "7", "Error"],
                    "correct": 1,
                    "explanation": "len() returns the number of characters in a string. 'Python' has 6 characters."
                },
                {
                    "question": "How do you create an f-string in Python?",
                    "type": "multiple_choice",
                    "options": ["f'Hello {name}'", "'Hello {name}'", "format('Hello {name}')", "printf('Hello {name}')"],
                    "correct": 0,
                    "explanation": "F-strings are created by prefixing a string with 'f' and using {} for variables."
                }
            ]
        
        elif "Control Flow" in topic:
            questions = [
                {
                    "question": "Which operator checks if two values are equal?",
                    "type": "multiple_choice",
                    "options": ["=", "==", "!=", "is"],
                    "correct": 1,
                    "explanation": "== is used for equality comparison, while = is for assignment."
                },
                {
                    "question": "What does the 'and' operator do?",
                    "type": "multiple_choice",
                    "options": ["Returns True if one condition is True", "Returns True if both conditions are True", "Returns False always", "Returns True always"],
                    "correct": 1,
                    "explanation": "The 'and' operator returns True only when both conditions are True."
                }
            ]
        
        elif "Loops" in topic:
            questions = [
                {
                    "question": "What does range(5) generate?",
                    "type": "multiple_choice",
                    "options": ["[1, 2, 3, 4, 5]", "[0, 1, 2, 3, 4]", "[0, 1, 2, 3, 4, 5]", "[1, 2, 3, 4]"],
                    "correct": 1,
                    "explanation": "range(5) generates numbers from 0 to 4 (5 is excluded)."
                },
                {
                    "question": "What does 'break' do in a loop?",
                    "type": "multiple_choice",
                    "options": ["Pauses the loop", "Skips current iteration", "Exits the loop completely", "Restarts the loop"],
                    "correct": 2,
                    "explanation": "'break' exits the loop immediately and continues with the code after the loop."
                }
            ]
        
        elif "Functions" in topic:
            questions = [
                {
                    "question": "How do you define a function in Python?",
                    "type": "multiple_choice",
                    "options": ["function myFunc():", "def myFunc():", "create myFunc():", "func myFunc():"],
                    "correct": 1,
                    "explanation": "Use the 'def' keyword to define functions in Python."
                },
                {
                    "question": "What does a function return if no return statement is specified?",
                    "type": "multiple_choice",
                    "options": ["0", "Empty string", "None", "Error"],
                    "correct": 2,
                    "explanation": "Functions without a return statement automatically return None."
                }
            ]
        
        # Add more questions based on level difficulty
        if level_id > 50:
            questions.append({
                "question": f"Advanced concept for level {level_id}: What is the best practice for this topic?",
                "type": "multiple_choice",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct": 0,
                "explanation": "This is an advanced concept that builds on previous knowledge."
            })
        
        return questions
    
    def _generate_test_questions(self, level_id: int, topic: str) -> List[Dict[str, Any]]:
        """Generate comprehensive test questions for every 10th level."""
        questions = []
        
        # Base questions for all tests
        base_questions = [
            {
                "question": "What is the output of print(type(42))?",
                "type": "multiple_choice",
                "options": ["<class 'int'>", "<class 'float'>", "int", "42"],
                "correct": 0,
                "explanation": "The type() function returns the class of the object."
            },
            {
                "question": "Which of these is a mutable data type in Python?",
                "type": "multiple_choice",
                "options": ["string", "tuple", "list", "integer"],
                "correct": 2,
                "explanation": "Lists are mutable, meaning they can be modified after creation."
            },
            {
                "question": "What does the following code print?\n\nfor i in range(3):\n    print(i)",
                "type": "multiple_choice",
                "options": ["0 1 2", "1 2 3", "0 1 2 3", "1 2"],
                "correct": 0,
                "explanation": "range(3) generates numbers from 0 to 2."
            }
        ]
        
        # Add level-specific questions
        if level_id <= 20:
            questions.extend([
                {
                    "question": "Write a Python function that takes a name as parameter and returns a greeting.",
                    "type": "code",
                    "placeholder": "def greet(name):\n    # Your code here\n    return",
                    "expected_keywords": ["def", "greet", "return"],
                    "explanation": "Functions should use 'def' keyword and return a value."
                }
            ])
        
        elif level_id <= 40:
            questions.extend([
                {
                    "question": "What is the difference between a list and a tuple?",
                    "type": "multiple_choice",
                    "options": ["Lists are mutable, tuples are immutable", "Lists are immutable, tuples are mutable", "No difference", "Lists are faster"],
                    "correct": 0,
                    "explanation": "Lists can be modified after creation, tuples cannot."
                },
                {
                    "question": "Write a loop that prints numbers from 1 to 5.",
                    "type": "code",
                    "placeholder": "# Write your loop here",
                    "expected_keywords": ["for", "range", "print"],
                    "explanation": "Use a for loop with range(1, 6)."
                }
            ])
        
        elif level_id <= 60:
            questions.extend([
                {
                    "question": "What is the purpose of the 'self' parameter in class methods?",
                    "type": "multiple_choice",
                    "options": ["It refers to the class", "It refers to the instance", "It's optional", "It's a keyword"],
                    "correct": 1,
                    "explanation": "'self' refers to the instance of the class."
                }
            ])
        
        # Combine base questions with level-specific ones
        all_questions = base_questions + questions
        
        # Return random selection for variety
        return random.sample(all_questions, min(len(all_questions), 5))
    
    def _load_tests(self) -> List[Dict[str, Any]]:
        """Load test data for every 10th level."""
        return []  # Tests are generated dynamically in _load_levels()
    
    def _load_rewards(self) -> List[Dict[str, Any]]:
        """Load reward data."""
        return [
            {"id": "theme_dark", "name": "🌙 Dark Theme", "cost": 100, "type": "theme", "description": "Sleek dark theme for nighttime learning"},
            {"id": "theme_colorful", "name": "🌈 Colorful Theme", "cost": 150, "type": "theme", "description": "Vibrant colors to brighten your learning"},
            {"id": "xp_boost", "name": "🚀 XP Booster", "cost": 200, "type": "boost", "description": "Double XP for the next 5 levels"},
            {"id": "hint_pack", "name": "💡 Hint Pack", "cost": 75, "type": "consumable", "description": "Get hints for difficult questions"},
            {"id": "skip_level", "name": "⏭️ Level Skip", "cost": 300, "type": "consumable", "description": "Skip one difficult level"},
            {"id": "certificate", "name": "🏆 Certificate", "cost": 500, "type": "achievement", "description": "Python proficiency certificate"},
            {"id": "badge_bronze", "name": "🥉 Bronze Badge", "cost": 250, "type": "badge", "description": "Bronze learner badge"},
            {"id": "badge_silver", "name": "🥈 Silver Badge", "cost": 400, "type": "badge", "description": "Silver learner badge"},
            {"id": "badge_gold", "name": "🥇 Gold Badge", "cost": 600, "type": "badge", "description": "Gold master badge"},
            {"id": "avatar_ninja", "name": "🥷 Ninja Avatar", "cost": 300, "type": "avatar", "description": "Stealthy ninja avatar"}
        ]
    
    def _load_achievements(self) -> List[Dict[str, Any]]:
        """Load achievement data."""
        return [
            {"id": "first_level", "name": "🎯 First Steps", "description": "Complete your first level", "condition": "levels_completed", "requirement": 1},
            {"id": "test_master", "name": "🧠 Test Master", "description": "Complete your first test", "condition": "tests_completed", "requirement": 1},
            {"id": "perfect_score", "name": "⭐ Perfect Score", "description": "Get 100% on any test", "condition": "perfect_test", "requirement": 1},
            {"id": "level_10", "name": "🔟 Decade", "description": "Complete 10 levels", "condition": "levels_completed", "requirement": 10},
            {"id": "level_25", "name": "🎖️ Quarter Century", "description": "Complete 25 levels", "condition": "levels_completed", "requirement": 25},
            {"id": "level_50", "name": "🏅 Half Century", "description": "Complete 50 levels", "condition": "levels_completed", "requirement": 50},
            {"id": "level_100", "name": "👑 Century", "description": "Complete all 100 levels", "condition": "levels_completed", "requirement": 100},
            {"id": "streak_3", "name": "🔥 Hot Streak", "description": "3-day learning streak", "condition": "streak", "requirement": 3},
            {"id": "streak_7", "name": "🌟 Week Warrior", "description": "7-day learning streak", "condition": "streak", "requirement": 7},
            {"id": "streak_30", "name": "🚀 Monthly Master", "description": "30-day learning streak", "condition": "streak", "requirement": 30},
            {"id": "python_pro", "name": "🐍 Python Pro", "description": "Complete 5 test levels", "condition": "tests_completed", "requirement": 5},
            {"id": "coin_collector", "name": "💰 Coin Collector", "description": "Collect 1000 coins", "condition": "coins_earned", "requirement": 1000}
        ]
    
    def get_level_map(self, player) -> List[Dict[str, Any]]:
        """Get the level map for display."""
        level_map = []
        
        for level in self.levels:
            level_info = {
                "id": level["id"],
                "type": level["type"],
                "title": level["title"],
                "difficulty": level["difficulty"],
                "topic": level["topic"],
                "completed": level["id"] in player.completed_levels,
                "unlocked": level["id"] <= player.current_level,
                "stars": player.level_stars.get(str(level["id"]), 0),
                "rewards": level["rewards"]
            }
            level_map.append(level_info)
        
        return level_map
    
    def get_level_data(self, level_id: int, player) -> Optional[Dict[str, Any]]:
        """Get data for a specific level."""
        if level_id > player.current_level:
            return None
        
        level = next((l for l in self.levels if l["id"] == level_id), None)
        if not level:
            return None
        
        return level
    
    def get_test_data(self, level_id: int, player) -> Optional[Dict[str, Any]]:
        """Get test data for a specific level."""
        if level_id % 10 != 0 or level_id > player.current_level:
            return None
        
        level = next((l for l in self.levels if l["id"] == level_id and l["type"] == "test"), None)
        return level
    
    def complete_level(self, player, level_id: int, quiz_answers: List[int]) -> Dict[str, Any]:
        """Complete a level and update player progress."""
        level = next((l for l in self.levels if l["id"] == level_id), None)
        if not level or level["type"] != "lesson":
            return {"success": False, "error": "Invalid level"}
        
        # Calculate score
        correct_answers = 0
        total_questions = len(level["quiz"])
        
        for i, user_answer in enumerate(quiz_answers):
            if i < len(level["quiz"]) and user_answer == level["quiz"][i]["correct"]:
                correct_answers += 1
        
        score_percentage = (correct_answers / total_questions) * 100 if total_questions > 0 else 100
        
        # Calculate stars (1-3 based on score)
        if score_percentage >= 90:
            stars = 3
        elif score_percentage >= 70:
            stars = 2
        else:
            stars = 1
        
        # Update player progress
        if level_id not in player.completed_levels:
            player.completed_levels.append(level_id)
        
        player.level_stars[str(level_id)] = max(player.level_stars.get(str(level_id), 0), stars)
        
        # Award coins and XP
        coins_earned = level["rewards"]["coins"] * stars
        xp_earned = level["rewards"]["xp"] * stars
        
        player.coins += coins_earned
        player.total_xp += xp_earned
        
        # Unlock next level
        if level_id == player.current_level:
            player.current_level += 1
        
        # Check for achievements
        new_achievements = self._check_achievements(player)
        
        # Check for level-up
        leveled_up = self._check_level_up(player)
        
        return {
            "success": True,
            "score": score_percentage,
            "stars": stars,
            "coins_earned": coins_earned,
            "xp_earned": xp_earned,
            "new_achievements": new_achievements,
            "leveled_up": leveled_up,
            "correct_answers": correct_answers,
            "total_questions": total_questions
        }
    
    def complete_test(self, player, level_id: int, test_answers: List[int]) -> Dict[str, Any]:
        """Complete a test and update player progress."""
        level = next((l for l in self.levels if l["id"] == level_id), None)
        if not level or level["type"] != "test":
            return {"success": False, "error": "Invalid test"}
        
        # Calculate score
        correct_answers = 0
        total_questions = len(level["questions"])
        
        for i, user_answer in enumerate(test_answers):
            if i < len(level["questions"]) and user_answer == level["questions"][i]["correct"]:
                correct_answers += 1
        
        score_percentage = (correct_answers / total_questions) * 100 if total_questions > 0 else 100
        
        # Tests require at least 60% to pass
        passed = score_percentage >= 60
        stars = 0
        coins_earned = 0
        xp_earned = 0
        
        if passed:
            # Calculate stars (1-3 based on score)
            if score_percentage >= 90:
                stars = 3
            elif score_percentage >= 75:
                stars = 2
            else:
                stars = 1
            
            # Update player progress
            if level_id not in player.completed_levels:
                player.completed_levels.append(level_id)
            
            player.level_stars[str(level_id)] = max(player.level_stars.get(str(level_id), 0), stars)
            
            # Award coins and XP (tests give more rewards)
            coins_earned = level["rewards"]["coins"] * stars
            xp_earned = level["rewards"]["xp"] * stars
            
            player.coins += coins_earned
            player.total_xp += xp_earned
            
            # Unlock next level
            if level_id == player.current_level:
                player.current_level += 1
            
            # Special reward for completing 10 levels in a row
            if level_id % 10 == 0:
                bonus_coins = 200
                bonus_xp = 100
                player.coins += bonus_coins
                player.total_xp += bonus_xp
                coins_earned += bonus_coins
                xp_earned += bonus_xp
        
        # Check for achievements
        new_achievements = self._check_achievements(player)
        
        # Check for level-up
        leveled_up = self._check_level_up(player)
        
        return {
            "success": True,
            "passed": passed,
            "score": score_percentage,
            "stars": stars,
            "coins_earned": coins_earned,
            "xp_earned": xp_earned,
            "new_achievements": new_achievements,
            "leveled_up": leveled_up,
            "correct_answers": correct_answers,
            "total_questions": total_questions,
            "completion_bonus": level_id % 10 == 0 and passed
        }
    
    def _check_achievements(self, player) -> List[Dict[str, Any]]:
        """Check for new achievements."""
        new_achievements = []
        
        for achievement in self.achievements:
            if achievement["id"] in player.achievements:
                continue
            
            earned = False
            
            if achievement["condition"] == "levels_completed":
                if len(player.completed_levels) >= achievement["requirement"]:
                    earned = True
            elif achievement["condition"] == "tests_completed":
                test_levels = [l for l in player.completed_levels if l % 10 == 0]
                if len(test_levels) >= achievement["requirement"]:
                    earned = True
            elif achievement["condition"] == "perfect_test":
                # Check if any test has 3 stars
                for level_id in player.completed_levels:
                    if level_id % 10 == 0 and player.level_stars.get(str(level_id), 0) == 3:
                        earned = True
                        break
            elif achievement["condition"] == "streak":
                if player.streak >= achievement["requirement"]:
                    earned = True
            elif achievement["condition"] == "coins_earned":
                if player.coins >= achievement["requirement"]:
                    earned = True
            
            if earned:
                player.achievements.append(achievement["id"])
                new_achievements.append(achievement)
        
        return new_achievements
    
    def _check_level_up(self, player) -> bool:
        """Check if player leveled up."""
        # Simple level up system based on XP
        required_xp = player.player_level * 1000
        if player.total_xp >= required_xp:
            player.player_level += 1
            return True
        return False
    
    def get_available_rewards(self, player) -> List[Dict[str, Any]]:
        """Get available rewards for purchase."""
        available_rewards = []
        
        for reward in self.rewards:
            reward_info = reward.copy()
            reward_info["owned"] = reward["id"] in player.purchased_rewards
            reward_info["can_afford"] = player.coins >= reward["cost"]
            available_rewards.append(reward_info)
        
        return available_rewards
    
    def purchase_reward(self, player, reward_id: str) -> Dict[str, Any]:
        """Purchase a reward."""
        reward = next((r for r in self.rewards if r["id"] == reward_id), None)
        if not reward:
            return {"success": False, "error": "Reward not found"}
        
        if reward_id in player.purchased_rewards:
            return {"success": False, "error": "Already purchased"}
        
        if player.coins < reward["cost"]:
            return {"success": False, "error": "Not enough coins"}
        
        player.coins -= reward["cost"]
        player.purchased_rewards.append(reward_id)
        
        return {"success": True, "reward": reward}
    
    def get_achievements(self, player) -> Dict[str, Any]:
        """Get player achievements."""
        unlocked = []
        locked = []
        
        for achievement in self.achievements:
            if achievement["id"] in player.achievements:
                unlocked.append(achievement)
            else:
                locked.append(achievement)
        
        return {
            "unlocked": unlocked,
            "locked": locked,
            "total": len(self.achievements)
        }
    
    def get_player_stats(self, player) -> Dict[str, Any]:
        """Get player statistics."""
        total_levels = len(self.levels)
        completed_levels = len(player.completed_levels)
        test_levels = len([l for l in player.completed_levels if l % 10 == 0])
        
        total_stars = sum(player.level_stars.values())
        max_stars = completed_levels * 3
        
        return {
            "levels_completed": completed_levels,
            "total_levels": total_levels,
            "completion_percentage": (completed_levels / total_levels) * 100,
            "tests_completed": test_levels,
            "total_stars": total_stars,
            "max_stars": max_stars,
            "star_percentage": (total_stars / max_stars) * 100 if max_stars > 0 else 0,
            "achievements_unlocked": len(player.achievements),
            "total_achievements": len(self.achievements),
            "rewards_purchased": len(player.purchased_rewards),
            "total_rewards": len(self.rewards)
        }
