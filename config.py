import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'YOU WLL NEVER GUESS'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATOINS = False