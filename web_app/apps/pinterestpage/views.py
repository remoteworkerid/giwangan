from flask import render_template, json

from models import Page


def process(page):
    data = json.loads(page.subtype_data)

    if data['show_post']:
        if 'tag' in data and data['tag']:
            posts = Page.query.filter(Page.tag.contains(data['tag'])).all()
        elif 'category' in data and data['category']:
            posts = Page.query.filter(Page.category == data['category']).all()
    return render_template('pinterestpage/content.html', posts=posts)