import os
import sys
sys.path.append(os.getcwd() + "/web_app/")

import flask_security
from flask import Flask, render_template
from flask_admin import Admin
from flask_security import SQLAlchemyUserDatastore, Security
from flask_security.decorators import anonymous_user_required

import global_vars as global_vars
from models import db, Page, Menu, User, Role, SiteConfiguration, Image, AdsenseCode, AdsenseType
from views import PageModelView, MenuModelView, UserModelView, RoleModelView, SecuredHomeView, \
    SiteConfigurationView, ImageView


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')
    db.init_app(app)

    admin = Admin(app, name=app.config['TITLE'], template_mode='bootstrap3', index_view=SecuredHomeView(url='/admin'))

    admin.add_view(PageModelView(Page, db.session))
    admin.add_view(MenuModelView(Menu, db.session))
    admin.add_view(UserModelView(User, db.session))
    admin.add_view(RoleModelView(Role, db.session))
    admin.add_view(SiteConfigurationView(SiteConfiguration, db.session))
    admin.add_view(ImageView(Image, db.session))

    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)

    @app.before_first_request
    def init_vars():
        #TODO improve for multisite
        siteconfiguration = SiteConfiguration.query.filter_by(id=1).first()

        if siteconfiguration is not None:
            global_vars.SITE_NAME = siteconfiguration.name
            global_vars.SITE_TAGLINE = siteconfiguration.tagline
            global_vars.SHOW_REGISTRATION_MENU = siteconfiguration.show_registration_menu
            global_vars.YOUTUBE_LINK = siteconfiguration.youtube_link
            global_vars.GA_TRACKING_CODE = siteconfiguration.ga_tracking_code

            #page level ads
            ads = db.session.query(AdsenseCode).join(AdsenseType).filter(AdsenseType.name == 'Page-level Ads').first()
            if ads is not None:
                global_vars.ADSENSE_PAGELEVEL_CODE = ads.code

            #inapp ads
            ads = db.session.query(AdsenseCode).join(AdsenseType).filter(AdsenseType.name == 'In-article Ads').first()
            if ads is not None:
                global_vars.ADSENSE_INAPP_ARTICLE_CODE = ads.code

            # infeed
            ads = db.session.query(AdsenseCode).join(AdsenseType).filter(AdsenseType.name == 'In-feed Ads').first()
            if ads is not None:
                global_vars.ADSENSE_INFEED_CODE = ads.code

    @app.route('/')
    @app.route('/<uri>')
    def index(uri=None):
        print(uri)
        import importlib
        if uri is None:
            page = Page.query.filter_by(is_homepage=True).first()
        else:
            page = Page.query.filter(Page.url == uri).first()
        menus = Menu.query.order_by('order')
        if page is None:
            return uri
        else:
            views_= importlib.import_module('web_app.apps.{}.views'.format(page.subtype))
            content = views_.process(page)
            og = views_.get_og(page)
            return render_template('index.html', global_vars=global_vars, content=content, menus=menus, og=og)

    @app.route('/register', methods=['GET', 'POST'])
    @anonymous_user_required
    def register():
        return flask_security.views.register()

    return app
