from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

db = SQLAlchemy()

# http://docs.sqlalchemy.org/en/latest/core/constraints.html
class Page(db.Model):
    __tablename__ = 'page'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String)
    tag = Column(String)
    keyword = Column(String)

    def __repr__(self):
        return self.title


class Menu(db.Model):
    __tablename__ = 'menu'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    order = Column(Integer, nullable=False)

    page_id = Column(Integer, ForeignKey('page.id'))
    page = relationship("Page", backref=backref("Linked from Menu", uselist=False))

    def __repr__(self):
        return self.title