import os
import sys

sys.path.append(os.getcwd() + "/web_app/")
from utils import readfile

from flask import json

from app import create_app
from models import User, db, Role, SiteConfiguration, Page, Menu, AdsenseType, AdsenseCode

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
    site.ga_tracking_code = 'UA-99596173-4'
    db.session.add(site)

    # HomePage should display all featured post from all category, in pinterest like
    page = Page()
    page.title = "Homepage"
    page.subtype = 'pinterestpage'
    page.subtype_data = json.dumps({'show_post': True, 'tag': 'feature', 'count': 5, 'order_by': 'date'})
    page.is_homepage = True
    db.session.add(page)

    gaming_page = Page()
    gaming_page.title = "Gaming"
    gaming_page.subtype = 'pinterestpage'
    gaming_page.subtype_data = json.dumps({'show_post': True, 'category': 'gaming', 'count': 5, 'order_by': 'date'})
    db.session.add(gaming_page)
    db.session.commit()

    menu = Menu()
    menu.title = 'Gaming'
    menu.page_id = gaming_page.id #NOTE: As it refer to gaming_page.id, we need to commit gaming_page first
    menu.order = 1
    db.session.add(menu)

    it_page = Page()
    it_page.title = "IT"
    it_page.subtype = 'pinterestpage'
    it_page.subtype_data = json.dumps({'show_post': True, 'category': 'it', 'count': 5, 'order_by': 'date'})
    db.session.add(it_page)
    db.session.commit()

    menu = Menu()
    menu.title = 'IT'
    menu.page_id = it_page.id  # NOTE: As it refer to gaming_page.id, we need to commit gaming_page first
    menu.order = 1
    db.session.add(menu)
    db.session.commit()

    # All initial posts
    post = Page()
    post.title = 'Doom VFR datang!'
    post.content = readfile(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'doomfvr.txt'))
    post.category = 'gaming'
    post.tag = 'doom,vr,feature'
    db.session.add(post)

    post = Page()
    post.title = 'Bug memalukan pada OSX Sierra'
    post.content = \
        '''
        <h1>Siapa yang salah ini?</h1>
        <p>Masa' bisa begitu saja error?</p>    
        '''
    post.category = 'it'
    post.tag = 'osx,feature'
    db.session.add(post)
    db.session.commit()

    adstype_inarticle = AdsenseType()
    adstype_inarticle.name = 'In-article'
    db.session.add(adstype_inarticle)
    db.session.commit()

    adsense = AdsenseCode()
    adsense.adstype_id = adstype_inarticle.id
    adsense.code = \
"""
<script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
<ins class="adsbygoogle"
     style="display:block; text-align:center;"
     data-ad-layout="in-article"
     data-ad-format="fluid"
     data-ad-client="ca-pub-3131828654572794"
     data-ad-slot="2968395654"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script>
"""
    db.session.add(adsense)
    db.session.commit()