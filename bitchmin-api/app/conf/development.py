from .config import Config


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://bitchmin:bitchmin@localhost/bitchmin'
