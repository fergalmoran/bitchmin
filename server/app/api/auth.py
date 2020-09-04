import logging
from datetime import timedelta

from flask import jsonify, request
from flask_jwt_extended import (
    create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_current_user
)

from app import db, jwt
from app.api import api
from app.config import Config
from app.models.user import User

logger = logging.getLogger(__name__)


def __create_token(user_id):
    expiry = timedelta(days=14) if Config.ISDEV else timedelta(minutes=15)
    return create_access_token(
        identity=user_id,
        expires_delta=expiry,
        fresh=True)


@jwt.user_loader_callback_loader
def user_loader_callback(identity):
    return User.by_id(identity)


@api.route('/auth/register/', methods=('POST',))
def register():
    data = request.get_json()
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201


@api.route('/auth/login/', methods=('POST',))
def login():
    data = request.get_json()
    user = User.authenticate(**data)

    if not user:
        return jsonify({'message': 'Invalid credentials', 'authenticated': False}), 401
    access_token = __create_token(user.id)
    refresh_token = create_refresh_token(user.id)

    return jsonify({
        'accessToken': access_token,
        'refreshToken': refresh_token,
        'user': {
            'fullName': user.fullName
        }
    }), 200


@api.route('/auth/token/refresh', methods=('POST',))
@jwt_refresh_token_required
def token_refresh():
    user = get_current_user()
    access_token = __create_token(user.id)
    refresh_token = create_refresh_token(user.id)

    return jsonify({
        'accessToken': access_token,
        'refreshToken': refresh_token, }
    ), 200
