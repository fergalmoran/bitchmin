from .config import Config


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
    # SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://bitchmin:bitchmin@localhost/bitchmin'

