from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')

    db = SQLAlchemy(app)

    @app.route('/')
    def index():
        return render_template('index.html', TITLE=app.config['TITLE'],
                               TAGLINE=app.config['TAGLINE'])

    @app.route('/about')
    def about():
        return render_template('about.html', TITLE=app.config['TITLE'],
                               TAGLINE=app.config['TAGLINE'])

    @app.route('/testdb')
    def testdb():
        import psycopg2
        con = psycopg2.connect('dbname=web_app user=devuser password=devpassword host=postgres')
        cur = con.cursor()
        cur.execute("SELECT * FROM page;")

        id, title = cur.fetchone()
        con.close()
        return title


    return app