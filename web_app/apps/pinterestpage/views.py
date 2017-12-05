from flask import render_template, json
from models import Page
import global_vars


def process(page):
    data = json.loads(page.subtype_data)

    if data['show_post']:
        global_vars.ACTIVE_MENU = page.title
        if 'tag' in data and data['tag']:
            posts = Page.query.filter(Page.tag.contains(data['tag'])).order_by(Page.stamp.desc()).all()
        elif 'category' in data and data['category']:
            posts = Page.query.filter(Page.category == data['category']).order_by(Page.stamp.desc()).all()
    return render_template('pinterestpage/content.html', posts=posts, global_vars=global_vars)

def get_og(page):
    return None