"""
Level Loader Module
Manages sequential loading of levels and level progression logic
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import json
import random


class LevelLoader:
    """Handles level loading, progression, and availability logic."""
    
    def __init__(self):
        self.progression_rules = self._define_progression_rules()
        self.levels = self._load_all_levels()
        self.level_cache = {}
    
    def _define_progression_rules(self) -> Dict[str, Any]:
        """Define rules for level progression."""
        return {
            'sequential_unlock': True,  # Levels unlock sequentially
            'skip_allowed': False,      # Can't skip levels normally
            'test_frequency': 10,       # Test level every 10 levels
            'challenge_frequency': 25,  # Challenge level every 25 levels
            'minimum_score': 70,        # Minimum passing score
            'test_minimum_score': 80,   # Higher minimum for tests
            'retry_allowed': True,      # Allow retrying failed levels
            'max_retries': 3           # Maximum retries per level
        }
    
    def _load_all_levels(self) -> List[Dict[str, Any]]:
        """Load all level definitions."""
        levels = []
        
        # Enhanced level topics with advanced progression
        topics = [
            "Python Basics", "Variables & Data Types", "Strings & Input", 
            "Operators & Expressions", "Control Flow", "If Statements & Logic", 
            "Loops & Iteration", "Functions & Scope", "Lists & Indexing", 
            "Dictionaries & Sets", "Tuples & Data Structures", "File Handling",
            "Error Handling & Debugging", "Classes & Objects", "Inheritance & Polymorphism",
            "Decorators & Closures", "Generators & Iterators", "Context Managers",
            "Modules & Packages", "Testing & Quality", "Regular Expressions",
            "Database Programming", "Web Development Basics", "API Development",
            "Asynchronous Programming", "Concurrency & Threading", "Design Patterns",
            "Data Science Basics", "Machine Learning Intro", "Advanced Topics"
        ]
        
        difficulties = ["Beginner", "Easy", "Intermediate", "Advanced", "Expert"]
        
        for i in range(1, 101):  # 100 levels
            level = self._create_level(i, topics, difficulties)
            levels.append(level)
        
        return levels
    
    def _create_level(self, level_id: int, topics: List[str], difficulties: List[str]) -> Dict[str, Any]:
        """Create a single level definition."""
        is_test_level = (level_id % self.progression_rules['test_frequency'] == 0)
        is_challenge_level = (level_id % self.progression_rules['challenge_frequency'] == 0)
        
        topic_index = ((level_id - 1) // 3) % len(topics)
        difficulty_index = min((level_id - 1) // 15, len(difficulties) - 1)
        
        base_xp = 50 + (level_id // 5) * 10
        base_coins = 20 + (level_id // 10) * 5
        
        if is_challenge_level:
            return self._create_challenge_level(level_id, topics[topic_index], difficulties, difficulty_index, base_xp, base_coins)
        elif is_test_level:
            return self._create_test_level(level_id, topics[topic_index], difficulties, difficulty_index, base_xp, base_coins)
        else:
            return self._create_regular_level(level_id, topics[topic_index], difficulties, difficulty_index, base_xp, base_coins)
    
    def _create_regular_level(self, level_id: int, topic: str, difficulties: List[str], 
                            difficulty_index: int, base_xp: int, base_coins: int) -> Dict[str, Any]:
        """Create a regular lesson level."""
        return {
            "id": level_id,
            "type": "lesson",
            "title": f"Level {level_id}: {topic}",
            "topic": topic,
            "difficulty": difficulties[difficulty_index],
            "description": f"Learn {topic} with hands-on practice",
            "estimated_time": 15 + (difficulty_index * 5),
            "content": self._generate_lesson_content(level_id, topic),
            "code_example": self._generate_code_example(topic),
            "interactive_elements": self._generate_interactive_elements(topic),
            "quiz": self._generate_quiz_questions(topic),
            "practice_exercises": self._generate_practice_exercises(topic),
            "rewards": {
                "stars": 1,
                "coins": base_coins,
                "xp": base_xp
            },
            "learning_objectives": self._generate_learning_objectives(topic),
            "real_world_applications": self._generate_real_world_applications(topic),
            "prerequisites": self._calculate_prerequisites(level_id, "lesson")
        }
    
    def _create_test_level(self, level_id: int, topic: str, difficulties: List[str], 
                          difficulty_index: int, base_xp: int, base_coins: int) -> Dict[str, Any]:
        """Create a test level."""
        return {
            "id": level_id,
            "type": "test",
            "title": f"Assessment Level {level_id}",
            "topic": f"{topic} - Comprehensive Test",
            "difficulty": difficulties[difficulty_index],
            "description": f"Test your mastery of {topic}",
            "question_count": min(20, 10 + (level_id // 20)),
            "time_limit": 45,  # minutes
            "passing_score": self.progression_rules['test_minimum_score'],
            "questions": self._generate_test_questions(level_id, topic),
            "rewards": {
                "stars": 3,
                "coins": base_coins * 2,
                "xp": base_xp * 3
            },
            "prerequisites": self._calculate_prerequisites(level_id, "test")
        }
    
    def _create_challenge_level(self, level_id: int, topic: str, difficulties: List[str], 
                               difficulty_index: int, base_xp: int, base_coins: int) -> Dict[str, Any]:
        """Create a challenge level."""
        return {
            "id": level_id,
            "type": "challenge",
            "title": f"Challenge Level {level_id}: Master {topic}",
            "topic": f"{topic} - Master Challenge",
            "difficulty": difficulties[min(difficulty_index + 1, len(difficulties) - 1)],
            "description": f"Ultimate challenge to master {topic}",
            "challenge_type": "project",
            "time_limit": 60,  # minutes
            "requirements": self._generate_challenge_requirements(topic),
            "rewards": {
                "stars": 5,
                "coins": base_coins * 3,
                "xp": base_xp * 4,
                "badges": [f"{topic} Master"]
            },
            "prerequisites": self._calculate_prerequisites(level_id, "challenge")
        }
    
    def _calculate_prerequisites(self, level_id: int, level_type: str) -> List[int]:
        """Calculate prerequisites for a level."""
        if level_id == 1:
            return []
        
        if level_type == "challenge":
            # Challenge levels require completing recent levels
            return list(range(max(1, level_id - 10), level_id))
        elif level_type == "test":
            # Test levels require completing recent lessons
            return list(range(max(1, level_id - 5), level_id))
        else:
            # Regular levels require the previous level
            return [level_id - 1]
    
    def get_level_data(self, level_id: int, player=None) -> Optional[Dict[str, Any]]:
        """Get detailed data for a specific level."""
        level = next((l for l in self.levels if l.get('id') == level_id), None)
        if not level:
            return None
        
        # Add player-specific customizations if needed
        if player:
            level = self._personalize_level(level, player)
        
        return level
    
    def get_level_map(self, player) -> List[Dict[str, Any]]:
        """Get all levels with their unlock and completion status."""
        completed_levels = getattr(player, 'completed_levels', [])
        level_map = []
        
        for level in self.levels:
            level_copy = level.copy()
            level_copy['unlocked'] = self.is_level_available(level_id=level['id'], player=player)
            level_copy['completed'] = level['id'] in completed_levels
            level_copy['stars'] = self._get_level_stars(level['id'], player)
            level_copy['attempts'] = self._get_level_attempts(level['id'], player)
            level_map.append(level_copy)
        
        return level_map
    
    def is_level_available(self, level_id: int, player) -> bool:
        """Check if a level is available for the player."""
        level = self.get_level_data(level_id)
        if not level:
            return False
        
        # Level 1 is always available
        if level_id == 1:
            return True
        
        # Check prerequisites
        prerequisites = level.get('prerequisites', [])
        completed_levels = getattr(player, 'completed_levels', [])
        
        if prerequisites:
            return all(prereq in completed_levels for prereq in prerequisites)
        
        # Default sequential unlocking
        if self.progression_rules['sequential_unlock']:
            return (level_id - 1) in completed_levels
        
        return True
    
    def get_recommended_levels(self, player, count: int = 3) -> List[Dict[str, Any]]:
        """Get recommended levels based on player progress and performance."""
        available_levels = []
        completed_levels = getattr(player, 'completed_levels', [])
        
        for level in self.levels:
            if (self.is_level_available(level['id'], player) and 
                level['id'] not in completed_levels):
                available_levels.append(level)
        
        # Sort by recommendation score
        recommended = self._sort_by_recommendation_score(available_levels, player)
        return recommended[:count]
    
    def _sort_by_recommendation_score(self, levels: List[Dict[str, Any]], player) -> List[Dict[str, Any]]:
        """Sort levels by recommendation score based on player performance."""
        def calculate_score(level):
            score = 0
            
            # Prefer next sequential level
            completed_levels = getattr(player, 'completed_levels', [])
            if completed_levels:
                if level['id'] == max(completed_levels) + 1:
                    score += 100
            
            # Prefer levels matching player's skill level
            player_performance = self._get_player_average_performance(player)
            if player_performance >= 90 and level.get('difficulty') in ['Advanced', 'Expert']:
                score += 50
            elif player_performance >= 70 and level.get('difficulty') in ['Intermediate', 'Advanced']:
                score += 50
            elif player_performance < 70 and level.get('difficulty') in ['Beginner', 'Easy']:
                score += 50
            
            # Prefer level type based on recent activity
            recent_types = self._get_recent_level_types(player)
            if level.get('type') == 'test' and 'lesson' in recent_types:
                score += 30
            
            return score
        
        return sorted(levels, key=calculate_score, reverse=True)
    
    def _get_player_average_performance(self, player) -> float:
        """Calculate player's average performance percentage."""
        performance_history = getattr(player, 'performance_history', [])
        if not performance_history:
            return 70.0  # Default assumption
        
        recent_scores = [
            record.get('score_percentage', 0) 
            for record in performance_history[-10:]  # Last 10 records
        ]
        
        return sum(recent_scores) / len(recent_scores) if recent_scores else 70.0
    
    def _get_recent_level_types(self, player) -> List[str]:
        """Get types of recently completed levels."""
        performance_history = getattr(player, 'performance_history', [])
        return [
            record.get('level_type', 'lesson')
            for record in performance_history[-5:]  # Last 5 records
        ]
    
    def _get_level_stars(self, level_id: int, player) -> int:
        """Get stars earned for a specific level."""
        level_stars = getattr(player, 'level_stars', {})
        return level_stars.get(str(level_id), 0)
    
    def _get_level_attempts(self, level_id: int, player) -> int:
        """Get number of attempts for a specific level."""
        level_attempts = getattr(player, 'level_attempts', {})
        return level_attempts.get(str(level_id), 0)
    
    def _personalize_level(self, level: Dict[str, Any], player) -> Dict[str, Any]:
        """Add personalization to a level based on player preferences."""
        # This could include difficulty adjustment, content style, etc.
        personalized = level.copy()
        
        # Adjust difficulty based on player performance
        avg_performance = self._get_player_average_performance(player)
        if avg_performance >= 90:
            personalized['suggested_approach'] = 'Challenge yourself with advanced concepts'
        elif avg_performance >= 70:
            personalized['suggested_approach'] = 'Steady progress with practice exercises'
        else:
            personalized['suggested_approach'] = 'Take your time and focus on fundamentals'
        
        return personalized
    
    # Content generation methods (simplified versions)
    def _generate_lesson_content(self, level_id: int, topic: str) -> str:
        """Generate lesson content for a topic."""
        return f"""
        Level {level_id}: {topic}
        
        In this level, you'll master {topic} through hands-on practice and real-world examples.
        
        🎯 Learning Goals:
        • Understand core concepts of {topic}
        • Apply knowledge through practical exercises
        • Build confidence through guided practice
        • Connect learning to real-world applications
        
        🚀 What You'll Build:
        Interactive projects that demonstrate {topic} in action.
        """
    
    def _generate_code_example(self, topic: str) -> str:
        """Generate code example for a topic."""
        examples = {
            "Variables & Data Types": '''# Variables and Data Types Example
name = "Python Learner"
age = 25
height = 5.8
is_student = True

print(f"Name: {name}, Age: {age}, Height: {height}ft, Student: {is_student}")
''',
            "Lists & Indexing": '''# Lists and Indexing Example
fruits = ["apple", "banana", "orange", "grape"]

# Accessing elements
first_fruit = fruits[0]
last_fruit = fruits[-1]

# Adding and removing
fruits.append("mango")
fruits.remove("banana")

print(f"First: {first_fruit}, Last: {last_fruit}")
print(f"All fruits: {fruits}")
'''
        }
        
        return examples.get(topic, f"# {topic} Example\n# Your code here")
    
    def _generate_interactive_elements(self, topic: str) -> List[Dict[str, Any]]:
        """Generate interactive elements for a topic."""
        return [
            {"type": "code_playground", "description": f"Try {topic} concepts"},
            {"type": "visualization", "description": f"{topic} visual guide"},
            {"type": "quiz_game", "description": f"Interactive {topic} quiz"}
        ]
    
    def _generate_quiz_questions(self, topic: str) -> List[Dict[str, Any]]:
        """Generate quiz questions for a topic."""
        topic_lower = topic.lower()
        
        if 'variable' in topic_lower:
            return [
                {
                    "question": "Which is a valid Python variable name?",
                    "type": "multiple_choice",
                    "options": ["2variable", "variable_name", "variable-name", "variable name"],
                    "correct": 1,
                    "explanation": "Variable names must start with a letter or underscore."
                }
            ]
        elif 'list' in topic_lower:
            return [
                {
                    "question": "How do you access the first element of a list?",
                    "type": "multiple_choice",
                    "options": ["list[1]", "list[0]", "list.first()", "list.get(0)"],
                    "correct": 1,
                    "explanation": "Python uses zero-based indexing."
                }
            ]
        
        return [
            {
                "question": f"What is the main purpose of {topic}?",
                "type": "multiple_choice",
                "options": ["To complicate code", "To solve problems efficiently", "To slow execution", "To confuse developers"],
                "correct": 1,
                "explanation": f"{topic} helps solve programming problems efficiently."
            }
        ]
    
    def _generate_practice_exercises(self, topic: str) -> List[Dict[str, Any]]:
        """Generate practice exercises for a topic."""
        return [
            {
                "title": f"Basic {topic} Exercise",
                "description": f"Practice fundamental {topic} concepts",
                "starter_code": f"# Practice {topic} here\n",
                "difficulty": "beginner"
            }
        ]
    
    def _generate_learning_objectives(self, topic: str) -> List[str]:
        """Generate learning objectives for a topic."""
        return [
            f"Master fundamental concepts of {topic}",
            f"Apply {topic} in practical scenarios",
            f"Debug and troubleshoot {topic}-related issues",
            f"Write clean, efficient code using {topic}"
        ]
    
    def _generate_real_world_applications(self, topic: str) -> List[str]:
        """Generate real-world applications for a topic."""
        return [
            f"{topic} in web development",
            f"{topic} in data science",
            f"{topic} in automation scripts",
            f"{topic} in enterprise software"
        ]
    
    def _generate_test_questions(self, level_id: int, topic: str) -> List[Dict[str, Any]]:
        """Generate test questions for assessments."""
        return [
            {
                "question": f"Advanced question about {topic}",
                "type": "multiple_choice",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct": 1,
                "explanation": f"This tests advanced understanding of {topic}.",
                "difficulty": "advanced"
            }
        ]
    
    def _generate_challenge_requirements(self, topic: str) -> List[str]:
        """Generate requirements for challenge levels."""
        return [
            f"Demonstrate mastery of {topic}",
            "Implement clean, readable code",
            "Include proper error handling",
            "Provide comprehensive testing"
        ]
    
    def validate_answer_submission(self, level_id: int, player, submitted_answers: List[Any]) -> Dict[str, Any]:
        """
        Validate submitted answers and provide feedback.
        
        Args:
            level_id: ID of the level being attempted
            player: Player object
            submitted_answers: List of submitted answers
            
        Returns:
            Dictionary containing validation results and feedback
        """
        level = self.get_level_data(level_id, player)
        if not level:
            return {
                "success": False,
                "error": "Level not found",
                "feedback": {
                    "type": "error",
                    "title": "Level Error",
                    "message": "The requested level could not be found. Please try again.",
                    "show_retry": True
                }
            }
        
        # Get questions for the level
        questions = level.get('quiz', level.get('questions', []))
        if not questions:
            return {
                "success": False,
                "error": "No questions found",
                "feedback": {
                    "type": "error", 
                    "title": "Content Error",
                    "message": "This level has no questions to validate. Please contact support.",
                    "show_retry": False
                }
            }
        
        # Validate answer count
        if len(submitted_answers) != len(questions):
            return {
                "success": False,
                "error": "Answer count mismatch",
                "feedback": {
                    "type": "error",
                    "title": "Incomplete Submission",
                    "message": f"Please answer all {len(questions)} questions before submitting.",
                    "show_retry": True
                }
            }
        
        # Calculate score and detailed results
        validation_result = self._calculate_score_and_feedback(questions, submitted_answers, level)
        
        # Determine if level is passed
        minimum_score = level.get('passing_score', self.progression_rules['minimum_score'])
        passed = validation_result['score_percentage'] >= minimum_score
        
        # Update player attempts
        self._record_level_attempt(player, level_id, validation_result['score_percentage'], passed)
        
        # Generate appropriate feedback
        feedback = self._generate_submission_feedback(validation_result, passed, level)
        
        # Handle level progression if passed
        progression_data = {}
        if passed:
            progression_data = self._handle_level_completion(player, level_id, validation_result)
        
        return {
            "success": True,
            "passed": passed,
            "score_percentage": validation_result['score_percentage'],
            "correct_answers": validation_result['correct_count'],
            "total_questions": validation_result['total_questions'],
            "detailed_results": validation_result['detailed_results'],
            "feedback": feedback,
            "progression": progression_data,
            "retry_available": self._can_retry_level(player, level_id)
        }
    
    def _calculate_score_and_feedback(self, questions: List[Dict], answers: List[Any], level: Dict) -> Dict[str, Any]:
        """Calculate score and generate detailed feedback for each question."""
        correct_count = 0
        detailed_results = []
        
        for i, (question, answer) in enumerate(zip(questions, answers)):
            correct_answer = question.get('correct')
            is_correct = (answer == correct_answer)
            
            if is_correct:
                correct_count += 1
            
            # Generate detailed feedback for this question
            question_feedback = {
                'question_number': i + 1,
                'question_text': question.get('question', ''),
                'submitted_answer': answer,
                'correct_answer': correct_answer,
                'is_correct': is_correct,
                'explanation': question.get('explanation', ''),
                'options': question.get('options', [])
            }
            
            # Add specific feedback message
            if is_correct:
                question_feedback['feedback_message'] = "Correct! " + question_feedback['explanation']
                question_feedback['feedback_type'] = "success"
            else:
                if question.get('options') and correct_answer is not None:
                    correct_option_text = question['options'][correct_answer] if correct_answer < len(question['options']) else "Unknown"
                    question_feedback['feedback_message'] = f"Incorrect. The correct answer is: {correct_option_text}. {question_feedback['explanation']}"
                else:
                    question_feedback['feedback_message'] = f"Incorrect. {question_feedback['explanation']}"
                question_feedback['feedback_type'] = "error"
            
            detailed_results.append(question_feedback)
        
        total_questions = len(questions)
        score_percentage = (correct_count / total_questions * 100) if total_questions > 0 else 0
        
        return {
            'correct_count': correct_count,
            'total_questions': total_questions,
            'score_percentage': score_percentage,
            'detailed_results': detailed_results
        }
    
    def _generate_submission_feedback(self, validation_result: Dict, passed: bool, level: Dict) -> Dict[str, Any]:
        """Generate comprehensive feedback for the submission."""
        score_percentage = validation_result['score_percentage']
        correct_count = validation_result['correct_count']
        total_questions = validation_result['total_questions']
        
        if passed:
            # Success feedback
            if score_percentage == 100:
                feedback = {
                    "type": "success",
                    "title": "Perfect Score! 🌟",
                    "message": f"Outstanding! You answered all {total_questions} questions correctly!",
                    "score_message": f"Score: {score_percentage:.0f}%",
                    "encouragement": "You've mastered this topic completely!",
                    "show_next_button": True,
                    "show_retry": False,
                    "next_button_text": "Continue to Next Level",
                    "celebration_type": "perfect"
                }
            elif score_percentage >= 90:
                feedback = {
                    "type": "success", 
                    "title": "Excellent Work! ⭐",
                    "message": f"Great job! You got {correct_count} out of {total_questions} questions correct.",
                    "score_message": f"Score: {score_percentage:.0f}%",
                    "encouragement": "You have a strong understanding of this topic!",
                    "show_next_button": True,
                    "show_retry": False,
                    "next_button_text": "Continue to Next Level",
                    "celebration_type": "excellent"
                }
            else:
                feedback = {
                    "type": "success",
                    "title": "Well Done! ✅", 
                    "message": f"Good work! You got {correct_count} out of {total_questions} questions correct.",
                    "score_message": f"Score: {score_percentage:.0f}%",
                    "encouragement": "You've passed this level and can move on!",
                    "show_next_button": True,
                    "show_retry": True,
                    "next_button_text": "Continue to Next Level",
                    "retry_button_text": "Retry for Better Score",
                    "celebration_type": "success"
                }
        else:
            # Failure feedback
            minimum_score = level.get('passing_score', self.progression_rules['minimum_score'])
            
            if score_percentage >= minimum_score - 10:
                feedback = {
                    "type": "warning",
                    "title": "Almost There! 📚",
                    "message": f"You got {correct_count} out of {total_questions} questions correct.",
                    "score_message": f"Score: {score_percentage:.0f}% (Need {minimum_score}% to pass)",
                    "encouragement": "You're very close! Review the explanations and try again.",
                    "show_next_button": False,
                    "show_retry": True,
                    "retry_button_text": "Try Again",
                    "study_suggestion": "Focus on the questions you missed and review the explanations."
                }
            else:
                feedback = {
                    "type": "error",
                    "title": "Keep Learning! 📖",
                    "message": f"You got {correct_count} out of {total_questions} questions correct.",
                    "score_message": f"Score: {score_percentage:.0f}% (Need {minimum_score}% to pass)",
                    "encouragement": "Don't worry! Learning takes practice. Review the material and try again.",
                    "show_next_button": False,
                    "show_retry": True,
                    "retry_button_text": "Study and Retry",
                    "study_suggestion": "Take some time to review the lesson content before retrying."
                }
        
        return feedback
    
    def _handle_level_completion(self, player, level_id: int, validation_result: Dict) -> Dict[str, Any]:
        """Handle level completion and unlock progression."""
        # Update player's completed levels
        if hasattr(player, 'completed_levels') and level_id not in player.completed_levels:
            player.completed_levels.append(level_id)
        
        # Calculate stars earned
        score_percentage = validation_result['score_percentage']
        stars = self._calculate_stars_earned(score_percentage)
        
        # Update player's level stars
        if hasattr(player, 'level_stars'):
            current_stars = player.level_stars.get(str(level_id), 0)
            if stars > current_stars:
                player.level_stars[str(level_id)] = stars
        
        # Determine next level to unlock
        next_level_id = self._get_next_level_id(level_id)
        next_level_unlocked = False
        
        if next_level_id:
            next_level_unlocked = self.is_level_available(next_level_id, player)
        
        # Get level rewards
        level = self.get_level_data(level_id)
        rewards = level.get('rewards', {}) if level else {}
        
        return {
            "level_completed": level_id,
            "stars_earned": stars,
            "next_level_id": next_level_id,
            "next_level_unlocked": next_level_unlocked,
            "rewards": rewards,
            "can_proceed": next_level_unlocked,
            "redirect_to_dashboard": True
        }
    
    def _calculate_stars_earned(self, score_percentage: float) -> int:
        """Calculate stars earned based on score percentage."""
        if score_percentage >= 95:
            return 3
        elif score_percentage >= 85:
            return 2
        elif score_percentage >= 70:
            return 1
        else:
            return 0
    
    def _get_next_level_id(self, current_level_id: int) -> Optional[int]:
        """Get the ID of the next level."""
        next_id = current_level_id + 1
        next_level = next((l for l in self.levels if l.get('id') == next_id), None)
        return next_id if next_level else None
    
    def _record_level_attempt(self, player, level_id: int, score: float, passed: bool):
        """Record a level attempt in player's history."""
        if not hasattr(player, 'level_attempts'):
            player.level_attempts = {}
        
        if not hasattr(player, 'performance_history'):
            player.performance_history = []
        
        # Update attempt count
        attempts_key = str(level_id)
        current_attempts = player.level_attempts.get(attempts_key, 0)
        player.level_attempts[attempts_key] = current_attempts + 1
        
        # Add to performance history
        performance_record = {
            'level_id': level_id,
            'score_percentage': score,
            'passed': passed,
            'attempt_number': player.level_attempts[attempts_key],
            'timestamp': datetime.now().isoformat(),
            'type': 'level_attempt'
        }
        
        player.performance_history.append(performance_record)
    
    def _can_retry_level(self, player, level_id: int) -> bool:
        """Check if player can retry a level."""
        if not self.progression_rules['retry_allowed']:
            return False
        
        attempts_key = str(level_id)
        current_attempts = getattr(player, 'level_attempts', {}).get(attempts_key, 0)
        max_retries = self.progression_rules['max_retries']
        
        return current_attempts < max_retries
    
    def get_next_available_level(self, player) -> Optional[Dict[str, Any]]:
        """Get the next available level for the player."""
        completed_levels = getattr(player, 'completed_levels', [])
        
        # Find the first uncompleted level that's available
        for level in self.levels:
            level_id = level['id']
            if level_id not in completed_levels and self.is_level_available(level_id, player):
                return level
        
        return None
    
    def get_dashboard_data(self, player) -> Dict[str, Any]:
        """Get comprehensive dashboard data for the player."""
        level_map = self.get_level_map(player)
        next_level = self.get_next_available_level(player)
        completed_levels = getattr(player, 'completed_levels', [])
        
        # Calculate progress statistics
        total_levels = len(self.levels)
        completed_count = len(completed_levels)
        progress_percentage = (completed_count / total_levels * 100) if total_levels > 0 else 0
        
        # Get stars statistics
        total_stars = sum(getattr(player, 'level_stars', {}).values())
        max_possible_stars = completed_count * 3
        
        return {
            "level_map": level_map,
            "next_level": next_level,
            "progress": {
                "completed_levels": completed_count,
                "total_levels": total_levels,
                "progress_percentage": progress_percentage,
                "total_stars": total_stars,
                "max_possible_stars": max_possible_stars
            },
            "recent_activity": self._get_recent_activity(player),
            "achievements_available": self._check_available_achievements(player)
        }
    
    def _get_recent_activity(self, player) -> List[Dict[str, Any]]:
        """Get recent activity for the player."""
        if not hasattr(player, 'performance_history'):
            return []
        
        # Get last 5 activities
        recent = sorted(
            player.performance_history,
            key=lambda x: x.get('timestamp', ''),
            reverse=True
        )[:5]
        
        return recent
    
    def _check_available_achievements(self, player) -> List[Dict[str, Any]]:
        """Check for achievements that can be unlocked."""
        # This would integrate with the achievement system
        # For now, return placeholder data
        return []
