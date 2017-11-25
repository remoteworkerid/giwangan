from flask import Flask, render_template
from flask_admin import Admin

from web_app.models import db, Page, Menu
from web_app.views import PageModelView, MenuModelView
from sqlalchemy import func

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')
    db.init_app(app)

    admin = Admin(app, name=app.config['TITLE'], template_mode='bootstrap3')
    admin.add_view(PageModelView(Page, db.session))
    admin.add_view(MenuModelView(Menu, db.session))

    @app.route('/')
    @app.route('/<uri>')
    def index(uri=None):
        if uri is None:
            page = Page.query.filter_by(is_homepage=True).first()
        else:
            page = Page.query.filter(func.lower(Page.title) == uri.lower()).first()
        menus = Menu.query.order_by('order')

        content = ''
        if page is not None:
            content = page.content
        return render_template('index.html', TITLE=app.config['TITLE'],
                               TAGLINE=app.config['TAGLINE'], body=content, menus=menus)


    return app