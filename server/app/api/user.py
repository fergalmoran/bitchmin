import logging

from flask import jsonify
from flask_jwt_extended import jwt_required, get_current_user

from app.api import api

logger = logging.getLogger(__name__)


@api.route('/user', methods=['GET'])
@jwt_required
def get_user():
    user = get_current_user()
    if user:
        user = {
            'fullName': user.fullName,
        }
        return jsonify({
            'status': 'success',
            'payload': user
        })
    else:
        return jsonify({
            'status': 'error'
        }), 401
