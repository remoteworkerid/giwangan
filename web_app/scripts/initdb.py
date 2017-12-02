import os
import sys
sys.path.append(os.getcwd() + "/web_app/")

from app import create_app
from models import User, db, Role, SiteConfiguration, Page, Menu

app = create_app()

with app.app_context():
    admin_role = Role()
    admin_role.name = 'admin'
    db.session.add(admin_role)

    root = User()
    root.email = 'swdev.bali@gmail.com'
    root.active = True
    root.password = '123456'
    root.roles.append(admin_role)
    db.session.add(root)

    site = SiteConfiguration()
    site.name = 'NezzMedia'
    site.tagline = 'Days of Fun from All Over The World'
    site.show_registration_menu = True
    site.youtube_link = 'https://www.youtube.com/user/swdevbali/'
    db.session.add(site)

    page = Page()
    page.title = "Homepage"
    page.subtype = 'page'
    page.content = \
    '''
    <h1>Welcome to Giwangan CMS!</h1>
    <p>Could you please edit me? It will be a shame if the world find out that you are too lazy to edit the homepage 
    of your own wesbite :)</p>    
    '''
    db.session.add(page)

    gaming_page = Page()
    gaming_page.title = "Gaming"
    gaming_page.subtype = 'pinterestpage'
    gaming_page.is_homepage = True
    gaming_page.content = \
        '''
        Pinterest like is here
        '''
    db.session.add(gaming_page)
    db.session.commit()

    menu = Menu()
    menu.title = 'Gaming'
    menu.page_id = gaming_page.id #NOTE: As it refer to gaming_page.id, we need to commit gaming_page first
    menu.order = 1
    db.session.add(menu)
    db.session.commit()

