import os
import sys

from flask_admin.contrib.sqla import ModelView
from flask_wtf import CsrfProtect

sys.path.append(os.getcwd() + "/web_app/")

import humanize
import flask_security
from flask import Flask, render_template, request, session
from flask_admin import Admin
from flask_security import SQLAlchemyUserDatastore, Security
from flask_security.decorators import anonymous_user_required

import global_vars as global_vars
from models import db, Page, Menu, User, Role, SiteConfiguration, Image, AdsenseCode, AdsenseType, PageState
from views import PageModelView, MenuModelView, UserModelView, RoleModelView, SecuredHomeView, \
    SiteConfigurationView, ImageView

from utils.humanize import number
from api.core import ToggleLovesAPI, CommentAPI, AccountKitAPI
from flask_restful import Api, abort


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')
    db.init_app(app)

    admin = Admin(app, name='Giwangan', template_mode='bootstrap3', index_view=SecuredHomeView())

    admin.add_view(PageModelView(Page, db.session))
    admin.add_view(MenuModelView(Menu, db.session))
    admin.add_view(UserModelView(User, db.session))
    admin.add_view(RoleModelView(Role, db.session))
    admin.add_view(SiteConfigurationView(SiteConfiguration, db.session))
    admin.add_view(ImageView(Image, db.session))
    admin.add_view(ModelView(AdsenseType, db.session))
    admin.add_view(ModelView(AdsenseCode, db.session))
    admin.add_view(ModelView(PageState, db.session))

    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)
    # csrf = CsrfProtect(app)

    api = Api(app)
    api.add_resource(ToggleLovesAPI, '/api/loves')
    api.add_resource(CommentAPI, '/api/comments')
    api.add_resource(AccountKitAPI, '/api/accountkit')

    # @app.before_request
    # def csrf_protect():
    #     if request.method == "POST":
    #         token = session.pop('_csrf_token', None)
    #         if not token or token != request.form.get('_csrf_token'):
    #             abort(403)

    def generate_csrf_token():
        if '_csrf_token' not in session:
            import os, binascii
            session['_csrf_token'] = binascii.b2a_hex(os.urandom(15))
        return session['_csrf_token']

    app.jinja_env.globals.update(generate_csrf_token=generate_csrf_token)

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
            global_vars.DESCRIPTION = siteconfiguration.description

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

            # header
            ads = db.session.query(AdsenseCode).join(AdsenseType).filter(AdsenseType.name == 'Header Ads').first()
            if ads is not None:
                global_vars.ADSENSE_HEADER = ads.code

            # footer
            ads = db.session.query(AdsenseCode).join(AdsenseType).filter(AdsenseType.name == 'Footer Ads').first()
            if ads is not None:
                global_vars.ADSENSE_FOOTER = ads.code

            # footer
            ads = db.session.query(AdsenseCode).join(AdsenseType).filter(AdsenseType.name == 'Large Skyscraper').all()
            if ads is not None:
                for a in ads:
                    global_vars.ADSENSE_SKYSCRAPER.append(a.code)


    @app.route('/')
    @app.route('/<uri>')
    def index(uri=None):
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
            loved = views_.get_love(page)
            return render_template('index.html', global_vars=global_vars, content=content,
                                   menus=menus, og=og, page=page, loved=loved)

    @app.route('/register', methods=['GET', 'POST'])
    @anonymous_user_required
    def register():
        return flask_security.views.register()

    @app.template_filter('friendly_time')
    def friendly_time(date):
        # humanize.i18n.activate('in_ID')
        return humanize.naturaltime(date)

    @app.template_filter('friendly_number')
    def friendly_number(n):
        return number.intword(n)

    @app.template_filter('safe_email')
    def safe_email(s):
        return s[:s.index('@')]

    return app
