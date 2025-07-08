# 🐍 Python Learning Adventure

A gamified Python learning platform with levels, rewards, tests, and achievements!

## 🎮 Features

- **📚 Interactive Lessons**: Learn Python concepts through engaging lessons
- **🏆 Level System**: Progress through levels as you gain experience
- **💰 Reward System**: Earn coins to unlock rewards and achievements
- **📝 Tests & Quizzes**: Test your knowledge with comprehensive assessments
- **🎯 Achievements**: Unlock achievements for reaching milestones
- **🔥 Streak System**: Maintain daily learning streaks for bonuses
- **💾 Progress Tracking**: Your progress is automatically saved

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- No external dependencies required (uses only Python standard library)

### Installation
1. Clone or download this repository
2. Navigate to the project directory
3. Run the game:
   ```bash
   python main.py
   ```

## 🎯 How to Play

### Main Menu Options
1. **📚 Start Learning**: Access interactive Python lessons
2. **📝 Take a Test**: Test your knowledge with comprehensive quizzes
3. **📊 View Progress**: See your achievements, stats, and progress
4. **🏆 Rewards Shop**: Spend coins on rewards and unlockables
5. **⚙️ Settings**: Configure game settings and view help
6. **🚪 Save & Exit**: Save your progress and exit the game

### Learning System
- Complete lessons to earn XP and coins
- Each lesson includes:
  - Detailed explanations
  - Code examples
  - Practical tips
  - Knowledge quiz
- Lessons are unlocked based on your level

### Testing System
- Take tests to assess your understanding
- Tests include:
  - Multiple choice questions
  - Code writing exercises
  - Immediate feedback
- Scores are tracked and contribute to achievements

### Progression System
- **Experience Points (XP)**: Earned by completing lessons and tests
- **Levels**: Unlock new content as you level up
- **Coins**: Spend on rewards and customizations
- **Achievements**: Unlock special milestones
- **Streaks**: Maintain daily learning habits

## 📚 Curriculum

### Beginner Level (Level 1-2)
- **Python Basics**: Variables, data types, and basic operations
- **Strings**: String manipulation and formatting
- **Input/Output**: Getting user input and displaying output

### Intermediate Level (Level 3-4)
- **Control Flow**: If statements, conditional logic
- **Loops**: For loops, while loops, and loop control
- **Functions**: Defining and calling functions

### Advanced Level (Level 5+)
- **Data Structures**: Lists, dictionaries, sets
- **File Handling**: Reading and writing files
- **Error Handling**: Try/except blocks
- **Object-Oriented Programming**: Classes and objects

## 🏆 Achievements

### Learning Achievements
- **🎯 First Steps**: Complete your first lesson
- **📚 Dedicated Learner**: Complete 5 lessons
- **🐍 Python Explorer**: Complete lessons from 3 different topics

### Performance Achievements
- **🧠 Quiz Master**: Score 100% on any test
- **📝 Test Taker**: Complete 3 tests

### Consistency Achievements
- **🔥 Streak Starter**: Maintain a 3-day learning streak
- **🌟 Streak Master**: Maintain a 7-day learning streak

### Progression Achievements
- **⬆️ Level Up**: Reach level 5

## 💰 Rewards Shop

Spend your hard-earned coins on:
- **🎨 Custom Themes**: Personalize your learning experience
- **🚀 XP Boosters**: Get double XP for upcoming lessons
- **🏅 Achievement Badges**: Show off your accomplishments
- **📚 Bonus Content**: Access to advanced topics
- **🎯 Skill Certificates**: Official proficiency certificates

## 📁 Project Structure

```
python_learning_game/
├── main.py              # Main entry point
├── player.py            # Player class and progress management
├── game_engine.py       # Core game logic and content
├── ui_manager.py        # User interface and display
├── requirements.txt     # Project dependencies
├── README.md           # This file
└── player_data.json    # Saved player progress (created automatically)
```

## 🔧 Customization

### Adding New Lessons
1. Edit the `_load_lessons()` method in `game_engine.py`
2. Follow the existing lesson structure:
   ```python
   {
       "id": "unique_lesson_id",
       "title": "Lesson Title",
       "topic": "Topic Name",
       "difficulty": "Beginner|Intermediate|Advanced",
       "level_requirement": 1,
       "content": "Lesson content...",
       "code_example": "# Python code example",
       "tips": ["Tip 1", "Tip 2"],
       "quiz": [
           {
               "question": "Question text",
               "type": "multiple_choice",
               "options": ["Option 1", "Option 2"],
               "correct": 0,
               "explanation": "Answer explanation"
           }
       ]
   }
   ```

### Adding New Tests
1. Edit the `_load_tests()` method in `game_engine.py`
2. Follow the existing test structure with questions

### Adding New Achievements
1. Edit the `_load_achievements()` method in `game_engine.py`
2. Add corresponding logic in `_check_achievements()`

## 🎨 UI Features

- **Colorful Output**: Uses ANSI color codes for better visual experience
- **Progress Bars**: Visual representation of progress
- **Emojis**: Fun emojis to make learning more engaging
- **Formatted Tables**: Clean display of information
- **Interactive Menus**: Easy navigation through options

## 💾 Save System

- Progress is automatically saved to `player_data.json`
- Includes all player data:
  - Level and experience
  - Completed lessons
  - Test scores
  - Achievements
  - Coins and rewards
  - Learning streak

## 🚀 Future Enhancements

Potential features to add:
- **Multiplayer Mode**: Compete with friends
- **Code Execution**: Run Python code directly in the game
- **Advanced Analytics**: Detailed learning analytics
- **Mobile App**: Cross-platform mobile version
- **Community Features**: Share achievements and compete
- **AI Tutor**: Personalized learning recommendations

## 🤝 Contributing

Feel free to contribute to this project by:
1. Adding new lessons and content
2. Improving the UI/UX
3. Adding new features
4. Fixing bugs
5. Enhancing documentation

## 📜 License

This project is open source and available under the MIT License.

## 🐛 Troubleshooting

### Common Issues

**Game won't start:**
- Ensure you have Python 3.7+ installed
- Check that all files are in the same directory

**Progress not saving:**
- Ensure the directory is writable
- Check file permissions

**Colors not displaying:**
- Some terminals may not support ANSI colors
- Try running in a different terminal

### Support

If you encounter any issues or have suggestions:
1. Check the troubleshooting section
2. Review the code for understanding
3. Modify the game to suit your needs

## 🎓 Learning Tips

1. **Take your time**: Don't rush through lessons
2. **Practice coding**: Try the examples yourself
3. **Ask questions**: Think critically about concepts
4. **Review mistakes**: Learn from incorrect answers
5. **Maintain streaks**: Consistent daily practice is key
6. **Experiment**: Try modifying the code examples

Happy learning! 🚀🐍
