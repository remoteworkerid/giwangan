import os
import sys
sys.path.append(os.getcwd() + "/web_app/")

from app import create_app
from models import User, db, Role, SiteConfiguration

app = create_app()

with app.app_context():
    role = Role()
    role.name = 'admin'
    db.session.add(role)

    root = User()
    root.email = 'swdev.bali@gmail.com'
    root.active = True
    root.password = '123456'
    root.roles.append(role)

    db.session.add(root)

    site = SiteConfiguration()
    site.name = 'Pythonthusiast'
    site.tagline = 'Remote Work Mentoring'

    db.session.add(site)
    db.session.commit()
