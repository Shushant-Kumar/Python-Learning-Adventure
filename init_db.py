#!/usr/bin/env python3
"""
Database initialization script
Creates the database with correct schema and admin user
"""

from app import app
from auth import db, User

def init_database():
    """Initialize the database with correct schema and default admin user."""
    with app.app_context():
        # Drop all tables if they exist (clean slate)
        db.drop_all()
        print("Dropped existing tables")
        
        # Create all tables with current schema
        db.create_all()
        print("Created database tables with current schema")
        
        # Create default admin user if needed
        if not User.query.first():
            admin = User(
                username='admin',
                email='admin@pythonlearning.com',
                full_name='Administrator'
            )
            admin.set_password('admin123')
            admin.email_verified = True
            admin.is_active_user = True
            admin.is_admin = True  # Set admin flag
            
            db.session.add(admin)
            
            # Create a test user for demonstration
            test_user = User(
                username='testuser',
                email='test@pythonlearning.com',
                full_name='Test User'
            )
            test_user.set_password('test123')
            test_user.email_verified = True
            test_user.is_active_user = True
            test_user.current_level = 3
            test_user.total_score = 75
            
            db.session.add(test_user)
            
            db.session.commit()
            print("Created default admin user (username: admin, password: admin123)")
            print("Created test user (username: testuser, password: test123)")
        else:
            print("Users already exist in database")
        
        print("Database initialization completed successfully!")

if __name__ == '__main__':
    init_database()
