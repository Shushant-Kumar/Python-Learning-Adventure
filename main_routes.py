"""
Main Routes Module
Handles main game functionality routes
"""

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from game_logic.coordinator import GameLogicCoordinator as AdvancedGameLogic
from player_manager import PlayerManager
from auth import db, User
from sqlalchemy import desc
import json

main_bp = Blueprint('main', __name__)

# Initialize game components
game_logic = AdvancedGameLogic()
player_manager = PlayerManager()

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Main game page with level map (for authenticated users)."""
    # Convert User to Player-like object for compatibility
    player_data = current_user.get_game_progress()
    player_obj = current_user.get_player_object()
    levels = game_logic.get_level_map(player_obj)
    
    return render_template('index.html', player=player_data, levels=levels)

@main_bp.route('/level/<int:level_id>')
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

@main_bp.route('/test/<int:level_id>')
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

@main_bp.route('/api/complete_level', methods=['POST'])
@login_required
def complete_level():
    """Complete a level and update progress."""
    data = request.get_json()
    level_id = data.get('level_id')
    quiz_answers = data.get('quiz_answers', [])
    
    # Convert User to Player-like object for compatibility
    player_obj = current_user.get_player_object()
    
    # Complete level using game logic
    result = game_logic.complete_level(player_obj, level_id, quiz_answers)
    
    if result['success']:
        # Update user progress in database
        current_user.current_level = result.get('new_level', current_user.current_level)
        current_user.total_score = result.get('total_score', current_user.total_score)
        
        # Update completed levels safely
        completed_levels_str = current_user.completed_levels or '[]'
        try:
            completed_levels = json.loads(completed_levels_str)
        except (json.JSONDecodeError, TypeError):
            completed_levels = []
        
        if level_id not in completed_levels:
            completed_levels.append(level_id)
            current_user.completed_levels = json.dumps(completed_levels)
        
        # Update achievements
        if result.get('achievements'):
            achievements_str = current_user.achievements or '[]'
            try:
                user_achievements = json.loads(achievements_str)
            except (json.JSONDecodeError, TypeError):
                user_achievements = []
            
            for achievement in result['achievements']:
                if achievement not in user_achievements:
                    user_achievements.append(achievement)
            current_user.achievements = json.dumps(user_achievements)
        
        # Update activity timestamp
        from datetime import datetime
        current_user.last_activity = datetime.utcnow()
        
        # Commit changes
        db.session.commit()
    
    return jsonify(result)

@main_bp.route('/api/complete_test', methods=['POST'])
@login_required
def complete_test():
    """Complete a test and update progress."""
    data = request.get_json()
    test_id = data.get('test_id')
    answers = data.get('answers', [])
    
    # Convert User to Player-like object for compatibility
    player_obj = current_user.get_player_object()
    
    # Tests use the same completion system as regular levels
    result = game_logic.complete_level(player_obj, test_id, answers)
    
    if result['success']:
        # Update user progress in database
        current_user.current_level = result.get('new_level', current_user.current_level)
        current_user.total_score = result.get('total_score', current_user.total_score)
        
        # Update completed levels safely (for tests too)
        completed_levels_str = current_user.completed_levels or '[]'
        try:
            completed_levels = json.loads(completed_levels_str)
        except (json.JSONDecodeError, TypeError):
            completed_levels = []
        
        if test_id not in completed_levels:
            completed_levels.append(test_id)
            current_user.completed_levels = json.dumps(completed_levels)
        
        # Update achievements safely
        if result.get('achievements'):
            achievements_str = current_user.achievements or '[]'
            try:
                user_achievements = json.loads(achievements_str)
            except (json.JSONDecodeError, TypeError):
                user_achievements = []
            
            for achievement in result['achievements']:
                if achievement not in user_achievements:
                    user_achievements.append(achievement)
            current_user.achievements = json.dumps(user_achievements)
        
        # Update activity timestamp
        from datetime import datetime
        current_user.last_activity = datetime.utcnow()
        
        # Commit changes
        db.session.commit()
    
    return jsonify(result)

@main_bp.route('/api/get_hint', methods=['POST'])
@login_required
def get_hint():
    """Get a hint for a level."""
    data = request.get_json()
    level_id = data.get('level_id')
    
    # Convert User to Player-like object for compatibility
    player_obj = current_user.get_player_object()
    
    hint = game_logic.get_hint(player_obj, level_id)
    return jsonify({'hint': hint})

@main_bp.route('/profile')
@login_required
def profile():
    """User profile page."""
    # Get user stats
    completed_levels = json.loads(current_user.completed_levels) if current_user.completed_levels else []
    achievements = json.loads(current_user.achievements) if current_user.achievements else []
    
    # Calculate statistics
    stats = {
        'levels_completed': len(completed_levels),
        'total_score': current_user.total_score,
        'current_level': current_user.current_level,
        'achievements_count': len(achievements),
        'streak_count': current_user.streak_count,
        'member_since': current_user.created_at,
        'last_activity': current_user.last_activity
    }
    
    return render_template('profile.html', user=current_user, stats=stats, achievements=achievements)

@main_bp.route('/leaderboard')
@login_required
def leaderboard():
    """Leaderboard page."""
    # Get top users by score
    all_users = User.query.all()
    top_users = sorted([u for u in all_users if u.total_score > 0], key=lambda x: x.total_score, reverse=True)[:50]
    
    # Find current user's rank
    user_rank = None
    for i, user in enumerate(top_users, 1):
        if user.id == current_user.id:
            user_rank = i
            break
    
    # If current user not in top 50, find their actual rank
    if not user_rank:
        users_above = User.query.filter(User.total_score > current_user.total_score).count()
        user_rank = users_above + 1
    
    return render_template('leaderboard.html', top_users=top_users, user_rank=user_rank)
