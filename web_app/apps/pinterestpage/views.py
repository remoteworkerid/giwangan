from flask import render_template, json

from web_app.models import Post


def process(page):
    data = json.loads(page.subtype_data)

    if data['show_post']:
        if 'tag' in data and data['tag']:
            posts = Post.query.filter(Post.tag.contains(data['tag'])).all()
        elif 'category' in data and data['category']:
            posts = Post.query.filter(Post.category == data['category']).all()
    return render_template('pinterestpage/content.html', posts=posts)