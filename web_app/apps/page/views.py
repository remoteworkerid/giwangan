from flask import render_template
from flask_login import current_user
from flask_security import AnonymousUser

import global_vars
from models import db, Page, User


def process(page):
    if page is not None:
        # TODO: dump this to celery for updating
        if current_user is not None:
            if not current_user.has_role('admin'):
                page.view_count += 1
                db.session.query(Page).filter_by(id=page.id).update({"view_count": page.view_count})
                db.session.commit()

        return render_template('page/content.html', page=page, global_vars=global_vars)

def get_og(page):
    og = {}
    if page is not None:
        # Open graph for facebook
        og['url'] = '{}/{}'.format('http://nezzmedia.com', page.url)
        og['type'] = "article"
        og['title'] = page.title
        og['description'] = page.excerpt
        if page.feature_image is not None:
            og['image'] = 'http://nezzmedia.com/static/upload/{}'.format(page.feature_image.path)
        else:
            og['image'] = 'http://nezzmedia.com/static/favicon.ico'
        return og

def get_love(page):
    if current_user and current_user.is_authenticated:
        user = User.query.join(User.loves).filter(User.id == current_user.id, Page.id == page.id).first()
        if user is not None:
            return True
        else:
            return False

    return False