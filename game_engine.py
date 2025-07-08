"""
Game Engine for Python Learning Game
Handles core game logic, lessons, tests, and progression
"""

import json
import random
from typing import Dict, List, Any, Optional
from player import Player
from ui_manager import UIManager

class GameEngine:
    """Core game engine that manages lessons, tests, and progression."""
    
    def __init__(self):
        self.ui = UIManager()
        self.lessons = self._load_lessons()
        self.tests = self._load_tests()
        self.achievements = self._load_achievements()
    
    def _load_lessons(self) -> List[Dict[str, Any]]:
        """Load lesson data."""
        return [
            {
                "id": "python_basics_1",
                "title": "Python Basics - Variables and Data Types",
                "topic": "Variables",
                "difficulty": "Beginner",
                "duration": "15 minutes",
                "level_requirement": 1,
                "content": """
Welcome to Python! Let's start with the fundamentals.

VARIABLES:
Variables are containers for storing data. In Python, you don't need to declare 
variable types explicitly - Python figures it out automatically!

Creating variables:
- Use descriptive names
- Start with a letter or underscore
- Case sensitive (age ≠ Age)
- No spaces (use underscores instead)

DATA TYPES:
1. Integers (int) - Whole numbers: 42, -7, 0
2. Floats (float) - Decimal numbers: 3.14, -2.5
3. Strings (str) - Text: "Hello", 'Python'
4. Booleans (bool) - True or False

You can check a variable's type using type() function.
                """,
                "code_example": """# Creating variables
name = "Alice"
age = 25
height = 5.6
is_student = True

# Checking types
print(type(name))      # <class 'str'>
print(type(age))       # <class 'int'>
print(type(height))    # <class 'float'>
print(type(is_student)) # <class 'bool'>

# Variables can change
age = 26
print(f"Name: {name}, Age: {age}")
                """,
                "tips": [
                    "Use meaningful variable names like 'user_name' instead of 'x'",
                    "Python is case-sensitive: 'Name' and 'name' are different",
                    "Use snake_case for variable names (words separated by underscores)"
                ],
                "quiz": [
                    {
                        "question": "Which of these is a valid variable name?",
                        "type": "multiple_choice",
                        "options": ["2name", "user-name", "user_name", "user name"],
                        "correct": 2,
                        "explanation": "Variable names cannot start with numbers, contain hyphens, or have spaces. user_name follows Python naming conventions."
                    },
                    {
                        "question": "What data type is the value 3.14?",
                        "type": "multiple_choice",
                        "options": ["int", "float", "str", "bool"],
                        "correct": 1,
                        "explanation": "3.14 is a decimal number, which is a float data type."
                    }
                ]
            },
            {
                "id": "python_basics_2",
                "title": "Python Basics - Strings and Input",
                "topic": "Strings",
                "difficulty": "Beginner",
                "duration": "20 minutes",
                "level_requirement": 1,
                "content": """
STRINGS:
Strings are sequences of characters enclosed in quotes.

Creating strings:
- Use single quotes: 'Hello'
- Use double quotes: "Hello"
- Use triple quotes for multi-line: '''Hello'''

STRING OPERATIONS:
- Concatenation: "Hello" + " World"
- Repetition: "Ha" * 3 = "HaHaHa"
- Length: len("Hello") = 5
- Indexing: "Hello"[0] = 'H'
- Slicing: "Hello"[1:4] = 'ell'

STRING METHODS:
- .upper() - Convert to uppercase
- .lower() - Convert to lowercase
- .strip() - Remove whitespace
- .replace() - Replace characters
- .split() - Split into list

F-STRINGS (formatted strings):
Use f"text {variable}" for easy string formatting.

INPUT:
Use input() to get user input (always returns a string).
                """,
                "code_example": """# String creation
greeting = "Hello, World!"
name = 'Python'

# String operations
full_greeting = greeting + " Welcome to " + name
print(full_greeting)

# String methods
text = "  Python Programming  "
print(text.upper())
print(text.strip())
print(text.replace("Python", "Java"))

# F-strings
user_name = "Alice"
age = 25
message = f"Hello {user_name}, you are {age} years old!"
print(message)

# User input
user_input = input("Enter your name: ")
print(f"Nice to meet you, {user_input}!")
                """,
                "tips": [
                    "Use f-strings for cleaner string formatting",
                    "Remember that input() always returns a string",
                    "Use .strip() to remove extra whitespace from user input",
                    "String indices start at 0, not 1"
                ],
                "quiz": [
                    {
                        "question": "What does len('Python') return?",
                        "type": "multiple_choice",
                        "options": ["5", "6", "7", "Error"],
                        "correct": 1,
                        "explanation": "len() returns the number of characters in a string. 'Python' has 6 characters."
                    },
                    {
                        "question": "What is the output of 'Hello'[1:3]?",
                        "type": "multiple_choice",
                        "options": ["'He'", "'el'", "'ell'", "'lo'"],
                        "correct": 1,
                        "explanation": "String slicing [1:3] returns characters from index 1 up to (but not including) index 3."
                    }
                ]
            },
            {
                "id": "python_control_1",
                "title": "Control Flow - If Statements",
                "topic": "Control Flow",
                "difficulty": "Beginner",
                "duration": "25 minutes",
                "level_requirement": 2,
                "content": """
CONDITIONAL STATEMENTS:
If statements allow your program to make decisions based on conditions.

BASIC IF STATEMENT:
if condition:
    # code to execute if condition is True

IF-ELSE:
if condition:
    # code if True
else:
    # code if False

IF-ELIF-ELSE:
if condition1:
    # code if condition1 is True
elif condition2:
    # code if condition2 is True
else:
    # code if all conditions are False

COMPARISON OPERATORS:
- == (equal to)
- != (not equal to)
- < (less than)
- > (greater than)
- <= (less than or equal to)
- >= (greater than or equal to)

LOGICAL OPERATORS:
- and (both conditions must be True)
- or (at least one condition must be True)
- not (inverts the condition)

INDENTATION:
Python uses indentation to define code blocks. Use 4 spaces or 1 tab consistently.
                """,
                "code_example": """# Basic if statement
age = 18
if age >= 18:
    print("You are an adult!")

# If-else
temperature = 25
if temperature > 30:
    print("It's hot outside!")
else:
    print("Weather is pleasant.")

# If-elif-else
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
elif age >= 18 and not has_license:
    print("You need a license to drive.")
else:
    print("You're too young to drive.")
                """,
                "tips": [
                    "Always use consistent indentation (4 spaces recommended)",
                    "Use == for comparison, not = (which is assignment)",
                    "Logical operators: and, or, not (not &&, ||, ! like other languages)",
                    "You can combine multiple conditions with logical operators"
                ],
                "quiz": [
                    {
                        "question": "What will this code print?\n\nage = 16\nif age >= 18:\n    print('Adult')\nelse:\n    print('Minor')",
                        "type": "multiple_choice",
                        "options": ["Adult", "Minor", "Error", "Nothing"],
                        "correct": 1,
                        "explanation": "Since age (16) is not >= 18, the condition is False, so the else block executes."
                    },
                    {
                        "question": "Which operator checks if two values are equal?",
                        "type": "multiple_choice",
                        "options": ["=", "==", "!=", "is"],
                        "correct": 1,
                        "explanation": "== is used for equality comparison, while = is for assignment."
                    }
                ]
            },
            {
                "id": "python_loops_1",
                "title": "Loops - For and While",
                "topic": "Loops",
                "difficulty": "Intermediate",
                "duration": "30 minutes",
                "level_requirement": 3,
                "content": """
LOOPS:
Loops allow you to repeat code multiple times.

FOR LOOPS:
Used when you know how many times to repeat or want to iterate over a sequence.

Basic for loop:
for item in sequence:
    # code to repeat

Common patterns:
- range(n): numbers from 0 to n-1
- range(start, stop): numbers from start to stop-1
- range(start, stop, step): numbers with custom step

WHILE LOOPS:
Used when you want to repeat code while a condition is True.

while condition:
    # code to repeat
    # don't forget to update the condition!

LOOP CONTROL:
- break: exit the loop immediately
- continue: skip the rest of the current iteration
- else: executes if loop completes normally (no break)

NESTED LOOPS:
You can put loops inside other loops.
                """,
                "code_example": """# For loop with range
print("Counting to 5:")
for i in range(1, 6):
    print(f"Count: {i}")

# For loop with list
fruits = ["apple", "banana", "orange"]
for fruit in fruits:
    print(f"I like {fruit}")

# For loop with string
word = "Python"
for letter in word:
    print(letter)

# While loop
count = 0
while count < 3:
    print(f"Count is {count}")
    count += 1  # Important: update the condition!

# Loop with break and continue
for i in range(10):
    if i == 3:
        continue  # Skip 3
    if i == 7:
        break     # Stop at 7
    print(i)

# Nested loops
for i in range(3):
    for j in range(2):
        print(f"i={i}, j={j}")
                """,
                "tips": [
                    "Use for loops when you know the number of iterations",
                    "Use while loops when the number of iterations depends on a condition",
                    "Always make sure while loop conditions will eventually become False",
                    "Use break and continue to control loop flow when needed"
                ],
                "quiz": [
                    {
                        "question": "What does range(3) generate?",
                        "type": "multiple_choice",
                        "options": ["[1, 2, 3]", "[0, 1, 2]", "[0, 1, 2, 3]", "[1, 2]"],
                        "correct": 1,
                        "explanation": "range(3) generates numbers from 0 to 2 (3 is excluded)."
                    },
                    {
                        "question": "What happens if you forget to update the condition in a while loop?",
                        "type": "multiple_choice",
                        "options": ["The loop runs once", "The loop doesn't run", "Infinite loop", "Syntax error"],
                        "correct": 2,
                        "explanation": "If the condition never becomes False, the loop will run forever (infinite loop)."
                    }
                ]
            },
            {
                "id": "python_functions_1",
                "title": "Functions - Defining and Calling",
                "topic": "Functions",
                "difficulty": "Intermediate",
                "duration": "35 minutes",
                "level_requirement": 4,
                "content": """
FUNCTIONS:
Functions are reusable blocks of code that perform specific tasks.

DEFINING FUNCTIONS:
def function_name(parameters):
    \"\"\"Optional docstring\"\"\"
    # function body
    return value  # optional

CALLING FUNCTIONS:
function_name(arguments)

PARAMETERS VS ARGUMENTS:
- Parameters: variables in function definition
- Arguments: actual values passed to function

TYPES OF PARAMETERS:
1. Required parameters
2. Default parameters
3. Keyword arguments
4. Variable arguments (*args, **kwargs)

RETURN VALUES:
- Functions can return values using 'return'
- If no return statement, function returns None
- Can return multiple values as tuple

SCOPE:
- Local variables: exist only inside function
- Global variables: exist outside function
- Use 'global' keyword to modify global variables inside function

DOCSTRINGS:
Use triple quotes to document what your function does.
                """,
                "code_example": """# Basic function
def greet(name):
    \"\"\"Greet someone by name\"\"\"
    return f"Hello, {name}!"

# Calling the function
message = greet("Alice")
print(message)

# Function with default parameter
def greet_with_title(name, title="Mr."):
    return f"Hello, {title} {name}!"

print(greet_with_title("Smith"))
print(greet_with_title("Johnson", "Dr."))

# Function with multiple parameters
def calculate_area(length, width):
    \"\"\"Calculate rectangle area\"\"\"
    area = length * width
    return area

result = calculate_area(5, 3)
print(f"Area: {result}")

# Function returning multiple values
def get_name_age():
    name = input("Enter your name: ")
    age = int(input("Enter your age: "))
    return name, age

user_name, user_age = get_name_age()
print(f"Name: {user_name}, Age: {user_age}")

# Function with variable arguments
def sum_numbers(*args):
    \"\"\"Sum any number of arguments\"\"\"
    total = 0
    for num in args:
        total += num
    return total

print(sum_numbers(1, 2, 3, 4, 5))
                """,
                "tips": [
                    "Use descriptive function names that explain what the function does",
                    "Keep functions small and focused on a single task",
                    "Use docstrings to document your functions",
                    "Prefer return values over printing inside functions for reusability"
                ],
                "quiz": [
                    {
                        "question": "What does this function return?\n\ndef mystery(x):\n    return x * 2\n\nresult = mystery(5)",
                        "type": "multiple_choice",
                        "options": ["5", "10", "25", "None"],
                        "correct": 1,
                        "explanation": "The function multiplies the input by 2, so mystery(5) returns 10."
                    },
                    {
                        "question": "What happens if a function doesn't have a return statement?",
                        "type": "multiple_choice",
                        "options": ["Error", "Returns 0", "Returns None", "Returns empty string"],
                        "correct": 2,
                        "explanation": "Functions without a return statement automatically return None."
                    }
                ]
            }
        ]
    
    def _load_tests(self) -> List[Dict[str, Any]]:
        """Load test data."""
        return [
            {
                "id": "basics_test",
                "title": "Python Basics Test",
                "description": "Test your knowledge of Python variables, data types, and strings",
                "level_requirement": 2,
                "questions": [
                    {
                        "question": "Which of the following is NOT a valid Python data type?",
                        "type": "multiple_choice",
                        "options": ["int", "float", "char", "str"],
                        "correct": 2,
                        "explanation": "Python doesn't have a 'char' data type. Single characters are just strings of length 1."
                    },
                    {
                        "question": "What is the output of: print(type(42))?",
                        "type": "multiple_choice",
                        "options": ["<class 'int'>", "<class 'float'>", "int", "42"],
                        "correct": 0,
                        "explanation": "The type() function returns the class of the object, which is <class 'int'> for integer 42."
                    },
                    {
                        "question": "How do you create a multi-line string in Python?",
                        "type": "multiple_choice",
                        "options": ["Use \\n", "Use triple quotes", "Use double quotes", "Use single quotes"],
                        "correct": 1,
                        "explanation": "Triple quotes (''' or \"\"\") allow you to create multi-line strings in Python."
                    },
                    {
                        "question": "Write a Python code that creates a variable 'name' with your name and prints it using an f-string.",
                        "type": "code",
                        "expected_concepts": ["variable", "f-string", "print"],
                        "sample_answer": "name = 'Alice'\nprint(f'My name is {name}')"
                    }
                ]
            },
            {
                "id": "control_flow_test",
                "title": "Control Flow Test",
                "description": "Test your understanding of if statements and conditional logic",
                "level_requirement": 3,
                "questions": [
                    {
                        "question": "What is the output of this code?\n\nx = 10\nif x > 5:\n    print('A')\nelif x > 15:\n    print('B')\nelse:\n    print('C')",
                        "type": "multiple_choice",
                        "options": ["A", "B", "C", "A and B"],
                        "correct": 0,
                        "explanation": "Since x=10 is > 5, the first condition is True, so 'A' is printed. elif is not checked when if is True."
                    },
                    {
                        "question": "Which logical operator returns True if both conditions are True?",
                        "type": "multiple_choice",
                        "options": ["or", "and", "not", "xor"],
                        "correct": 1,
                        "explanation": "The 'and' operator returns True only when both conditions are True."
                    },
                    {
                        "question": "Write an if-else statement that checks if a number is positive, negative, or zero.",
                        "type": "code",
                        "expected_concepts": ["if", "elif", "else", "comparison"],
                        "sample_answer": "num = 5\nif num > 0:\n    print('positive')\nelif num < 0:\n    print('negative')\nelse:\n    print('zero')"
                    }
                ]
            },
            {
                "id": "loops_test",
                "title": "Loops Test",
                "description": "Test your knowledge of for loops and while loops",
                "level_requirement": 4,
                "questions": [
                    {
                        "question": "What does range(2, 8, 2) generate?",
                        "type": "multiple_choice",
                        "options": ["[2, 4, 6]", "[2, 4, 6, 8]", "[2, 3, 4, 5, 6, 7]", "[0, 2, 4, 6, 8]"],
                        "correct": 0,
                        "explanation": "range(2, 8, 2) starts at 2, goes up to (but not including) 8, with step 2: [2, 4, 6]."
                    },
                    {
                        "question": "What does 'continue' do in a loop?",
                        "type": "multiple_choice",
                        "options": ["Exits the loop", "Skips current iteration", "Restarts the loop", "Pauses the loop"],
                        "correct": 1,
                        "explanation": "'continue' skips the rest of the current iteration and moves to the next one."
                    },
                    {
                        "question": "Write a for loop that prints numbers from 1 to 5.",
                        "type": "code",
                        "expected_concepts": ["for", "range", "print"],
                        "sample_answer": "for i in range(1, 6):\n    print(i)"
                    }
                ]
            }
        ]
    
    def _load_achievements(self) -> List[Dict[str, Any]]:
        """Load achievement data."""
        return [
            {
                "id": "first_steps",
                "name": "🎯 First Steps",
                "description": "Complete your first lesson",
                "condition": "complete_lesson",
                "requirement": 1
            },
            {
                "id": "quiz_master",
                "name": "🧠 Quiz Master",
                "description": "Score 100% on any test",
                "condition": "perfect_score",
                "requirement": 1
            },
            {
                "id": "dedicated_learner",
                "name": "📚 Dedicated Learner",
                "description": "Complete 5 lessons",
                "condition": "complete_lessons",
                "requirement": 5
            },
            {
                "id": "streak_starter",
                "name": "🔥 Streak Starter",
                "description": "Maintain a 3-day learning streak",
                "condition": "streak",
                "requirement": 3
            },
            {
                "id": "streak_master",
                "name": "🌟 Streak Master",
                "description": "Maintain a 7-day learning streak",
                "condition": "streak",
                "requirement": 7
            },
            {
                "id": "level_up",
                "name": "⬆️ Level Up",
                "description": "Reach level 5",
                "condition": "level",
                "requirement": 5
            },
            {
                "id": "python_explorer",
                "name": "🐍 Python Explorer",
                "description": "Complete lessons from 3 different topics",
                "condition": "diverse_learning",
                "requirement": 3
            },
            {
                "id": "test_taker",
                "name": "📝 Test Taker",
                "description": "Complete 3 tests",
                "condition": "complete_tests",
                "requirement": 3
            }
        ]
    
    def start_learning_session(self, player: Player):
        """Start a learning session with level selection."""
        available_levels = self._get_available_levels(player)
        
        while True:
            choice = self.ui.show_level_menu(available_levels)
            
            if choice == "0":
                break
            
            try:
                level_index = int(choice) - 1
                if 0 <= level_index < len(available_levels):
                    lesson = available_levels[level_index]
                    if not lesson.get('locked', True):
                        self._play_lesson(player, lesson)
                    else:
                        print(f"🔒 This lesson is locked. Reach level {lesson['level_requirement']} to unlock it.")
                        input("Press Enter to continue...")
                else:
                    print("❌ Invalid choice. Please try again.")
            except ValueError:
                print("❌ Please enter a valid number.")
    
    def _get_available_levels(self, player: Player) -> List[Dict[str, Any]]:
        """Get list of available levels based on player progress."""
        available_levels = []
        
        for lesson in self.lessons:
            level_info = {
                'id': lesson['id'],
                'title': lesson['title'],
                'topic': lesson['topic'],
                'difficulty': lesson['difficulty'],
                'description': lesson['content'][:100] + "...",
                'level_requirement': lesson['level_requirement'],
                'locked': player.level < lesson['level_requirement'],
                'completed': lesson['id'] in player.completed_lessons
            }
            available_levels.append(level_info)
        
        return available_levels
    
    def _play_lesson(self, player: Player, lesson_info: Dict[str, Any]):
        """Play a specific lesson."""
        lesson = next((l for l in self.lessons if l['id'] == lesson_info['id']), None)
        if not lesson:
            print("❌ Lesson not found.")
            return
        
        # Show lesson content
        self.ui.show_lesson_content(lesson)
        
        # Ask if player wants to continue to quiz
        continue_choice = input("\nReady for the lesson quiz? (y/n): ").lower()
        if continue_choice != 'y':
            return
        
        # Take lesson quiz
        score, total = self._take_quiz(lesson['quiz'])
        
        # Calculate rewards
        xp_earned = 25 + (score * 5)  # Base XP + bonus for correct answers
        coins_earned = xp_earned // 10
        
        # Update player progress
        lesson_completed = player.complete_lesson(lesson['id'])
        leveled_up = player.add_experience(xp_earned)
        
        # Show results
        self.ui.show_quiz_result(score, total, [])
        
        if lesson_completed:
            self.ui.show_level_completed(lesson['title'], xp_earned, coins_earned)
            
            # Check for achievements
            self._check_achievements(player)
        
        if leveled_up:
            self.ui.show_level_up(player.level)
    
    def _take_quiz(self, questions: List[Dict[str, Any]]) -> tuple:
        """Take a quiz and return score and total questions."""
        score = 0
        total = len(questions)
        
        for i, question in enumerate(questions, 1):
            answer = self.ui.show_quiz_question(question, i, total)
            
            if question['type'] == 'multiple_choice':
                try:
                    answer_index = int(answer) - 1
                    if 0 <= answer_index < len(question['options']):
                        if answer_index == question['correct']:
                            score += 1
                            print(f"✅ Correct! {question['explanation']}")
                        else:
                            print(f"❌ Wrong. {question['explanation']}")
                    else:
                        print("❌ Invalid choice.")
                except ValueError:
                    print("❌ Please enter a number.")
            
            elif question['type'] == 'code':
                # Simple code evaluation (in real implementation, use safer methods)
                if self._evaluate_code_answer(answer, question):
                    score += 1
                    print("✅ Great code!")
                else:
                    print("❌ Try again. Check the expected concepts.")
            
            print("-" * 50)
        
        return score, total
    
    def _evaluate_code_answer(self, code: str, question: Dict[str, Any]) -> bool:
        """Evaluate a code answer (simplified version)."""
        expected_concepts = question.get('expected_concepts', [])
        code_lower = code.lower()
        
        # Check if code contains expected concepts
        for concept in expected_concepts:
            if concept not in code_lower:
                return False
        
        # Basic syntax check
        try:
            compile(code, '<string>', 'exec')
            return True
        except:
            return False
    
    def take_test(self, player: Player):
        """Take a comprehensive test."""
        available_tests = [test for test in self.tests if player.level >= test['level_requirement']]
        
        if not available_tests:
            print("🔒 No tests available at your current level.")
            input("Press Enter to continue...")
            return
        
        print(f"\n{self.ui.colors['header']}📝 AVAILABLE TESTS{self.ui.colors['end']}")
        print("-" * 50)
        
        for i, test in enumerate(available_tests, 1):
            print(f"{i}. {test['title']}")
            print(f"   {test['description']}")
            print(f"   Required Level: {test['level_requirement']}")
            print()
        
        print("0. ⬅️ Back to Main Menu")
        print("-" * 50)
        
        choice = input("Choose a test (0 to go back): ").strip()
        
        if choice == "0":
            return
        
        try:
            test_index = int(choice) - 1
            if 0 <= test_index < len(available_tests):
                test = available_tests[test_index]
                self._take_full_test(player, test)
            else:
                print("❌ Invalid choice.")
        except ValueError:
            print("❌ Please enter a valid number.")
    
    def _take_full_test(self, player: Player, test: Dict[str, Any]):
        """Take a full test."""
        print(f"\n{self.ui.colors['header']}📝 {test['title']}{self.ui.colors['end']}")
        print("=" * 60)
        print(f"Description: {test['description']}")
        print(f"Questions: {len(test['questions'])}")
        print("=" * 60)
        
        ready = input("Are you ready to start the test? (y/n): ").lower()
        if ready != 'y':
            return
        
        score, total = self._take_quiz(test['questions'])
        
        # Record test score
        player.record_test_score(test['title'], score, total)
        
        # Show detailed results
        percentage = (score / total) * 100
        feedback = []
        
        if percentage >= 90:
            feedback.append("Excellent work! You have mastered this topic.")
        elif percentage >= 75:
            feedback.append("Good job! You understand most concepts well.")
        elif percentage >= 60:
            feedback.append("Not bad! Review the topics you missed.")
        else:
            feedback.append("Keep practicing! Consider reviewing the lessons.")
        
        self.ui.show_quiz_result(score, total, feedback)
        
        # Check for achievements
        self._check_achievements(player)
        
        input(f"\n{self.ui.colors['blue']}Press Enter to continue...{self.ui.colors['end']}")
    
    def _check_achievements(self, player: Player):
        """Check and award achievements."""
        for achievement in self.achievements:
            if achievement['name'] in player.achievements:
                continue
            
            awarded = False
            
            if achievement['condition'] == 'complete_lesson':
                if len(player.completed_lessons) >= achievement['requirement']:
                    awarded = True
            
            elif achievement['condition'] == 'perfect_score':
                for test_score in player.test_scores.values():
                    if test_score['percentage'] == 100:
                        awarded = True
                        break
            
            elif achievement['condition'] == 'complete_lessons':
                if len(player.completed_lessons) >= achievement['requirement']:
                    awarded = True
            
            elif achievement['condition'] == 'streak':
                if player.streak >= achievement['requirement']:
                    awarded = True
            
            elif achievement['condition'] == 'level':
                if player.level >= achievement['requirement']:
                    awarded = True
            
            elif achievement['condition'] == 'diverse_learning':
                topics = set()
                for lesson_id in player.completed_lessons:
                    lesson = next((l for l in self.lessons if l['id'] == lesson_id), None)
                    if lesson:
                        topics.add(lesson['topic'])
                if len(topics) >= achievement['requirement']:
                    awarded = True
            
            elif achievement['condition'] == 'complete_tests':
                if len(player.test_scores) >= achievement['requirement']:
                    awarded = True
            
            if awarded:
                player.add_achievement(achievement['name'])
                self.ui.show_achievement_unlocked(achievement['name'])
