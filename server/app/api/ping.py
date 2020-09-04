from flask import jsonify

from app.api import api


@api.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

