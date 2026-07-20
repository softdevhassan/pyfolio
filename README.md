# Personal Portfolio Platform

## 1. Planning
**Objective:** To build a dynamic, multi-page personal portfolio that highlights professional experience, technical skills, and completed projects as a SaaS Architect and Full-Stack Developer.
**Target Audience:** Recruiters, clients, and potential collaborators.
**Architecture Design:**
- **Framework:** Python Flask (chosen for its lightweight, modular architecture).
- **Frontend:** HTML5, Alpine.js (for lightweight interactivity), Tailwind CSS (for rapid, modern styling without heavy CSS files).
- **Database:** SQLite with SQLAlchemy ORM to dynamically manage projects and services.
- **Routing Strategy:** Blueprint-based routing to separate main frontend views from administrative logic.

## 2. Development
**Tech Stack Used:**
- **Backend:** Python 3, Flask, Flask-SQLAlchemy
- **Frontend:** Jinja2 Templating, Tailwind CSS, Alpine.js, jQuery
- **Version Control:** Git & GitHub

**Development Lifecycle:**
1. **Initial Setup:** Configured the virtual environment, installed Flask and dependencies (`requirements.txt`), and created the application factory (`create_app`).
2. **Database Modeling:** Designed the SQLite schema (`models.py`) with tables for `SiteSettings`, `User`, `Project`, and `Service` to avoid hardcoded content.
3. **Routing & Logic:** Implemented `routes_main.py` to handle dynamic data rendering from the database to the Jinja2 templates.
4. **UI/UX Implementation:** Built a sleek, dark-mode SaaS aesthetic using Tailwind CSS. Created modular components (`_header.html`, `_footer.html`) for maintainability.

## 3. Documentation
- **Code Organization:** The codebase follows the Flask Application Factory pattern, ensuring scalability. Templates are separated into `components` and `public` directories.
- **Configuration:** Managed via `config.py` using object-based configuration classes (e.g., `Config`, `ProductionConfig`).
- **Seeding Script:** Created a custom CLI command (`flask --app run.py init-db`) to automatically seed the database with initial profile data and projects.

## 4. Deployment (Heroku)
The application is fully prepared for cloud deployment on Heroku:
- **Procfile:** Contains `web: gunicorn run:app` to instruct Heroku on how to serve the Flask application.
- **Dependencies:** All required packages (including `gunicorn`) are frozen in `requirements.txt`.
- **Environment Management:** Designed to adapt to Heroku's ephemeral file system while serving read-only portfolio data effectively.
