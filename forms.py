"""
WTForms for authentication and user management
Handles form validation for login, signup, and password reset
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from auth import User

class LoginForm(FlaskForm):
    """User login form."""
    
    username_or_email = StringField(
        'Username or Email',
        validators=[DataRequired(), Length(min=3, max=80)],
        render_kw={'placeholder': 'Enter your username or email'}
    )
    
    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=6)],
        render_kw={'placeholder': 'Enter your password'}
    )
    
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    """User registration form."""
    
    full_name = StringField(
        'Full Name',
        validators=[DataRequired(), Length(min=2, max=100)],
        render_kw={'placeholder': 'Enter your full name'}
    )
    
    username = StringField(
        'Username',
        validators=[DataRequired(), Length(min=3, max=80)],
        render_kw={'placeholder': 'Choose a username'}
    )
    
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()],
        render_kw={'placeholder': 'Enter your email address'}
    )
    
    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=6)],
        render_kw={'placeholder': 'Create a password (min 6 characters)'}
    )
    
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match')
        ],
        render_kw={'placeholder': 'Confirm your password'}
    )
    
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        """Check if username is already taken."""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken. Please choose a different one.')
    
    def validate_email(self, email):
        """Check if email is already registered."""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different email or login.')

class ForgotPasswordForm(FlaskForm):
    """Forgot password form."""
    
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()],
        render_kw={'placeholder': 'Enter your registered email'}
    )
    
    submit = SubmitField('Send Reset Link')

class ResetPasswordForm(FlaskForm):
    """Reset password form."""
    
    password = PasswordField(
        'New Password',
        validators=[DataRequired(), Length(min=6)],
        render_kw={'placeholder': 'Enter new password (min 6 characters)'}
    )
    
    confirm_password = PasswordField(
        'Confirm New Password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match')
        ],
        render_kw={'placeholder': 'Confirm new password'}
    )
    
    submit = SubmitField('Reset Password')

class ChangePasswordForm(FlaskForm):
    """Change password form for logged-in users."""
    
    current_password = PasswordField(
        'Current Password',
        validators=[DataRequired()],
        render_kw={'placeholder': 'Enter current password'}
    )
    
    new_password = PasswordField(
        'New Password',
        validators=[DataRequired(), Length(min=6)],
        render_kw={'placeholder': 'Enter new password (min 6 characters)'}
    )
    
    confirm_password = PasswordField(
        'Confirm New Password',
        validators=[
            DataRequired(),
            EqualTo('new_password', message='Passwords must match')
        ],
        render_kw={'placeholder': 'Confirm new password'}
    )
    
    submit = SubmitField('Change Password')

class ProfileForm(FlaskForm):
    """User profile update form."""
    
    full_name = StringField(
        'Full Name',
        validators=[DataRequired(), Length(min=2, max=100)],
        render_kw={'placeholder': 'Enter your full name'}
    )
    
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()],
        render_kw={'placeholder': 'Enter your email address'}
    )
    
    submit = SubmitField('Update Profile')
    
    def __init__(self, original_email, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.original_email = original_email
    
    def validate_email(self, email):
        """Check if email is already registered (excluding current user)."""
        if email.data != self.original_email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already registered. Please use a different email.')
