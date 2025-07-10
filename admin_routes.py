"""
Admin Routes Module
Handles admin functionality for user management, content moderation, and system administration
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from functools import wraps
from auth import db, User
from game_logic.coordinator import GameLogicCoordinator as AdvancedGameLogic
from game_logic.player_state import PlayerState
import json
from datetime import datetime

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Initialize game logic
game_logic = AdvancedGameLogic()

def create_dummy_player(level: int = 1) -> PlayerState:
    """Create a dummy player for admin operations."""
    dummy_player = PlayerState(
        id="admin-dummy",
        username="admin-dummy",
        created_at=datetime.now().isoformat(),
        last_login=datetime.now().isoformat()
    )
    dummy_player.current_level = level
    dummy_player.completed_levels = list(range(1, level))
    return dummy_player

def admin_required(f):
    """Decorator to require admin privileges."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Admin privileges required to access this page.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    """Admin dashboard with overview statistics."""
    # Get statistics
    total_users = User.query.count()
    active_users = User.query.filter_by(is_active_user=True).count()
    admin_users = User.query.filter_by(is_admin=True).count()
    
    # Calculate average score
    all_users = User.query.all()
    users_with_scores = [user for user in all_users if user.total_score > 0]
    avg_score = sum(user.total_score for user in users_with_scores) / len(users_with_scores) if users_with_scores else 0
    
    # Get recent users (last 10)
    recent_users = sorted(all_users, key=lambda x: x.created_at, reverse=True)[:10]
    
    # Get top performers
    top_performers = sorted([user for user in all_users if user.total_score > 0], key=lambda x: x.total_score, reverse=True)[:10]
    
    stats = {
        'total_users': total_users,
        'active_users': active_users,
        'admin_users': admin_users,
        'avg_score': round(avg_score, 1),
        'recent_users': recent_users,
        'top_performers': top_performers
    }
    
    return render_template('admin/dashboard.html', stats=stats)

@admin_bp.route('/users')
@login_required
@admin_required
def manage_users():
    """User management page."""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    
    query = User.query
    
    if search:
        # Use simple Python filtering instead of SQL contains
        all_users = User.query.all()
        filtered_users = [
            user for user in all_users 
            if (search.lower() in user.username.lower() or 
                search.lower() in user.email.lower() or 
                search.lower() in user.full_name.lower())
        ]
        # Sort by created_at (newest first)
        filtered_users = sorted(filtered_users, key=lambda x: x.created_at, reverse=True)
        
        # Simple pagination simulation
        per_page = 20
        start = (page - 1) * per_page
        end = start + per_page
        items = filtered_users[start:end]
        total = len(filtered_users)
        
        # Create simple pagination object
        users = type('Pagination', (), {
            'items': items,
            'total': total,
            'pages': (total + per_page - 1) // per_page,
            'page': page,
            'has_prev': page > 1,
            'has_next': page < (total + per_page - 1) // per_page,
            'prev_num': page - 1 if page > 1 else None,
            'next_num': page + 1 if page < (total + per_page - 1) // per_page else None,
            'iter_pages': lambda: range(1, min(total // per_page + 2, 11))
        })()
    else:
        # Get all users and sort manually
        all_users = User.query.all()
        sorted_users = sorted(all_users, key=lambda x: x.created_at, reverse=True)
        
        # Simple pagination
        per_page = 20
        start = (page - 1) * per_page
        end = start + per_page
        items = sorted_users[start:end]
        total = len(sorted_users)
        
        users = type('Pagination', (), {
            'items': items,
            'total': total,
            'pages': (total + per_page - 1) // per_page,
            'page': page,
            'has_prev': page > 1,
            'has_next': page < (total + per_page - 1) // per_page,
            'prev_num': page - 1 if page > 1 else None,
            'next_num': page + 1 if page < (total + per_page - 1) // per_page else None,
            'iter_pages': lambda: range(1, min(total // per_page + 2, 11))
        })()
    
    return render_template('admin/users.html', users=users, search=search)

@admin_bp.route('/users/<int:user_id>')
@login_required
@admin_required
def view_user(user_id):
    """View detailed user information."""
    user = User.query.get_or_404(user_id)
    
    # Parse JSON fields
    completed_levels = json.loads(user.completed_levels) if user.completed_levels else []
    achievements = json.loads(user.achievements) if user.achievements else []
    
    user_data = {
        'user': user,
        'completed_levels': completed_levels,
        'achievements': achievements,
        'levels_completed_count': len(completed_levels),
        'achievements_count': len(achievements)
    }
    
    return render_template('admin/user_detail.html', **user_data)

@admin_bp.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    """Edit user information."""
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        # Update user fields with proper type conversion
        user.username = request.form.get('username', user.username)
        user.email = request.form.get('email', user.email)
        user.full_name = request.form.get('full_name', user.full_name)
        
        # Safe integer conversion
        try:
            user.current_level = int(request.form.get('current_level') or user.current_level)
        except (ValueError, TypeError):
            user.current_level = user.current_level
            
        try:
            user.total_score = int(request.form.get('total_score') or user.total_score)
        except (ValueError, TypeError):
            user.total_score = user.total_score
            
        try:
            user.streak_count = int(request.form.get('streak_count') or user.streak_count)
        except (ValueError, TypeError):
            user.streak_count = user.streak_count
        
        # Handle boolean fields
        user.is_active_user = 'is_active_user' in request.form
        user.email_verified = 'email_verified' in request.form
        user.is_admin = 'is_admin' in request.form
        
        # Handle password change
        new_password = request.form.get('new_password')
        if new_password:
            user.set_password(new_password)
        
        try:
            db.session.commit()
            flash(f'User {user.username} updated successfully.', 'success')
            return redirect(url_for('admin.view_user', user_id=user.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating user: {str(e)}', 'error')
    
    return render_template('admin/edit_user.html', user=user)

@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    """Delete a user."""
    user = User.query.get_or_404(user_id)
    
    # Prevent deleting yourself
    if user.id == current_user.id:
        flash('You cannot delete your own account.', 'error')
        return redirect(url_for('admin.manage_users'))
    
    try:
        username = user.username
        db.session.delete(user)
        db.session.commit()
        flash(f'User {username} deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting user: {str(e)}', 'error')
    
    return redirect(url_for('admin.manage_users'))

@admin_bp.route('/users/<int:user_id>/reset-progress', methods=['POST'])
@login_required
@admin_required
def reset_user_progress(user_id):
    """Reset user's game progress."""
    user = User.query.get_or_404(user_id)
    
    try:
        user.current_level = 1
        user.total_score = 0
        user.completed_levels = '[]'
        user.achievements = '[]'
        user.streak_count = 0
        
        db.session.commit()
        flash(f'Progress reset for user {user.username}.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error resetting progress: {str(e)}', 'error')
    
    return redirect(url_for('admin.view_user', user_id=user.id))

@admin_bp.route('/scores')
@login_required
@admin_required
def manage_scores():
    """Score management and leaderboard."""
    # Get top scores using Python sorting
    all_users = User.query.all()
    top_scores = sorted([u for u in all_users if u.total_score > 0], key=lambda x: x.total_score, reverse=True)[:50]
    
    # Get level completion statistics
    level_stats = {}
    for user in all_users:
        completed = json.loads(user.completed_levels) if user.completed_levels else []
        for level in completed:
            level_stats[level] = level_stats.get(level, 0) + 1
    
    return render_template('admin/scores.html', top_scores=top_scores, level_stats=level_stats)

@admin_bp.route('/content')
@login_required
@admin_required
def manage_content():
    """Content management for questions and tests."""
    # Get questions count per level
    level_questions = {}
    
    # This would need to be implemented based on your question storage system
    # For now, we'll use placeholder data
    for level in range(1, 21):
        # Create a dummy player object to get level data
        dummy_player = create_dummy_player(level)
        level_data = game_logic.get_level_data(level, dummy_player)
        if level_data:
            level_questions[level] = len(level_data.get('questions', []))
    
    return render_template('admin/content.html', level_questions=level_questions)

@admin_bp.route('/content/level/<int:level>')
@login_required
@admin_required
def manage_level_content(level):
    """Manage content for a specific level."""
    # Create a dummy player object to get level data
    dummy_player = create_dummy_player(level)
    level_data = game_logic.get_level_data(level, dummy_player)
    questions = level_data.get('questions', []) if level_data else []
    
    return render_template('admin/level_content.html', level=level, questions=questions, level_data=level_data)

@admin_bp.route('/content/level/<int:level>/add-question', methods=['GET', 'POST'])
@login_required
@admin_required
def add_question(level):
    """Add a new question to a level."""
    if request.method == 'POST':
        # This would need to be implemented based on your question storage system
        question_data = {
            'question': request.form.get('question'),
            'answer': request.form.get('answer'),
            'hint': request.form.get('hint'),
            'difficulty': request.form.get('difficulty'),
            'points': int(request.form.get('points', 10))
        }
        
        # Save question logic would go here
        flash(f'Question added to Level {level}.', 'success')
        return redirect(url_for('admin.manage_level_content', level=level))
    
    return render_template('admin/add_question.html', level=level)

@admin_bp.route('/api/users/<int:user_id>/toggle-status', methods=['POST'])
@login_required
@admin_required
def toggle_user_status(user_id):
    """API endpoint to toggle user active status."""
    user = User.query.get_or_404(user_id)
    
    try:
        user.is_active_user = not user.is_active_user
        db.session.commit()
        
        return jsonify({
            'success': True,
            'is_active': user.is_active_user,
            'message': f'User {user.username} {"activated" if user.is_active_user else "deactivated"}.'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error updating user status: {str(e)}'
        }), 500

@admin_bp.route('/api/users/<int:user_id>/toggle-admin', methods=['POST'])
@login_required
@admin_required
def toggle_admin_status(user_id):
    """API endpoint to toggle user admin status."""
    user = User.query.get_or_404(user_id)
    
    # Prevent removing admin from yourself
    if user.id == current_user.id and user.is_admin:
        return jsonify({
            'success': False,
            'message': 'You cannot remove admin privileges from yourself.'
        }), 400
    
    try:
        user.is_admin = not user.is_admin
        db.session.commit()
        
        return jsonify({
            'success': True,
            'is_admin': user.is_admin,
            'message': f'Admin privileges {"granted to" if user.is_admin else "removed from"} {user.username}.'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error updating admin status: {str(e)}'
        }), 500

@admin_bp.route('/system')
@login_required
@admin_required
def system_info():
    """System information and settings."""
    # Database statistics
    db_stats = {
        'users_table_size': User.query.count(),
        'database_file': 'python_learning.db',  # Adjust based on your setup
    }
    
    # Recent activity
    all_users = User.query.all()
    recent_activity = sorted([u for u in all_users if u.last_activity], key=lambda x: x.last_activity, reverse=True)[:10]
    
    return render_template('admin/system.html', db_stats=db_stats, recent_activity=recent_activity)
