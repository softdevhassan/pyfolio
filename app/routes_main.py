from flask import Blueprint, render_template
from app.models import SiteSettings, Project, Service

main = Blueprint('main', __name__)

@main.route('/')
def index():
    settings = SiteSettings.query.first()
    projects = Project.query.order_by(Project.order.asc()).limit(4).all()
    services = Service.query.order_by(Service.order.asc()).all()
    return render_template('public/index.html', settings=settings, projects=projects, services=services)

@main.route('/about')
def about():
    settings = SiteSettings.query.first()
    return render_template('public/about.html', settings=settings)

@main.route('/services')
def services():
    settings = SiteSettings.query.first()
    services = Service.query.order_by(Service.order.asc()).all()
    return render_template('public/services.html', settings=settings, services=services)

@main.route('/portfolio')
def portfolio():
    settings = SiteSettings.query.first()
    projects = Project.query.order_by(Project.order.asc()).all()
    return render_template('public/portfolio.html', settings=settings, projects=projects)

@main.route('/contact')
def contact():
    settings = SiteSettings.query.first()
    return render_template('public/contact.html', settings=settings)
