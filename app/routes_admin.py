from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, SiteSettings, Project, Service

admin = Blueprint('admin', __name__)

@admin.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('admin.dashboard'))
        flash('Invalid username or password', 'error')
        
    return render_template('admin/login.html')

@admin.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@admin.route('/')
@login_required
def dashboard():
    settings = SiteSettings.query.first()
    projects = Project.query.all()
    return render_template('admin/dashboard.html', settings=settings, projects=projects)

@admin.route('/settings', methods=['POST'])
@login_required
def update_settings():
    settings = SiteSettings.query.first()
    if not settings:
        settings = SiteSettings()
        db.session.add(settings)
        
    settings.name = request.form.get('name')
    settings.role = request.form.get('role')
    settings.location = request.form.get('location')
    settings.about_text = request.form.get('about_text')
    settings.email = request.form.get('email')
    settings.github_url = request.form.get('github_url')
    settings.linkedin_url = request.form.get('linkedin_url')
    settings.whatsapp = request.form.get('whatsapp')
    
    db.session.commit()
    flash('Settings updated successfully', 'success')
    return redirect(url_for('admin.dashboard'))
