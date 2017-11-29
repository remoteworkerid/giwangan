import flask_security
from flask import Flask, render_template
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import login_required
from flask_security import SQLAlchemyUserDatastore, Security
from flask_security.decorators import anonymous_user_required

from web_app import models
from web_app.models import db, Page, Menu, User, Role
from web_app.views import PageModelView, MenuModelView, UserModelView, RoleModelView, SecuredHomeView
from sqlalchemy import func


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')
    db.init_app(app)

    admin = Admin(app, name=app.config['TITLE'], template_mode='bootstrap3', index_view=SecuredHomeView(url='/admin'))

    admin.add_view(PageModelView(Page, db.session))
    admin.add_view(MenuModelView(Menu, db.session))
    admin.add_view(UserModelView(User, db.session))
    admin.add_view(RoleModelView(Role, db.session))

    user_datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
    security = Security(app, user_datastore)

    @app.route('/')
    @app.route('/<uri>')
    def index(uri=None):
        if uri is None:
            page = Page.query.filter_by(is_homepage=True).first()
        else:
            page = Page.query.filter(func.lower(Page.title) == uri.lower()).first()
        menus = Menu.query.order_by('order')

        content = 'empty page content'
        if page is not None:
            content = page.content
        return render_template('index.html', TITLE=app.config['TITLE'],
                               TAGLINE=app.config['TAGLINE'], content=content, menus=menus)

    @app.route('/register', methods=['GET', 'POST'])
    @anonymous_user_required
    def register():
        return flask_security.views.register()

    @app.route('/sec')
    @login_required
    def sec():
        return 'congrats!'

    return app
