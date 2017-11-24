from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, UniqueConstraint

db = SQLAlchemy()


class Page(db.Model):
    __tablename__ = 'page'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String)
    tag = Column(String)
    keyword = Column(String)

    UniqueConstraint(title, name='page_unique_title')