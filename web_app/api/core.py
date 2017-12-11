import requests
from flask import request, jsonify
from flask_restful import Resource
import json

from flask_security import login_user

from models import db, Page, User, Comment


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


class CommentAPI(Resource):

    def put(self):
        """
        Comment a page
        :return: success or not
        """
        page_id = request.form.getlist('page_id')[0]
        user_id = request.form.getlist('user_id')[0]
        comment = request.form.getlist('comment')[0]

        c = Comment(comment=comment, user_id=user_id)
        page = Page.query.filter_by(id=page_id).first()
        if page is not None:
            page.comments.append(c)
            db.session.commit()
            user = User.query.filter_by(id=user_id).first()
            email = user.email[:user.email.index('@')]
            return json.dumps({'success': True, 'comment': comment, 'email': email, 'id': c.id}), 200, {'ContentType': 'application/json'}
        else:
            return json.dumps({'success': False}), 200, {'ContentType': 'application/json'}


class AccountKitAPI(Resource):

    def put(self):
        print('fb success')
        code = request.form.getlist('code')[0]
        appid = '303680430123651'
        secret = '46668cf70438c9644bff716cea9db3e9'
        token_exchange_url = 'https://graph.accountkit.com/v1.1/access_token?' \
                             'grant_type=authorization_code&' \
                             'code={}&access_token=AA|{}|{}'.format(code, appid, secret)

        response = requests.get(token_exchange_url)
        if response.status_code == 200:
            data = json.loads(response.text)
            user_id = data['id']
            user_access_token = data['access_token']
            refresh_interval = data['token_refresh_interval_sec']
            print(user_id, user_access_token, refresh_interval)


            me_endpoint_url = 'https://graph.accountkit.com/v1.1/me?access_token={}'.format(user_access_token)

            response = requests.get(me_endpoint_url)
            if response.status_code == 200:
                data = json.loads(response.text)

                phone = data['phone']['number'] if data['phone'] else ''
                #register
                user = User.query.filter_by(phone=phone).first()
                if user is None:
                    user = User(phone=phone, email='', password='')
                    db.session.add(user)
                    db.commit()

                login_user(user)

                return json.dumps({'success': True, 'phone': phone}), 200, {'ContentType': 'application/json'}

        return json.dumps({'success': False}), 200, {'ContentType': 'application/json'}

