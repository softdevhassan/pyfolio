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
        
    settings = SiteSettings.query.first()
    return render_template('admin/login.html', settings=settings)

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
    services = Service.query.all()
    return render_template('admin/dashboard.html', settings=settings, projects=projects, services=services)

@admin.route('/settings', methods=['GET', 'POST'])
@login_required
def settings_form():
    settings = SiteSettings.query.first()
    if request.method == 'POST':
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
        return redirect(url_for('admin.settings_form'))
        
    return render_template('admin/settings.html', settings=settings)

# ==========================================
# PROJECTS CRUD
# ==========================================

@admin.route('/projects')
@login_required
def projects_index():
    projects = Project.query.order_by(Project.order).all()
    return render_template('admin/projects_index.html', projects=projects)

@admin.route('/projects/create', methods=['GET', 'POST'])
@login_required
def projects_create():
    if request.method == 'POST':
        project = Project(
            title=request.form.get('title'),
            description=request.form.get('description'),
            stack=request.form.get('stack'),
            live_url=request.form.get('live_url'),
            order=request.form.get('order', 0, type=int)
        )
        db.session.add(project)
        db.session.commit()
        flash('Project created successfully', 'success')
        return redirect(url_for('admin.projects_index'))
        
    return render_template('admin/projects_form.html', project=None)

@admin.route('/projects/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def projects_edit(id):
    project = db.session.get(Project, id)
    if not project:
        flash('Project not found', 'error')
        return redirect(url_for('admin.projects_index'))
        
    if request.method == 'POST':
        project.title = request.form.get('title')
        project.description = request.form.get('description')
        project.stack = request.form.get('stack')
        project.live_url = request.form.get('live_url')
        project.order = request.form.get('order', 0, type=int)
        
        db.session.commit()
        flash('Project updated successfully', 'success')
        return redirect(url_for('admin.projects_index'))
        
    return render_template('admin/projects_form.html', project=project)

@admin.route('/projects/<int:id>/delete', methods=['POST'])
@login_required
def projects_delete(id):
    project = db.session.get(Project, id)
    if project:
        db.session.delete(project)
        db.session.commit()
        flash('Project deleted successfully', 'success')
    return redirect(url_for('admin.projects_index'))

# ==========================================
# SERVICES CRUD
# ==========================================

@admin.route('/services')
@login_required
def services_index():
    services = Service.query.order_by(Service.order).all()
    return render_template('admin/services_index.html', services=services)

@admin.route('/services/create', methods=['GET', 'POST'])
@login_required
def services_create():
    if request.method == 'POST':
        service = Service(
            name=request.form.get('name'),
            order=request.form.get('order', 0, type=int)
        )
        db.session.add(service)
        db.session.commit()
        flash('Service created successfully', 'success')
        return redirect(url_for('admin.services_index'))
        
    return render_template('admin/services_form.html', service=None)

@admin.route('/services/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def services_edit(id):
    service = db.session.get(Service, id)
    if not service:
        flash('Service not found', 'error')
        return redirect(url_for('admin.services_index'))
        
    if request.method == 'POST':
        service.name = request.form.get('name')
        service.order = request.form.get('order', 0, type=int)
        
        db.session.commit()
        flash('Service updated successfully', 'success')
        return redirect(url_for('admin.services_index'))
        
    return render_template('admin/services_form.html', service=service)

@admin.route('/services/<int:id>/delete', methods=['POST'])
@login_required
def services_delete(id):
    service = db.session.get(Service, id)
    if service:
        db.session.delete(service)
        db.session.commit()
        flash('Service deleted successfully', 'success')
    return redirect(url_for('admin.services_index'))

# ==========================================
# SECURITY CRUD
# ==========================================

@admin.route('/security', methods=['GET', 'POST'])
@login_required
def security_update():
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        username = request.form.get('username')
        
        # Verify current password
        if not current_user.check_password(current_password):
            flash('Incorrect current password.', 'error')
            return redirect(url_for('admin.security_update'))
            
        # Update username if changed
        if username and username != current_user.username:
            # Check if username exists
            if User.query.filter_by(username=username).first():
                flash('Username already exists.', 'error')
                return redirect(url_for('admin.security_update'))
            current_user.username = username
            
        # Update password if provided
        if new_password:
            if new_password != confirm_password:
                flash('New passwords do not match.', 'error')
                return redirect(url_for('admin.security_update'))
            current_user.set_password(new_password)
            
        db.session.commit()
        flash('Security credentials updated successfully!', 'success')
        return redirect(url_for('admin.security_update'))
        
    return render_template('admin/security.html')
