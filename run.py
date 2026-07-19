from app import create_app, db
from app.models import User, SiteSettings, Project, Service

app = create_app()

@app.cli.command("init-db")
def init_db():
    with app.app_context():
        db.create_all()
        
        # Admin
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin')
            admin.set_password('admin')
            db.session.add(admin)
            
        # Settings
        if not SiteSettings.query.first():
            settings = SiteSettings(
                name="Hassan Ali",
                role="SaaS Architect & Full-Stack Developer",
                location="Sargodha, Pakistan 🇵🇰",
                about_text="Building SaaS platforms used in production every day.",
                email="softdevhassan@gmail.com",
                github_url="https://github.com/softdevhassan",
                linkedin_url="https://www.linkedin.com/in/softdevhassan/",
                whatsapp="923277133082"
            )
            db.session.add(settings)
            
        # Seed Projects
        if Project.query.count() == 0:
            projects_data = [
                {"title": "Accounting + Logistics SaaS", "desc": "20+ users, 24K+ logistics entries, 11K+ transactions in 3 months — running 24/7", "stack": "PHP, Laravel, MySQL", "url": "", "order": 1},
                {"title": "Bulk Email SaaS", "desc": "Handles 10M+ emails/month in parallel with crypto payment gateway", "stack": "Laravel, Node.js, PostgreSQL", "url": "", "order": 2},
                {"title": "Restaurant Management System", "desc": "Multi-tenant RBAC system with Admin, Manager, Waiter & Chef portals", "stack": "Laravel, MySQL", "url": "", "order": 3},
                {"title": "AI Automation System", "desc": "Competitor ads analysis + appointment calling — n8n, Make.com, OpenAI", "stack": "n8n, OpenAI API, VAPI AI", "url": "", "order": 4},
                {"title": "ScanSoles Frontend", "desc": "Swiss AI health-tech startup — orthotics platform for international B2B market", "stack": "Next.js, React, Tailwind", "url": "https://scansoles.com", "order": 5},
                {"title": "Entify — NLP Research Platform", "desc": "Comparative NER: CRF (90.32% F1) vs spaCy neural — trained on CoNLL2003", "stack": "Python, Flask, AWS EC2", "url": "https://entify.orbin.dev", "order": 6},
                {"title": "Bottleneck Agency", "desc": "Full WordPress website for a digital marketing agency", "stack": "WordPress, Elementor", "url": "https://onbottleneck.com", "order": 7},
                {"title": "Repave Ltd", "desc": "Local SEO-focused multi-service site for UK paving company", "stack": "WordPress", "url": "https://repave.co.uk", "order": 8}
            ]
            for p in projects_data:
                db.session.add(Project(title=p['title'], description=p['desc'], stack=p['stack'], live_url=p['url'], order=p['order']))
                
        # Seed Services / Categories
        if Service.query.count() == 0:
            services_data = ["Backend Development", "Frontend Development", "Database Architecture", "AI & Automation", "Infrastructure & DevOps", "CMS & E-Commerce"]
            for i, s in enumerate(services_data):
                db.session.add(Service(name=s, order=i+1))
                
        db.session.commit()
        print("Database initialized and fully seeded with projects and services!")

if __name__ == '__main__':
    app.run(debug=True)
