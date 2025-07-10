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
    """Advanced game engine that manages lessons, tests, and progression with enhanced features."""
    
    def __init__(self):
        self.ui = UIManager()
        self.lessons = self._load_lessons()
        self.tests = self._load_tests()
        self.achievements = self._load_achievements()
        self.challenges = self._load_challenges()
        self.skill_tree = self._load_skill_tree()
        self.difficulty_multipliers = {
            "Beginner": 1.0,
            "Intermediate": 1.2,
            "Advanced": 1.5,
            "Expert": 2.0,
            "Master": 2.5
        }
    
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
    \"\"\"Optional docstring\"""
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
    \"\"\"Greet someone by name\"""
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
    \"\"\"Calculate rectangle area\"""
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
    \"\"\"Sum any number of arguments\"""
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
            },
            {
                "id": "python_advanced_1",
                "title": "Advanced Python - Decorators and Context Managers",
                "topic": "Advanced Python",
                "difficulty": "Advanced",
                "duration": "45 minutes",
                "level_requirement": 8,
                "content": """
DECORATORS:
Decorators are a way to modify or enhance functions without changing their code directly.

WHAT ARE DECORATORS:
- Functions that take another function as argument
- Return a modified version of the function
- Use @ syntax for clean application
- Common for logging, timing, authentication

BASIC DECORATOR PATTERN:
def decorator(func):
    def wrapper(*args, **kwargs):
        # Do something before
        result = func(*args, **kwargs)
        # Do something after
        return result
    return wrapper

CONTEXT MANAGERS:
Context managers ensure proper resource management using 'with' statements.

BUILT-IN CONTEXT MANAGERS:
- File operations: with open()
- Thread locks: with threading.Lock()
- Database connections

CREATING CONTEXT MANAGERS:
1. Using contextlib.contextmanager decorator
2. Implementing __enter__ and __exit__ methods

BENEFITS:
- Automatic resource cleanup
- Exception handling
- Cleaner, more readable code
                """,
                "code_example": """# Simple decorator
def timer(func):
    import time
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper

@timer
def slow_function():
    import time
    time.sleep(1)
    return "Done!"

# Usage
result = slow_function()

# Context manager example
from contextlib import contextmanager

@contextmanager
def timer_context():
    import time
    start = time.time()
    try:
        yield
    finally:
        end = time.time()
        print(f"Block took {end - start:.4f} seconds")

# Usage
with timer_context():
    # Some time-consuming operation
    sum(range(1000000))

# File context manager
with open('data.txt', 'w') as file:
    file.write('Hello, World!')
# File is automatically closed
                """,
                "tips": [
                    "Use functools.wraps to preserve function metadata in decorators",
                    "Context managers are perfect for resource management",
                    "The 'with' statement guarantees cleanup even if exceptions occur",
                    "You can create reusable decorators for common functionality"
                ],
                "quiz": [
                    {
                        "question": "What does the @ symbol do in Python?",
                        "type": "multiple_choice",
                        "options": ["Create a comment", "Apply a decorator", "Define a variable", "Import a module"],
                        "correct": 1,
                        "explanation": "The @ symbol is syntactic sugar for applying decorators to functions."
                    },
                    {
                        "question": "What methods must a context manager implement?",
                        "type": "multiple_choice",
                        "options": ["__init__ and __del__", "__enter__ and __exit__", "__start__ and __stop__", "__open__ and __close__"],
                        "correct": 1,
                        "explanation": "Context managers must implement __enter__ and __exit__ methods."
                    }
                ]
            },
            {
                "id": "python_advanced_2",
                "title": "Advanced Python - Generators and Iterators",
                "topic": "Advanced Python",
                "difficulty": "Advanced",
                "duration": "50 minutes",
                "level_requirement": 9,
                "content": """
GENERATORS:
Generators are special functions that return an iterator object.

WHY GENERATORS:
- Memory efficient (lazy evaluation)
- Can represent infinite sequences
- Pause and resume execution
- Clean syntax with yield keyword

GENERATOR FUNCTIONS:
- Use 'yield' instead of 'return'
- Can yield multiple values
- Maintain state between calls
- Automatically implement iterator protocol

GENERATOR EXPRESSIONS:
- Similar to list comprehensions
- Use () instead of []
- Memory efficient for large datasets

ITERATORS:
Objects that implement the iterator protocol (__iter__ and __next__).

ITERATOR PROTOCOL:
- __iter__(): Returns the iterator object
- __next__(): Returns the next value
- Raises StopIteration when done

BUILT-IN ITERATORS:
- range(), enumerate(), zip()
- map(), filter(), sorted()
- File objects, strings, lists

ADVANCED TECHNIQUES:
- Generator pipelines
- Coroutines with send()
- yield from for delegation
                """,
                "code_example": """# Simple generator function
def countdown(n):
    while n > 0:
        yield n
        n -= 1

# Using the generator
for num in countdown(5):
    print(num)

# Generator expression
squares = (x**2 for x in range(10))
print(list(squares))

# Fibonacci generator (infinite sequence)
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# Get first 10 Fibonacci numbers
fib = fibonacci()
first_10 = [next(fib) for _ in range(10)]
print(first_10)

# Custom iterator class
class Counter:
    def __init__(self, max_count):
        self.max_count = max_count
        self.count = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.count < self.max_count:
            self.count += 1
            return self.count
        raise StopIteration

# Usage
counter = Counter(3)
for num in counter:
    print(num)

# Generator pipeline
def read_numbers():
    for i in range(100):
        yield i

def square_numbers(numbers):
    for num in numbers:
        yield num ** 2

def filter_even(numbers):
    for num in numbers:
        if num % 2 == 0:
            yield num

# Chain generators
pipeline = filter_even(square_numbers(read_numbers()))
result = list(pipeline)[:10]
print(result)
                """,
                "tips": [
                    "Use generators for large datasets to save memory",
                    "Generator expressions are more memory-efficient than list comprehensions",
                    "Generators are consumed once - convert to list if you need multiple iterations",
                    "Use yield from to delegate to another generator"
                ],
                "quiz": [
                    {
                        "question": "What keyword is used to create a generator function?",
                        "type": "multiple_choice",
                        "options": ["return", "yield", "generate", "iterator"],
                        "correct": 1,
                        "explanation": "The 'yield' keyword is used to create generator functions."
                    },
                    {
                        "question": "What happens when a generator is exhausted?",
                        "type": "multiple_choice",
                        "options": ["It restarts", "It raises StopIteration", "It returns None", "It raises ValueError"],
                        "correct": 1,
                        "explanation": "Generators raise StopIteration when they have no more values to yield."
                    }
                ]
            },
            {
                "id": "python_advanced_3",
                "title": "Advanced Python - Metaclasses and Descriptors",
                "topic": "Advanced Python",
                "difficulty": "Expert",
                "duration": "60 minutes",
                "level_requirement": 12,
                "content": """
METACLASSES:
Metaclasses are classes whose instances are classes themselves.

UNDERSTANDING METACLASSES:
- Everything in Python is an object
- Classes are objects too
- Metaclasses create classes
- type is the default metaclass

CLASS CREATION PROCESS:
1. Python collects class name, base classes, and namespace
2. Python calls the metaclass to create the class
3. The metaclass returns the new class object

CUSTOM METACLASSES:
- Inherit from type
- Override __new__ or __init__
- Control class creation process
- Add attributes/methods automatically

DESCRIPTORS:
Objects that define how attribute access is handled.

DESCRIPTOR PROTOCOL:
- __get__(self, obj, type): Get attribute
- __set__(self, obj, value): Set attribute
- __delete__(self, obj): Delete attribute

TYPES OF DESCRIPTORS:
- Data descriptors: Have __get__ and __set__
- Non-data descriptors: Have only __get__
- property is a built-in descriptor

USE CASES:
- Validation and type checking
- Lazy evaluation
- Attribute access logging
- ORM field definitions
                """,
                "code_example": """# Simple metaclass
class SingletonMeta(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=SingletonMeta):
    def __init__(self):
        self.connection = "Connected"

# Both will be the same instance
db1 = Database()
db2 = Database()
print(db1 is db2)  # True

# Metaclass for attribute validation
class ValidatedMeta(type):
    def __new__(mcs, name, bases, namespace):
        # Add validation to all methods starting with 'set_'
        for key, value in namespace.items():
            if key.startswith('set_') and callable(value):
                namespace[key] = mcs.add_validation(value)
        return super().__new__(mcs, name, bases, namespace)
    
    @staticmethod
    def add_validation(func):
        def wrapper(self, value):
            if value is None:
                raise ValueError("Value cannot be None")
            return func(self, value)
        return wrapper

# Descriptor example
class ValidatedAttribute:
    def __init__(self, validator=None):
        self.validator = validator
        self.private_name = None
    
    def __set_name__(self, owner, name):
        self.private_name = f'_{name}'
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.private_name, None)
    
    def __set__(self, obj, value):
        if self.validator:
            self.validator(value)
        setattr(obj, self.private_name, value)

def positive_number(value):
    if not isinstance(value, (int, float)) or value <= 0:
        raise ValueError("Must be a positive number")

class Product:
    price = ValidatedAttribute(positive_number)
    
    def __init__(self, name, price):
        self.name = name
        self.price = price

# Usage
product = Product("Laptop", 999.99)
print(product.price)  # 999.99

try:
    product.price = -100  # Raises ValueError
except ValueError as e:
    print(f"Error: {e}")
                """,
                "tips": [
                    "Metaclasses are powerful but complex - use sparingly",
                    "Most problems can be solved without metaclasses",
                    "Descriptors are great for reusable attribute validation",
                    "Study how property() is implemented as a descriptor"
                ],
                "quiz": [
                    {
                        "question": "What is the default metaclass in Python?",
                        "type": "multiple_choice",
                        "options": ["object", "type", "class", "meta"],
                        "correct": 1,
                        "explanation": "'type' is the default metaclass that creates all classes in Python."
                    },
                    {
                        "question": "Which method in a descriptor handles attribute assignment?",
                        "type": "multiple_choice",
                        "options": ["__get__", "__set__", "__delete__", "__assign__"],
                        "correct": 1,
                        "explanation": "__set__ method handles attribute assignment in descriptors."
                    }
                ]
            },
            {
                "id": "python_concurrency_1",
                "title": "Concurrency - Threading and Multiprocessing",
                "topic": "Concurrency",
                "difficulty": "Advanced",
                "duration": "55 minutes",
                "level_requirement": 10,
                "content": """
CONCURRENCY VS PARALLELISM:
- Concurrency: Multiple tasks making progress (not necessarily simultaneously)
- Parallelism: Multiple tasks running simultaneously
- Python's GIL limits true parallelism for CPU-bound tasks

THREADING:
Run multiple threads within a single process.

WHEN TO USE THREADING:
- I/O-bound tasks (file operations, network requests)
- User interface responsiveness
- Background tasks

THREADING MODULES:
- threading: High-level interface
- concurrent.futures: Thread pools
- asyncio: Asynchronous programming

MULTIPROCESSING:
Run multiple processes for true parallelism.

WHEN TO USE MULTIPROCESSING:
- CPU-bound tasks
- Parallel computation
- Independent task processing

SYNCHRONIZATION:
- Locks: Prevent race conditions
- Semaphores: Control resource access
- Queues: Thread-safe communication
- Events: Coordinate thread execution

BEST PRACTICES:
- Avoid shared mutable state
- Use thread-safe data structures
- Handle exceptions properly
- Use context managers for locks
                """,
                "code_example": """import threading
import multiprocessing
import time
import concurrent.futures
from queue import Queue

# Basic threading example
def worker(name, duration):
    print(f"Worker {name} starting")
    time.sleep(duration)
    print(f"Worker {name} finished")

# Create and start threads
threads = []
for i in range(3):
    t = threading.Thread(target=worker, args=(f"Thread-{i}", 2))
    threads.append(t)
    t.start()

# Wait for all threads to complete
for t in threads:
    t.join()

# Thread with shared data and lock
shared_counter = 0
counter_lock = threading.Lock()

def increment_counter():
    global shared_counter
    for _ in range(100000):
        with counter_lock:
            shared_counter += 1

# ThreadPoolExecutor example
def cpu_bound_task(n):
    total = 0
    for i in range(n):
        total += i * i
    return total

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(cpu_bound_task, 1000) for _ in range(10)]
    results = [future.result() for future in futures]

# Multiprocessing example
def cpu_intensive_work(n):
    return sum(i * i for i in range(n))

if __name__ == "__main__":
    with multiprocessing.Pool(processes=4) as pool:
        results = pool.map(cpu_intensive_work, [100000, 200000, 300000])
        print(f"Results: {results}")

# Producer-Consumer with Queue
def producer(queue):
    for i in range(5):
        item = f"item-{i}"
        queue.put(item)
        print(f"Produced {item}")
        time.sleep(1)

def consumer(queue):
    while True:
        item = queue.get()
        if item is None:
            break
        print(f"Consumed {item}")
        queue.task_done()

# Create queue and threads
q = Queue()
producer_thread = threading.Thread(target=producer, args=(q,))
consumer_thread = threading.Thread(target=consumer, args=(q,))

producer_thread.start()
consumer_thread.start()

producer_thread.join()
q.put(None)  # Signal consumer to stop
consumer_thread.join()
                """,
                "tips": [
                    "Use threading for I/O-bound tasks, multiprocessing for CPU-bound tasks",
                    "Always use locks when multiple threads access shared data",
                    "Prefer thread pools over creating threads manually",
                    "Be careful with deadlocks - acquire locks in consistent order"
                ],
                "quiz": [
                    {
                        "question": "What is Python's GIL?",
                        "type": "multiple_choice",
                        "options": ["Global Import Lock", "Global Interpreter Lock", "General Interface Lock", "Garbage Instruction Lock"],
                        "correct": 1,
                        "explanation": "GIL (Global Interpreter Lock) prevents multiple threads from executing Python code simultaneously."
                    },
                    {
                        "question": "Which is better for CPU-intensive tasks?",
                        "type": "multiple_choice",
                        "options": ["Threading", "Multiprocessing", "Asyncio", "Single thread"],
                        "correct": 1,
                        "explanation": "Multiprocessing is better for CPU-intensive tasks as it bypasses the GIL limitation."
                    }
                ]
            },
            {
                "id": "python_async_1",
                "title": "Asynchronous Programming with Asyncio",
                "topic": "Async Programming",
                "difficulty": "Advanced",
                "duration": "50 minutes",
                "level_requirement": 11,
                "content": """
ASYNCHRONOUS PROGRAMMING:
Write concurrent code using async/await syntax.

WHY ASYNC PROGRAMMING:
- Handle many I/O operations efficiently
- Single-threaded concurrency
- Better resource utilization
- Scalable web applications

KEY CONCEPTS:
- Event loop: Core of async programming
- Coroutines: Async functions
- Tasks: Wrapped coroutines
- Futures: Objects representing eventual results

ASYNC/AWAIT SYNTAX:
- async def: Define coroutine function
- await: Wait for async operation
- Can only await inside async functions

ASYNCIO FEATURES:
- Event loop management
- Task scheduling
- Network programming
- File I/O operations
- Synchronization primitives

COMMON PATTERNS:
- Gathering multiple async operations
- Creating tasks for background work
- Using async context managers
- Async generators and comprehensions

PERFORMANCE BENEFITS:
- High concurrency with low overhead
- Efficient I/O handling
- Reduced memory usage vs threading
                """,
                "code_example": """import asyncio
import aiohttp
import time

# Basic async function
async def say_hello(name, delay):
    await asyncio.sleep(delay)
    print(f"Hello, {name}!")
    return f"Greeted {name}"

# Running async function
async def main():
    # Run sequentially
    await say_hello("Alice", 1)
    await say_hello("Bob", 1)
    
    # Run concurrently
    await asyncio.gather(
        say_hello("Charlie", 1),
        say_hello("Diana", 1)
    )

# Async HTTP requests
async def fetch_url(session, url):
    try:
        async with session.get(url) as response:
            return await response.text()
    except Exception as e:
        return f"Error: {e}"

async def fetch_multiple_urls():
    urls = [
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/2",
        "https://httpbin.org/delay/1"
    ]
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        return results

# Async generator
async def async_range(count):
    for i in range(count):
        await asyncio.sleep(0.1)
        yield i

async def process_async_data():
    async for value in async_range(5):
        print(f"Processing {value}")

# Producer-Consumer with asyncio
async def producer(queue):
    for i in range(5):
        await asyncio.sleep(1)
        await queue.put(f"item-{i}")
        print(f"Produced item-{i}")

async def consumer(queue):
    while True:
        item = await queue.get()
        print(f"Consumed {item}")
        queue.task_done()
        if "item-4" in item:  # Stop after last item
            break

async def producer_consumer_example():
    queue = asyncio.Queue()
    
    # Create tasks
    producer_task = asyncio.create_task(producer(queue))
    consumer_task = asyncio.create_task(consumer(queue))
    
    # Wait for producer to finish
    await producer_task
    # Wait for all items to be processed
    await queue.join()
    # Cancel consumer task
    consumer_task.cancel()

# Performance comparison
async def async_version():
    start_time = time.time()
    await asyncio.gather(*[say_hello(f"User{i}", 1) for i in range(5)])
    return time.time() - start_time

def sync_version():
    start_time = time.time()
    for i in range(5):
        time.sleep(1)
        print(f"Hello, User{i}!")
    return time.time() - start_time

# Run the examples
if __name__ == "__main__":
    # Run main async function
    asyncio.run(main())
    
    # Compare performance
    async_time = asyncio.run(async_version())
    sync_time = sync_version()
    
    print(f"Async time: {async_time:.2f}s")
    print(f"Sync time: {sync_time:.2f}s")
                """,
                "tips": [
                    "Use asyncio for I/O-bound tasks, not CPU-bound tasks",
                    "Always use await with async functions",
                    "Use asyncio.gather() to run multiple coroutines concurrently",
                    "Async context managers ensure proper resource cleanup"
                ],
                "quiz": [
                    {
                        "question": "What keyword is used to define an async function?",
                        "type": "multiple_choice",
                        "options": ["async def", "await def", "asyncio def", "concurrent def"],
                        "correct": 0,
                        "explanation": "'async def' is used to define asynchronous functions (coroutines)."
                    },
                    {
                        "question": "Which function runs multiple coroutines concurrently?",
                        "type": "multiple_choice",
                        "options": ["asyncio.run()", "asyncio.gather()", "asyncio.wait()", "asyncio.create_task()"],
                        "correct": 1,
                        "explanation": "asyncio.gather() runs multiple coroutines concurrently and collects their results."
                    }
                ]
            }
        ]
    
    def _load_challenges(self) -> List[Dict[str, Any]]:
        """Load coding challenges for advanced practice."""
        return [
            {
                "id": "challenge_decorator",
                "title": "Build a Caching Decorator",
                "difficulty": "Advanced",
                "description": "Create a decorator that caches function results",
                "requirements": [
                    "Implement memoization",
                    "Handle different argument types",
                    "Add cache size limit",
                    "Provide cache statistics"
                ],
                "skeleton_code": """def cache(max_size=128):
    # Your implementation here
    pass

@cache(max_size=100)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)""",
                "test_cases": [
                    "fibonacci(10) should return 55",
                    "fibonacci(20) should return 6765",
                    "Cache should store results",
                    "Cache should respect max_size"
                ],
                "points": 150
            },
            {
                "id": "challenge_async_web_scraper",
                "title": "Async Web Scraper",
                "difficulty": "Expert",
                "description": "Build an asynchronous web scraper with rate limiting",
                "requirements": [
                    "Use aiohttp for requests",
                    "Implement rate limiting",
                    "Handle errors gracefully",
                    "Parse HTML content",
                    "Save results to file"
                ],
                "skeleton_code": """import asyncio
import aiohttp
from aiohttp import ClientSession

class AsyncWebScraper:
    def __init__(self, rate_limit=1):
        # Your implementation here
        pass
    
    async def scrape_urls(self, urls):
        # Your implementation here
        pass""",
                "test_cases": [
                    "Should handle multiple URLs",
                    "Should respect rate limiting",
                    "Should handle HTTP errors",
                    "Should parse HTML content"
                ],
                "points": 200
            },
            {
                "id": "challenge_metaclass_orm",
                "title": "Simple ORM with Metaclasses",
                "difficulty": "Expert",
                "description": "Create a simple ORM using metaclasses",
                "requirements": [
                    "Define model classes with metaclass",
                    "Implement field validation",
                    "Add query methods",
                    "Handle relationships"
                ],
                "skeleton_code": """class Field:
    def __init__(self, field_type, required=True):
        # Your implementation here
        pass

class ModelMeta(type):
    # Your implementation here
    pass

class Model(metaclass=ModelMeta):
    # Your implementation here
    pass""",
                "test_cases": [
                    "Should create model instances",
                    "Should validate field types",
                    "Should support queries",
                    "Should handle relationships"
                ],
                "points": 250
            }
        ]
    
    def _load_achievements(self) -> List[Dict[str, Any]]:
        """Load comprehensive achievement data including advanced categories."""
        return [
            # Beginner Achievements
            {
                "id": "first_steps",
                "name": "🎯 First Steps",
                "description": "Complete your first lesson",
                "condition": "complete_lesson",
                "requirement": 1,
                "category": "Beginner",
                "points": 10
            },
            {
                "id": "quiz_master",
                "name": "🧠 Quiz Master",
                "description": "Score 100% on any test",
                "condition": "perfect_score",
                "requirement": 1,
                "category": "Performance",
                "points": 25
            },
            {
                "id": "dedicated_learner",
                "name": "📚 Dedicated Learner",
                "description": "Complete 5 lessons",
                "condition": "complete_lessons",
                "requirement": 5,
                "category": "Progress",
                "points": 50
            },
            
            # Streak Achievements
            {
                "id": "streak_starter",
                "name": "🔥 Streak Starter",
                "description": "Maintain a 3-day learning streak",
                "condition": "streak",
                "requirement": 3,
                "category": "Consistency",
                "points": 30
            },
            {
                "id": "streak_master",
                "name": "🌟 Streak Master",
                "description": "Maintain a 7-day learning streak",
                "condition": "streak",
                "requirement": 7,
                "category": "Consistency",
                "points": 75
            },
            {
                "id": "streak_legend",
                "name": "⚡ Streak Legend",
                "description": "Maintain a 30-day learning streak",
                "condition": "streak",
                "requirement": 30,
                "category": "Consistency",
                "points": 200
            },
            
            # Level Achievements
            {
                "id": "level_5",
                "name": "⬆️ Rising Star",
                "description": "Reach player level 5",
                "condition": "level",
                "requirement": 5,
                "category": "Progression",
                "points": 40
            },
            {
                "id": "level_10",
                "name": "🌟 Advanced Learner",
                "description": "Reach player level 10",
                "condition": "level",
                "requirement": 10,
                "category": "Progression",
                "points": 100
            },
            {
                "id": "level_20",
                "name": "🏆 Expert Programmer",
                "description": "Reach player level 20",
                "condition": "level",
                "requirement": 20,
                "category": "Progression",
                "points": 250
            },
            
            # Advanced Achievements
            {
                "id": "challenge_conqueror",
                "name": "⚔️ Challenge Conqueror",
                "description": "Complete 3 coding challenges",
                "condition": "complete_challenges",
                "requirement": 3,
                "category": "Advanced",
                "points": 150
            },
            {
                "id": "decorator_master",
                "name": "🎭 Decorator Master",
                "description": "Complete advanced decorator lessons",
                "condition": "skill_mastery",
                "requirement": "decorators",
                "category": "Advanced",
                "points": 120
            },
            {
                "id": "async_wizard",
                "name": "🔮 Async Wizard",
                "description": "Master asynchronous programming",
                "condition": "skill_mastery",
                "requirement": "async_programming",
                "category": "Advanced",
                "points": 150
            },
            {
                "id": "metaclass_sage",
                "name": "🧙‍♂️ Metaclass Sage",
                "description": "Understand metaclasses and descriptors",
                "condition": "skill_mastery",
                "requirement": "metaclasses",
                "category": "Expert",
                "points": 200
            },
            
            # Ultimate Achievements
            {
                "id": "python_master",
                "name": "🐍👑 Python Master",
                "description": "Complete all 100 levels",
                "condition": "complete_all_levels",
                "requirement": 100,
                "category": "Ultimate",
                "points": 1000
            }
        ]
    
    def calculate_dynamic_rewards(self, player, level_data: Dict[str, Any], performance: Dict[str, Any]) -> Dict[str, int]:
        """Calculate dynamic rewards based on performance and difficulty."""
        base_xp = level_data.get('rewards', {}).get('xp', 50)
        base_coins = level_data.get('rewards', {}).get('coins', 20)
        
        # Performance multiplier
        score_percentage = performance.get('score_percentage', 0)
        performance_multiplier = 1.0 + (score_percentage - 50) / 100  # Bonus for >50%, penalty for <50%
        
        # Difficulty multiplier
        difficulty = level_data.get('difficulty', 'Beginner')
        difficulty_multiplier = self.difficulty_multipliers.get(difficulty, 1.0)
        
        # Streak bonus
        streak_multiplier = 1.0 + min(player.streak * 0.05, 0.5)  # Max 50% bonus
        
        # Level difference bonus (for completing harder content)
        level_diff_bonus = max(0, level_data.get('level_requirement', 1) - player.level) * 0.1
        
        # Calculate final rewards
        total_multiplier = performance_multiplier * difficulty_multiplier * streak_multiplier * (1 + level_diff_bonus)
        
        return {
            'xp': int(base_xp * total_multiplier),
            'coins': int(base_coins * total_multiplier),
            'stars': self._calculate_stars(score_percentage)
        }
    
    def _calculate_stars(self, score_percentage: float) -> int:
        """Calculate stars based on score percentage."""
        if score_percentage >= 95:
            return 3
        elif score_percentage >= 80:
            return 2
        elif score_percentage >= 60:
            return 1
        else:
            return 0
    
    def create_adaptive_challenge(self, player, skill_area: str) -> Dict[str, Any]:
        """Create personalized challenges based on player performance."""
        challenges = {
            'decorators': {
                'title': 'Master Decorators',
                'description': 'Create a custom decorator system',
                'difficulty_adjustment': player.get_skill_level('decorators')
            },
            'async': {
                'title': 'Async Programming Challenge',
                'description': 'Build an async web scraper',
                'difficulty_adjustment': player.get_skill_level('async')
            },
            'metaclasses': {
                'title': 'Metaclass Magic',
                'description': 'Design a metaclass-based ORM',
                'difficulty_adjustment': player.get_skill_level('metaclasses')
            }
        }
        
        base_challenge = challenges.get(skill_area, challenges['decorators'])
        
        # Adjust difficulty based on player skill
        skill_level = player.get_skill_level(skill_area) if hasattr(player, 'get_skill_level') else 1
        adjusted_challenge = base_challenge.copy()
        adjusted_challenge['complexity'] = min(5, max(1, skill_level))
        adjusted_challenge['time_limit'] = 30 + (skill_level * 10)  # minutes
        
        return adjusted_challenge
    
    def evaluate_advanced_code(self, code: str, challenge_data: Dict[str, Any]) -> Dict[str, Any]:
        """Advanced code evaluation with multiple criteria."""
        results = {
            'syntax_correct': False,
            'functionality_score': 0,
            'style_score': 0,
            'efficiency_score': 0,
            'total_score': 0,
            'feedback': []
        }
        
        try:
            # Basic syntax check
            compile(code, '<string>', 'exec')
            results['syntax_correct'] = True
            results['feedback'].append("✅ Code syntax is correct")
        except SyntaxError as e:
            results['feedback'].append(f"❌ Syntax error: {e}")
            return results
        
        # Check for required concepts
        required_concepts = challenge_data.get('required_concepts', [])
        found_concepts = []
        
        for concept in required_concepts:
            if concept.lower() in code.lower():
                found_concepts.append(concept)
        
        functionality_score = (len(found_concepts) / len(required_concepts)) * 100 if required_concepts else 100
        results['functionality_score'] = functionality_score
        
        # Style checking (simplified)
        style_issues = []
        if 'def ' in code and '"""' not in code and "'''" not in code:
            style_issues.append("Consider adding docstrings to functions")
        
        if len([line for line in code.split('\n') if len(line) > 100]) > 0:
            style_issues.append("Some lines are too long (>100 characters)")
        
        style_score = max(0, 100 - len(style_issues) * 20)
        results['style_score'] = style_score
        results['feedback'].extend([f"⚠️  {issue}" for issue in style_issues])
        
        # Efficiency score (placeholder - would need more sophisticated analysis)
        efficiency_score = 80  # Default good score
        if 'for' in code and 'in range(len(' in code:
            efficiency_score -= 10
            results['feedback'].append("💡 Consider using direct iteration instead of range(len())")
        
        results['efficiency_score'] = efficiency_score
        
        # Calculate total score
        weights = {'functionality': 0.5, 'style': 0.2, 'efficiency': 0.3}
        total_score = (
            functionality_score * weights['functionality'] +
            style_score * weights['style'] +
            efficiency_score * weights['efficiency']
        )
        results['total_score'] = total_score
        
        return results
    
    def get_next_recommended_lesson(self, player) -> Optional[Dict[str, Any]]:
        """Get AI-powered lesson recommendations based on player progress."""
        completed_lessons = set(player.completed_lessons) if hasattr(player, 'completed_lessons') else set()
        
        # Analyze player's weak areas
        weak_areas = self._analyze_weak_areas(player)
        
        # Find lessons that address weak areas
        for lesson in self.lessons:
            if lesson['id'] not in completed_lessons:
                if player.level >= lesson['level_requirement']:
                    # Check if lesson addresses weak areas
                    if any(weak_area in lesson['topic'].lower() for weak_area in weak_areas):
                        return lesson
        
        # Fallback to next available lesson
        for lesson in self.lessons:
            if lesson['id'] not in completed_lessons and player.level >= lesson['level_requirement']:
                return lesson
        
        return None
    
    def _analyze_weak_areas(self, player) -> List[str]:
        """Analyze player performance to identify weak areas."""
        weak_areas = []
        
        # Check test scores for patterns
        if hasattr(player, 'test_scores'):
            for test_name, score_data in player.test_scores.items():
                if score_data.get('percentage', 100) < 70:
                    # Extract topic from test name
                    for topic in ['functions', 'loops', 'classes', 'async', 'decorators']:
                        if topic in test_name.lower():
                            weak_areas.append(topic)
        
        return weak_areas[:3]  # Return top 3 weak areas
    
    def generate_learning_path(self, player, target_skill: str) -> List[Dict[str, Any]]:
        """Generate a personalized learning path to master a specific skill."""
        skill_tree = self.skill_tree['skills'].get(target_skill, {})
        prerequisites = skill_tree.get('prerequisites', [])
        
        learning_path = []
        
        # Add prerequisite lessons
        for prereq in prerequisites:
            prereq_lessons = [lesson for lesson in self.lessons if prereq.lower() in lesson['topic'].lower()]
            learning_path.extend(prereq_lessons[:2])  # Add first 2 lessons from each prereq
        
        # Add target skill lessons
        target_lessons = [lesson for lesson in self.lessons if target_skill.lower() in lesson['topic'].lower()]
        learning_path.extend(target_lessons)
        
        # Remove duplicates and sort by level requirement
        seen = set()
        unique_path = []
        for lesson in learning_path:
            if lesson['id'] not in seen:
                seen.add(lesson['id'])
                unique_path.append(lesson)
        
        return sorted(unique_path, key=lambda x: x['level_requirement'])
    
    def create_personalized_test(self, player, topic: str) -> Optional[Dict[str, Any]]:
        """Create a personalized test based on player's learning history."""
        base_test = next((test for test in self.tests if topic.lower() in test['title'].lower()), None)
        
        if not base_test:
            return None
        
        # Customize test based on player performance
        personalized_test = base_test.copy()
        
        # Adjust difficulty based on player level and past performance
        if hasattr(player, 'get_average_score'):
            avg_score = player.get_average_score(topic)
            if avg_score > 85:
                # Add more challenging questions
                personalized_test['title'] += " - Advanced"
                personalized_test['difficulty'] = "Advanced"
            elif avg_score < 60:
                # Add more basic questions
                personalized_test['title'] += " - Review"
                personalized_test['difficulty'] = "Review"
        
        return personalized_test
    
    def _load_tests(self) -> List[Dict[str, Any]]:
        """Load comprehensive tests including advanced topics."""
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
            },
            {
                "id": "functions_test",
                "title": "Functions Mastery Test",
                "description": "Advanced test on function creation and usage",
                "level_requirement": 5,
                "questions": [
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
                    },
                    {
                        "question": "Write a function that takes two numbers and returns their sum.",
                        "type": "code",
                        "expected_concepts": ["def", "return", "parameters"],
                        "sample_answer": "def add_numbers(a, b):\n    return a + b"
                    }
                ]
            },
            {
                "id": "advanced_python_test",
                "title": "Advanced Python Features Test",
                "description": "Test your knowledge of decorators, generators, and context managers",
                "level_requirement": 8,
                "questions": [
                    {
                        "question": "What is the purpose of the @property decorator?",
                        "type": "multiple_choice",
                        "options": [
                            "To create class methods",
                            "To create getter/setter methods",
                            "To create static methods",
                            "To create private methods"
                        ],
                        "correct": 1,
                        "explanation": "@property allows you to define methods that can be accessed like attributes."
                    },
                    {
                        "question": "Which statement best describes generators?",
                        "type": "multiple_choice",
                        "options": [
                            "They store all values in memory",
                            "They compute values on-demand",
                            "They can only be used once",
                            "Both B and C are correct"
                        ],
                        "correct": 3,
                        "explanation": "Generators compute values lazily and can only be iterated once."
                    },
                    {
                        "question": "Write a context manager that prints 'Entering' and 'Exiting'.",
                        "type": "code",
                        "expected_concepts": ["contextmanager", "yield", "try", "finally"],
                        "sample_answer": """from contextlib import contextmanager

@contextmanager
def my_context():
    print('Entering')
    try:
        yield
    finally:
        print('Exiting')"""
                    }
                ]
            },
            {
                "id": "concurrency_test",
                "title": "Concurrency and Async Programming Test",
                "description": "Test your understanding of threading, multiprocessing, and asyncio",
                "level_requirement": 10,
                "questions": [
                    {
                        "question": "What is the main limitation of Python's threading?",
                        "type": "multiple_choice",
                        "options": [
                            "High memory usage",
                            "Global Interpreter Lock (GIL)",
                            "Poor performance",
                            "Complex syntax"
                        ],
                        "correct": 1,
                        "explanation": "The GIL prevents true parallelism in CPU-bound threaded applications."
                    },
                    {
                        "question": "When should you use asyncio over threading?",
                        "type": "multiple_choice",
                        "options": [
                            "For CPU-bound tasks",
                            "For I/O-bound tasks with many operations",
                            "For simple sequential tasks",
                            "For mathematical calculations"
                        ],
                        "correct": 1,
                        "explanation": "Asyncio excels at handling many I/O-bound operations concurrently."
                    },
                    {
                        "question": "Write an async function that fetches data from multiple URLs concurrently.",
                        "type": "code",
                        "expected_concepts": ["async", "await", "aiohttp", "gather"],
                        "sample_answer": """async def fetch_multiple(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [session.get(url) for url in urls]
        responses = await asyncio.gather(*tasks)
        return responses"""
                    }
                ]
            },
            {
                "id": "metaclass_test",
                "title": "Metaclasses and Advanced OOP Test",
                "description": "Expert-level test on metaclasses, descriptors, and advanced object-oriented programming",
                "level_requirement": 12,
                "questions": [
                    {
                        "question": "What is the default metaclass in Python?",
                        "type": "multiple_choice",
                        "options": ["object", "type", "class", "meta"],
                        "correct": 1,
                        "explanation": "'type' is the default metaclass that creates all classes in Python."
                    },
                    {
                        "question": "Which method in a descriptor handles attribute assignment?",
                        "type": "multiple_choice",
                        "options": ["__get__", "__set__", "__delete__", "__assign__"],
                        "correct": 1,
                        "explanation": "__set__ method handles attribute assignment in descriptors."
                    },
                    {
                        "question": "Create a simple metaclass that adds a class attribute 'created_by' with value 'metaclass'.",
                        "type": "code",
                        "expected_concepts": ["metaclass", "__new__", "type"],
                        "sample_answer": """class MyMeta(type):
    def __new__(mcs, name, bases, namespace):
        namespace['created_by'] = 'metaclass'
        return super().__new__(mcs, name, bases, namespace)"""
                    }
                ]
            }
        ]
    
    def _load_skill_tree(self) -> Dict[str, Any]:
        """Load skill tree configuration for progression tracking."""
        return {
            "nodes": {
                "python_basics": {
                    "id": "python_basics",
                    "name": "Python Basics",
                    "description": "Variables, data types, and basic operations",
                    "prerequisites": [],
                    "levels_required": 1,
                    "skills": ["variables", "data_types", "basic_operations"]
                },
                "control_flow": {
                    "id": "control_flow",
                    "name": "Control Flow",
                    "description": "Conditionals, loops, and logic",
                    "prerequisites": ["python_basics"],
                    "levels_required": 5,
                    "skills": ["if_statements", "loops", "boolean_logic"]
                },
                "functions": {
                    "id": "functions",
                    "name": "Functions",
                    "description": "Creating and using functions",
                    "prerequisites": ["python_basics", "control_flow"],
                    "levels_required": 10,
                    "skills": ["function_definition", "parameters", "return_values"]
                },
                "data_structures": {
                    "id": "data_structures",
                    "name": "Data Structures",
                    "description": "Lists, dictionaries, and sets",
                    "prerequisites": ["functions"],
                    "levels_required": 15,
                    "skills": ["lists", "dictionaries", "sets", "tuples"]
                },
                "oop": {
                    "id": "oop",
                    "name": "Object-Oriented Programming",
                    "description": "Classes, objects, and inheritance",
                    "prerequisites": ["data_structures"],
                    "levels_required": 25,
                    "skills": ["classes", "objects", "inheritance", "polymorphism"]
                },
                "advanced_topics": {
                    "id": "advanced_topics",
                    "name": "Advanced Topics",
                    "description": "Decorators, generators, and metaclasses",
                    "prerequisites": ["oop"],
                    "levels_required": 40,
                    "skills": ["decorators", "generators", "context_managers", "metaclasses"]
                }
            },
            "progression_paths": [
                ["python_basics", "control_flow", "functions", "data_structures", "oop", "advanced_topics"]
            ],
            "skill_points": {
                "variables": {"cost": 1, "description": "Master variable assignment and naming"},
                "data_types": {"cost": 1, "description": "Understand int, float, str, bool"},
                "if_statements": {"cost": 2, "description": "Control program flow with conditionals"},
                "loops": {"cost": 2, "description": "Master for and while loops"},
                "function_definition": {"cost": 3, "description": "Create reusable functions"},
                "lists": {"cost": 2, "description": "Work with ordered collections"},
                "dictionaries": {"cost": 3, "description": "Use key-value data structures"},
                "classes": {"cost": 4, "description": "Create custom object types"},
                "inheritance": {"cost": 4, "description": "Extend classes with inheritance"},
                "decorators": {"cost": 5, "description": "Modify function behavior"},
                "generators": {"cost": 5, "description": "Create memory-efficient iterators"}
            }
        }
