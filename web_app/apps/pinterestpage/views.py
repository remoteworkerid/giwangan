from flask import render_template


def process(page):
    content = 'empty page content'
    if page is not None:
        content = page.content

    return render_template('pinterestpage/content.html')