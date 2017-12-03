from flask_security import RoleMixin, UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy import event


'''
http://docs.sqlalchemy.org/en/latest/core/constraints.html
'''

db = SQLAlchemy()


class Page(db.Model):
    __tablename__ = 'page'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String)
    tag = Column(String)
    keyword = Column(String)
    is_homepage = Column(Boolean)

    subtype = Column(String, default='page')
    subtype_data = Column(String)

    stamp = Column(DateTime)
    category = Column(String)
    url = Column(String, nullable=False)

    def __repr__(self):
        return self.title


def before_insert_update_listener(mapper, connection, target):
    if target.url is None:
        target.url = target.title.replace(' ', '-').lower()

        import re
        regex = re.compile('[^a-zA-Z\-]')
        print(target.url)
        target.url = (regex.sub('', target.url)).lower()
        print(target.url)

event.listen(Page, 'before_insert', before_insert_update_listener)
event.listen(Page, 'before_update', before_insert_update_listener)


class Menu(db.Model):
    __tablename__ = 'menu'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    order = Column(Integer, nullable=False)

    page_id = Column(Integer, ForeignKey('page.id'))
    page = relationship("Page", backref=backref("Linked from Menu", uselist=False))

    def __repr__(self):
        return self.title


class SiteConfiguration(db.Model):
    __tablename__ = 'siteconfiguration'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    tagline = Column(String, nullable=False)
    show_registration_menu = Column(Boolean)
    youtube_link = Column(String)


roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return self.name


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return self.email