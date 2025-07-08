"""
Authentication and User Management Module
Handles user registration, login, password hashing, and session management
"""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin, LoginManager
from datetime import datetime, timedelta
import secrets
import os

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # type: ignore
login_manager.login_message = 'Please log in to access the Python Learning Adventure.'
login_manager.login_message_category = 'info'

class User(UserMixin, db.Model):
    """User model for authentication and profile management."""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    
    # Profile information
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active_user = db.Column(db.Boolean, default=True)  # Renamed to avoid conflict
    email_verified = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)  # Admin role
    
    # Game progress (migrated from player_manager)
    current_level = db.Column(db.Integer, default=1)
    total_score = db.Column(db.Integer, default=0)
    completed_levels = db.Column(db.Text, default='[]')  # JSON string
    achievements = db.Column(db.Text, default='[]')  # JSON string
    streak_count = db.Column(db.Integer, default=0)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Password reset
    reset_token = db.Column(db.String(100), unique=True)
    reset_token_expiry = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def __init__(self, username, email, full_name, **kwargs):
        """Initialize a new User."""
        self.username = username
        self.email = email
        self.full_name = full_name
        
        # Set default values
        self.created_at = datetime.utcnow()
        self.last_activity = datetime.utcnow()
        self.current_level = 1
        self.total_score = 0
        self.completed_levels = '[]'
        self.achievements = '[]'
        self.streak_count = 0
        self.is_active_user = True
        self.email_verified = False
        
        # Apply any additional kwargs
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def set_password(self, password):
        """Hash and set password."""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        """Check if provided password matches hash."""
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def update_last_login(self):
        """Update last login timestamp."""
        self.last_login = datetime.utcnow()
        db.session.commit()
    
    def generate_reset_token(self):
        """Generate a secure reset token."""
        self.reset_token = secrets.token_urlsafe(50)
        self.reset_token_expiry = datetime.utcnow() + timedelta(hours=1)
        db.session.commit()
        return self.reset_token
    
    def verify_reset_token(self, token):
        """Verify reset token is valid and not expired."""
        if not self.reset_token or not self.reset_token_expiry:
            return False
        
        if datetime.utcnow() > self.reset_token_expiry:
            return False
        
        return self.reset_token == token
    
    def clear_reset_token(self):
        """Clear reset token after use."""
        self.reset_token = None
        self.reset_token_expiry = None
        db.session.commit()
    
    def get_game_progress(self):
        """Get user's game progress as dict."""
        import json
        completed_levels = json.loads(self.completed_levels or '[]')
        
        # Calculate level stars (3 stars per completed level for now)
        level_stars = {}
        for level_id in completed_levels:
            level_stars[str(level_id)] = 3  # Default to 3 stars per level
        
        return {
            'id': self.id,
            'name': self.full_name,
            'username': self.username,
            'current_level': self.current_level,
            'total_score': self.total_score,
            'completed_levels': completed_levels,
            'achievements': json.loads(self.achievements or '[]'),
            'streak_count': self.streak_count,
            'last_activity': self.last_activity,
            'level_stars': level_stars
        }
    
    def get_player_object(self):
        """Get user's game progress as PlayerWrapper object for game_logic compatibility."""
        return PlayerWrapper(self.get_game_progress())
    
    def update_game_progress(self, level=None, score=None, achievements=None, streak=None):
        """Update user's game progress."""
        import json
        
        if level is not None:
            self.current_level = max(self.current_level, level)
            
            # Update completed levels
            completed = json.loads(self.completed_levels or '[]')
            if level not in completed:
                completed.append(level)
                self.completed_levels = json.dumps(completed)
        
        if score is not None:
            self.total_score += score
        
        if achievements is not None:
            current_achievements = json.loads(self.achievements or '[]')
            for achievement in achievements:
                if achievement not in current_achievements:
                    current_achievements.append(achievement)
            self.achievements = json.dumps(current_achievements)
        
        if streak is not None:
            self.streak_count = streak
        
        self.last_activity = datetime.utcnow()
        db.session.commit()
    
    # Override Flask-Login's is_active method
    def is_active(self) -> bool:  # type: ignore
        """Flask-Login property for user active status."""
        return bool(self.is_active_user)

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login."""
    return User.query.get(int(user_id))

def create_database_tables(app):
    """Create database tables if they don't exist."""
    with app.app_context():
        db.create_all()
        
        # Create a default admin user if none exists
        if not User.query.first():
            admin = User(
                username='admin',
                email='admin@pythonlearning.com',
                full_name='Administrator'
            )
            admin.set_password('admin123')
            admin.email_verified = True
            admin.is_active_user = True
            admin.is_admin = True
            
            db.session.add(admin)
            db.session.commit()
            print("Created default admin user (username: admin, password: admin123)")

class PlayerWrapper:
    """Wrapper class to convert user progress dict to object with attributes for game_logic compatibility."""
    
    def __init__(self, progress_dict):
        """Initialize wrapper from progress dictionary."""
        self.id = progress_dict.get('id')
        self.name = progress_dict.get('name')
        self.username = progress_dict.get('username')
        self.current_level = progress_dict.get('current_level', 1)
        self.total_score = progress_dict.get('total_score', 0)
        self.completed_levels = progress_dict.get('completed_levels', [])
        self.achievements = progress_dict.get('achievements', [])
        self.streak_count = progress_dict.get('streak_count', 0)
        self.last_activity = progress_dict.get('last_activity')
        
        # Additional attributes that game_logic might expect
        self.level_stars = {}  # Level ID -> stars earned
        
        # Calculate level stars based on completed levels (assuming 3 stars per level)
        for level_id in self.completed_levels:
            self.level_stars[str(level_id)] = 3  # Default to 3 stars
    
    def to_dict(self):
        """Convert back to dictionary format."""
        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'current_level': self.current_level,
            'total_score': self.total_score,
            'completed_levels': self.completed_levels,
            'achievements': self.achievements,
            'streak_count': self.streak_count,
            'last_activity': self.last_activity
        }
