from flask import render_template
import global_vars


def process(page):
    if page is not None:
        return render_template('page/content.html', page=page, global_vars=global_vars)

def get_og(page):
    og = {}
    if page is not None:
        og['url'] = '{}/{}'.format('http://nezzmedia.com', page.url)
        og['type'] = "article"
        og['title'] = page.title
        og['description'] = page.excerpt
        if page.feature_image is not None:
            og['image'] = 'http://nezzmedia.com/static/upload/{}'.format(page.feature_image.path)
        else:
            og['image'] = 'http://nezzmedia.com/static/favicon.ico'
        return og