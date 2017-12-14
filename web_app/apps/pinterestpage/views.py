from _operator import and_

from flask import render_template, json
from models import Page, db, PageState
import global_vars


def process(page):
    data = json.loads(page.subtype_data)

    if data['show_post']:
        global_vars.ACTIVE_MENU = page.title
        if 'tag' in data and data['tag']: # tag with feature, will be in homepage
            print('here')
            posts = db.session.query(Page).join(PageState).\
                filter(PageState.title == 'Published',
                       Page.tag.contains(data['tag']),
                       Page.subtype == 'page',
                       Page.is_protected == False,
                       )\
                .order_by(Page.stamp.desc()).all()
            print('look!')
            for p in posts:
                print(p.password)

        elif 'category' in data and data['category']: # while 'category' will contains post for that category
            print('here2')
            posts = db.session.query(Page).join(PageState).\
                filter(PageState.title=='Published',
                       Page.category == data['category'],
                       Page.subtype == 'page',
                       Page.password is not None).\
                order_by(Page.stamp.desc()).all()
    return render_template('pinterestpage/content.html', posts=posts, global_vars=global_vars)

def get_og(page):
    return None

def get_love(page):
    return False