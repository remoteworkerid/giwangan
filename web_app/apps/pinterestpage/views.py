from flask import render_template, json

from web_app.models import Post


def process(page):
    data = json.loads(page.subtype_data)

    if data['show_post']:
        if data.has_key('tag') and data['tag']:
            posts = Post.query.filter(Post.tag.contains(data['tag'])).all()
        elif data.has_key('category') and data['category']:
            posts = Post.query.filter(Post.category == data['category']).all()
    return render_template('pinterestpage/content.html', posts=posts)