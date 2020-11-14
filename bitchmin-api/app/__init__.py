import logging
import os
from logging.handlers import RotatingFileHandler

from celery import Celery
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import flask_monitoringdashboard as dashboard

from app.conf import load_config
from app.utils.encoders import IPAddressFieldEncoder

logger = logging.getLogger(__name__)

db = SQLAlchemy()
jwt = JWTManager()
mail = Mail()
migrate = Migrate()

CELERY_TASK_LIST = [
    'app.tasks.hosts',
]


def create_app(app_name='bitchmin'):
    logger.info('Creating app {}'.format(app_name))
    app = Flask(app_name)

    app.config.from_object(
        load_config(os.environ.get('FLASK_ENV'))
    )

    logger.info('Creating database {}'.format(app.config['SQLALCHEMY_DATABASE_URI']))
    db.init_app(app)
    jwt.init_app(app)
    logger.info('Performing migrations')
    migrate.init_app(app, db)
    mail.init_app(app)

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
    dashboard.bind(app)
    dashboard.config.init_from(envvar='FLASK_MONITORING_DASHBOARD_CONFIG')

    db.init_app(app)

    return app


def create_celery_app(app=None):
    app = app or create_app()

    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        include=CELERY_TASK_LIST)

    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery
