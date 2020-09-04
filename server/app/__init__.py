import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager, verify_jwt_in_request_optional, get_jwt_identity
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.utils.encoders import IPAddressFieldEncoder

from app.config import Config

logger = logging.getLogger(__name__)

db = SQLAlchemy()
jwt = JWTManager()

migrate = Migrate()


def create_app(app_name='bitchmin', config_class=Config):

    logger.info('Creating app {}'.format(app_name))
    app = Flask(app_name)
    app.config.from_object(config_class)

    logger.info('Creating database {}'.format(app.config['SQLALCHEMY_DATABASE_URI']))
    db.init_app(app)
    jwt.init_app(app)
    logger.info('Performing migrations')
    migrate.init_app(app, db)

    # cors = CORS(app, resources={r"/*": {"origins": "*"}})
    CORS(app, supports_credentials=True)

    logger.info('Registering blueprints')
    from app.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/')

    if not app.debug and not app.testing:
        logger.info('Setting up live logging')
        if app.config['LOG_TO_STDOUT']:
            logger.info('Creating STDOUT handlers')
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            logger.info('Creating file handlers')
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler(
                'logs/BitchMin.log',
                maxBytes=10240,
                backupCount=10)

            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

    app.json_encoder = IPAddressFieldEncoder

    db.init_app(app)

    return app
