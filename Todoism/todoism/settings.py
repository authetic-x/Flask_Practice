import os


basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class Baseconfig:

    SECRET_KEY = os.getenv('SECRET_KEY', 'a secret string')

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///' + os.path.join(basedir, 'data.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class Development(Baseconfig):
    pass

config = {
    'development': Development
}