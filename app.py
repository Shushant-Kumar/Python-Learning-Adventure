"""
Flask Web Application for Python Learning Adventure
A web-based gamified Python learning platform with proper authentication
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_login import login_required, current_user
import json
import os
from datetime import datetime, timedelta
from game_logic.coordinator import GameLogicCoordinator as AdvancedGameLogic
from player_manager import PlayerManager
from auth import db, bcrypt, login_manager, create_database_tables, User
from auth_routes import auth_bp
from admin_routes import admin_bp
from main_routes import main_bp

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'python_learning_adventure_secret_key_2025'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///python_learning.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['WTF_CSRF_ENABLED'] = True

# Initialize extensions
db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(admin_bp)
app.register_blueprint(main_bp)

# Homepage route (before login)
@app.route('/welcome')
def welcome():
    """Landing page for visitors before login/signup."""
    return render_template('welcome.html')

# Initialize game components
game_logic = AdvancedGameLogic()
player_manager = PlayerManager()

# Create database tables
# create_database_tables(app)  # Remove automatic creation

@app.route('/')
def home():
    """Homepage - redirect based on authentication status."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    else:
        return redirect(url_for('welcome'))

@app.route('/dashboard')
@login_required
def main_dashboard():
    """Main game page with level map (for authenticated users)."""
    # Convert User to Player-like object for compatibility
    player_data = current_user.get_game_progress()
    player_obj = current_user.get_player_object()
    levels = game_logic.get_level_map(player_obj)
    
    return render_template('index.html', player=player_data, levels=levels)

@app.route('/level/<int:level_id>')
@login_required
def level(level_id):
    """Play a specific level."""
    # Convert User to Player-like object for compatibility
    player_data = current_user.get_game_progress()
    player_obj = current_user.get_player_object()
    level_data = game_logic.get_level_data(level_id, player_obj)
    
    if not level_data:
        flash('Level not found or not yet unlocked!', 'error')
        return redirect(url_for('main.dashboard'))
    
    return render_template('level.html', level=level_data, player=player_data)

@app.route('/test/<int:level_id>')
@login_required
def test(level_id):
    """Take a test (every 10th level)."""
    player_data = current_user.get_game_progress()
    player_obj = current_user.get_player_object()
    
    # Tests are just special levels (every 10th level)
    if level_id % 10 != 0:
        flash('This is not a test level!', 'error')
        return redirect(url_for('main.dashboard'))
    
    level_data = game_logic.get_level_data(level_id, player_obj)
    
    if not level_data:
        flash('Test not found or not yet unlocked!', 'error')
        return redirect(url_for('main.dashboard'))
    
    # Mark this as a test level for the template
    level_data['is_test'] = True
    return render_template('test.html', test=level_data, player=player_data)

@app.route('/api/complete_level', methods=['POST'])
@login_required
def complete_level():
    """Complete a level and update progress."""
    data = request.get_json()
    level_id = data.get('level_id')
    quiz_answers = data.get('quiz_answers', [])
    
    player_data = current_user.get_game_progress()
    player_obj = current_user.get_player_object()
    result = game_logic.complete_level(player_obj, level_id, quiz_answers)
    
    # Update user's game progress
    if result.get('success'):
        current_user.update_game_progress(
            level=level_id,
            score=result.get('score', 0),
            achievements=result.get('achievements', []),
            streak=result.get('streak', 0)
        )
    
    return jsonify(result)

@app.route('/api/complete_test', methods=['POST'])
@login_required
def complete_test():
    """Complete a test and update progress."""
    data = request.get_json()
    level_id = data.get('level_id')
    test_answers = data.get('test_answers', [])
    
    # Tests use the same completion system as regular levels
    player_data = current_user.get_game_progress()
    player_obj = current_user.get_player_object()
    result = game_logic.complete_level(player_obj, level_id, test_answers)
    
    # Update user's game progress
    if result.get('success'):
        current_user.update_game_progress(
            level=level_id,
            score=result.get('score', 0),
            achievements=result.get('achievements', []),
            streak=result.get('streak', 0)
        )
    
    return jsonify(result)

@app.route('/profile')
@login_required
def profile():
    """Player profile page."""
    player_data = current_user.get_game_progress()
    player_obj = current_user.get_player_object()
    stats = game_logic.get_player_stats(player_obj)
    
    return render_template('profile.html', player=player_data, stats=stats)

@app.route('/rewards')
@login_required
def rewards():
    """Rewards shop page."""
    player_data = current_user.get_game_progress()
    player_obj = current_user.get_player_object()
    available_rewards = game_logic.get_available_rewards(player_obj)
    
    return render_template('rewards.html', player=player_data, rewards=available_rewards)

@app.route('/api/purchase_reward', methods=['POST'])
@login_required
def purchase_reward():
    """Purchase a reward."""
    data = request.get_json()
    reward_id = data.get('reward_id')
    
    player_data = current_user.get_game_progress()
    player_obj = current_user.get_player_object()
    result = game_logic.purchase_reward(player_obj, reward_id)
    
    # Update user's game progress
    if result.get('success'):
        current_user.update_game_progress(
            score=result.get('score_change', 0)
        )
    
    return jsonify(result)

@app.route('/api/level_details/<int:level_id>')
@login_required
def level_details(level_id):
    """Get level details for modal."""
    player_data = current_user.get_game_progress()
    player_obj = current_user.get_player_object()
    level_data = game_logic.get_level_data(level_id, player_obj)
    
    if not level_data:
        return jsonify({'success': False, 'error': 'Level not found'})
    
    return jsonify({
        'success': True,
        'topic': level_data['topic'],
        'difficulty': level_data['difficulty'],
        'description': level_data.get('description', level_data.get('content', 'Learn Python concepts')[:100] + '...'),
        'rewards': level_data['rewards']
    })

@app.route('/achievements')
@login_required
def achievements():
    """Achievements page."""
    player_data = current_user.get_game_progress()
    player_obj = current_user.get_player_object()
    achievements = game_logic.get_player_achievements(player_obj)
    
    return render_template('achievements.html', player=player_data, achievements=achievements)

@app.route('/leaderboard')
@login_required
def leaderboard():
    """Leaderboard page."""
    # For now, create a simple leaderboard from the users table
    all_users = User.query.all()
    top_users = sorted([u for u in all_users if u.total_score > 0], key=lambda x: x.total_score, reverse=True)[:10]
    top_players = [user.get_game_progress() for user in top_users]
    current_player = current_user.get_game_progress()
    
    return render_template('leaderboard.html', 
                         top_players=top_players, 
                         current_player=current_player)

# Remove the old logout route since it's handled by auth_bp

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

# Template filters
@app.template_filter('from_json')
def from_json_filter(value):
    """Convert JSON string to Python object."""
    import json
    try:
        return json.loads(value) if value else []
    except (json.JSONDecodeError, TypeError):
        return []

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('player_data', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('static/images', exist_ok=True)
    
    # Ensure database tables exist (but don't recreate if they exist)
    with app.app_context():
        try:
            db.create_all()
            print("Database is ready!")
        except Exception as e:
            print(f"Database check error: {e}")
            print("Please run 'python init_db.py' to initialize the database.")
    
    # Run the Flask app
    app.run(debug=True, host='127.0.0.1', port=5000)
