"""
Authentication routes and handlers
Handles login, signup, logout, password reset, and profile management
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from auth import User, db
from forms import LoginForm, SignupForm, ForgotPasswordForm, ResetPasswordForm, ChangePasswordForm, ProfileForm
from datetime import datetime
import json

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login page and handler."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        username_or_email = form.username_or_email.data
        password = form.password.data
        remember = form.remember_me.data
        
        # Check if input is email or username (with null and empty check)
        if username_or_email and '@' in username_or_email:
            user = User.query.filter_by(email=username_or_email).first()
        elif username_or_email:
            user = User.query.filter_by(username=username_or_email).first()
        else:
            user = None
        
        if user and user.check_password(password):
            if not user.is_active_user:
                flash('Your account has been deactivated. Please contact support.', 'error')
                return render_template('auth/login.html', form=form)
            
            login_user(user, remember=remember)
            user.update_last_login()
            
            flash(f'Welcome back, {user.full_name}!', 'success')
            
            # Redirect to next page or home
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid username/email or password. Please try again.', 'error')
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """Signup page and handler."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = SignupForm()
    
    if form.validate_on_submit():
        try:
            # Create new user
            user = User(
                username=form.username.data,
                email=form.email.data,
                full_name=form.full_name.data
            )
            user.set_password(form.password.data)
            
            db.session.add(user)
            db.session.commit()
            
            # Log in the new user
            login_user(user)
            user.update_last_login()
            
            flash(f'Welcome to Python Learning Adventure, {user.full_name}! Your account has been created successfully.', 'success')
            return redirect(url_for('main.dashboard'))
            
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration. Please try again.', 'error')
            print(f"Registration error: {e}")
    
    return render_template('auth/signup.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    """Logout handler."""
    username = current_user.username
    logout_user()
    flash(f'You have been logged out successfully, {username}.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Forgot password page and handler."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = ForgotPasswordForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user:
            token = user.generate_reset_token()
            
            # In a real app, you would send an email here
            # For now, we'll just show the reset link
            reset_url = url_for('auth.reset_password', token=token, _external=True)
            
            flash(f'Password reset instructions have been sent to {user.email}. '
                  f'For demo purposes, your reset link is: {reset_url}', 'info')
        else:
            flash('If an account with that email exists, you will receive password reset instructions.', 'info')
        
        return redirect(url_for('auth.login'))
    
    return render_template('auth/forgot_password.html', form=form)

@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Reset password with token."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    user = User.query.filter_by(reset_token=token).first()
    
    if not user or not user.verify_reset_token(token):
        flash('Invalid or expired reset token. Please request a new one.', 'error')
        return redirect(url_for('auth.forgot_password'))
    
    form = ResetPasswordForm()
    
    if form.validate_on_submit():
        user.set_password(form.password.data)
        user.clear_reset_token()
        
        flash('Your password has been reset successfully. You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password.html', form=form)

@auth_bp.route('/profile')
@login_required
def profile():
    """User profile page."""
    return render_template('auth/profile.html', user=current_user)

@auth_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Edit user profile."""
    form = ProfileForm(current_user.email)
    
    if form.validate_on_submit():
        current_user.full_name = form.full_name.data
        current_user.email = form.email.data
        
        db.session.commit()
        flash('Your profile has been updated successfully.', 'success')
        return redirect(url_for('auth.profile'))
    
    elif request.method == 'GET':
        form.full_name.data = current_user.full_name
        form.email.data = current_user.email
    
    return render_template('auth/edit_profile.html', form=form)

@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change user password."""
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        if current_user.check_password(form.current_password.data):
            current_user.set_password(form.new_password.data)
            db.session.commit()
            
            flash('Your password has been changed successfully.', 'success')
            return redirect(url_for('auth.profile'))
        else:
            flash('Current password is incorrect.', 'error')
    
    return render_template('auth/change_password.html', form=form)

@auth_bp.route('/api/check-username')
def check_username():
    """API endpoint to check username availability."""
    username = request.args.get('username', '').strip()
    
    if not username:
        return jsonify({'available': False, 'message': 'Username is required'})
    
    if len(username) < 3:
        return jsonify({'available': False, 'message': 'Username must be at least 3 characters'})
    
    user = User.query.filter_by(username=username).first()
    
    if user:
        return jsonify({'available': False, 'message': 'Username is already taken'})
    
    return jsonify({'available': True, 'message': 'Username is available'})

@auth_bp.route('/api/check-email')
def check_email():
    """API endpoint to check email availability."""
    email = request.args.get('email', '').strip()
    
    if not email:
        return jsonify({'available': False, 'message': 'Email is required'})
    
    user = User.query.filter_by(email=email).first()
    
    if user:
        return jsonify({'available': False, 'message': 'Email is already registered'})
    
    return jsonify({'available': True, 'message': 'Email is available'})
