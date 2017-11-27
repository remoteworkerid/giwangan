TITLE = 'Pythonthusiast'
TAGLINE = 'Remote Work Mentoring'
DEBUG = True
GREETING = 'Halo Dunia. Apa kabar?'

SQLALCHEMY_DATABASE_URI = 'postgresql://devuser:devpassword@postgres:5432/web_app'
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = 'marvelisgreaterthandc'

SECURITY_REGISTERABLE = True
SECURITY_PASSWORD_SALT = 'https://stackoverflow.com/questions/25942092/unique-salt-per-user-using-flask-security'

#Temporary, for use in local setup
SECURITY_CONFIRMABLE = False
SECURITY_LOGIN_WITHOUT_CONFIRMATION = True
SECURITY_SEND_REGISTER_EMAIL = False
