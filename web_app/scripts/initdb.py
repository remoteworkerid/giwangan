import os
import sys
sys.path.append(os.getcwd() + "/web_app/")

from app import create_app
from models import User, db, Role, SiteConfiguration, Page, Menu

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
    site.show_registration_menu = False
    db.session.add(site)

    page = Page()
    page.title = "Homepage"
    page.is_homepage = True
    page.content = \
    '''
    <h1>Welcome to Giwangan CMS!</h1>
    <p>Could you please edit me? It will be a shame if the world find out that you are too lazy to edit the homepage 
    of your own wesbite :)</p>
    '''
    db.session.add(page)
    db.session.commit()
