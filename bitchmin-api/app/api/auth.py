import logging
from datetime import timedelta

from flask import jsonify, request, current_app
from flask_jwt_extended import (
    jwt_refresh_token_required, get_current_user
)
from sqlalchemy.orm.exc import NoResultFound

from app import db, jwt
from app.api import api
from app.models.user import User

logger = logging.getLogger(__name__)


@jwt.user_loader_callback_loader
def user_loader_callback(identity):
    return db.session.query(User).get(identity)


@api.route('/auth/register/', methods=('POST',))
def register():
    data = request.get_json()
    user = User(**data)
    try:
        db.session.query(User).filter_by(email=user.email).one()
        return jsonify({
            'status': 'error',
            'payload': 'User with email {} already exists.'.format(user.email)
        }), 409
    except NoResultFound:
        db.session.add(user)
        db.session.commit()
        return jsonify(user.to_dict()), 201


@api.route('/auth/login/', methods=('POST',))
def login():
    data = request.get_json()
    user = User.authenticate(**data)

    if not user:
        return jsonify({'message': 'Invalid credentials', 'authenticated': False}), 401
    access_token = user.create_token(timedelta(days=14) if current_app.config['ISDEV'] else timedelta(minutes=15))
    refresh_token = user.create_refresh_token()

    return jsonify({
        'accessToken': access_token,
        'refreshToken': refresh_token,
        'user': {
            'fullName': user.full_name
        }
    }), 200


@api.route('/auth/token/refresh', methods=('POST',))
@jwt_refresh_token_required
def token_refresh():
    user = get_current_user()
    access_token = user.create_token()
    refresh_token = user.create_refresh_token()

    return jsonify({
        'accessToken': access_token,
        'refreshToken': refresh_token, }
    ), 200
