from flask import render_template

import global_vars


def process(page):
    if page is not None:
        return render_template('page/content.html', page=page, global_vars=global_vars)