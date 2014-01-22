import os

from .config import DefaultConfig


class ProductionConfig(DefaultConfig):
    DEBUG = False

    SECRET_KEY = 'secret key'

    INSTANCE_FOLDER_PATH = os.path.join('/tmp', 'instance')
    # Flask-Sqlalchemy: http://packages.python.org/Flask-SQLAlchemy/config.html
    SQLALCHEMY_ECHO = True
    # SQLITE for prototyping.
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
                              INSTANCE_FOLDER_PATH + '/db.sqlite'
    # MYSQL for production.
    # SQLALCHEMY_DATABASE_URI =
    # 'mysql://username:password@server/db?charset=utf8'

    # Flask-babel: http://pythonhosted.org/Flask-Babel/
    ACCEPT_LANGUAGES = ['en']
    BABEL_DEFAULT_LOCALE = 'en'

    # Flask-cache: http://pythonhosted.org/Flask-Cache/
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 60

    # Flask-mail: http://pythonhosted.org/flask-mail/
    MAIL_DEBUG = DEBUG
    MAIL_SERVER = 'smtp.sendgrid.net'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    # Should put MAIL_USERNAME and MAIL_PASSWORD in production under instance
    # folder.
    MAIL_USERNAME = 'username'
    MAIL_PASSWORD = 'password'
    MAIL_DEFAULT_SENDER = 'no-reply-web-calendar@web-presence-in-china.com'
