from flask import Flask, render_template
from web_app.models import db, Page


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')
    db.init_app(app)

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

        if cur.rowcount > 0:
            id, title = cur.fetchone()
        else:
            return 'empty'

        con.close()
        return title

    @app.route('/testdbsqlalchemy')
    def testdbsqlalchemy():
        page = Page.query.filter_by(id=2).first()
        if page is not None:
            return page.title
        else:
            return 'empty'

    return app