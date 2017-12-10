from flask import request, jsonify
from flask_restful import Resource
import json

from models import db, Page, User


class ToggleLovesAPI(Resource):

    def put(self):
        """
        Toggle love for a page, for a user.
        Check if love already there, if it is, remove it.
        If not yet there, add it.
        :return: thew new condition, loved or not
        """
        page_id = request.form.getlist('page_id')[0]
        user_id = request.form.getlist('user_id')[0]
        user = User.query.join(User.loves).filter(User.id == user_id, Page.id == page_id).first()

        if user is not None:
            page = Page.query.filter_by(id=page_id).first()

            user.loves.remove(page)
            page.love_count -= 1
            db.session.commit()
            return json.dumps({'success': True, 'loved': False}), 200, {'ContentType': 'application/json'}
        else:
            user = User.query.filter_by(id=user_id).first()
            page = Page.query.filter_by(id=page_id).first()

            user.loves.append(page)
            page.love_count += 1
            db.session.commit()
            return json.dumps({'success': True, 'loved': True}), 200, {'ContentType': 'application/json'}
