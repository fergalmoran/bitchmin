import logging

from flask import jsonify
from flask_jwt_extended import get_current_user, jwt_required

from app.api import api

logger = logging.getLogger(__name__)


@api.route('/debug/user', methods=('GET',))
@jwt_required
def ping_debugger():
    user = get_current_user()
    return jsonify({
        'status': 'success',
        'payload': user
    }), 200
