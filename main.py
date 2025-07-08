"""
Python Learning Game - Main Entry Point
A gamified Python learning platform with levels, rewards, and tests.
"""

import json
import os
from datetime import datetime
from game_engine import GameEngine
from ui_manager import UIManager
from player import Player

def main():
    """Main function to start the Python learning game."""
    print("=" * 60)
    print("🐍 WELCOME TO PYTHON LEARNING ADVENTURE! 🐍")
    print("=" * 60)
    print()
    
    # Initialize game components
    ui = UIManager()
    game_engine = GameEngine()
    
    # Load or create player profile
    player = load_or_create_player()
    
    # Main game loop
    while True:
        choice = ui.show_main_menu(player)
        
        if choice == "1":
            # Start learning/play levels
            game_engine.start_learning_session(player)
        elif choice == "2":
            # Take a test
            game_engine.take_test(player)
        elif choice == "3":
            # View progress and achievements
            ui.show_progress(player)
        elif choice == "4":
            # View rewards
            ui.show_rewards(player)
        elif choice == "5":
            # Settings
            ui.show_settings()
        elif choice == "6":
            # Save and exit
            save_player(player)
            print("\n🎯 Thanks for playing! Keep learning Python! 🎯")
            break
        else:
            print("❌ Invalid choice. Please try again.")

def load_or_create_player():
    """Load existing player or create a new one."""
    player_file = "player_data.json"
    
    if os.path.exists(player_file):
        try:
            with open(player_file, 'r') as f:
                data = json.load(f)
                return Player.from_dict(data)
        except:
            print("⚠️ Error loading player data. Creating new profile.")
    
    # Create new player
    name = input("\n🎮 Enter your name: ").strip()
    if not name:
        name = "Python Learner"
    
    return Player(name)

def save_player(player):
    """Save player data to file."""
    try:
        with open("player_data.json", 'w') as f:
            json.dump(player.to_dict(), f, indent=2)
        print("💾 Game progress saved!")
    except Exception as e:
        print(f"⚠️ Error saving progress: {e}")

if __name__ == "__main__":
    main()
