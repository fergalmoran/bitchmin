import logging

from flask import jsonify, request
from flask_jwt_extended import jwt_required

from app.api import api
from app.utils.hue import hue_utils

logger = logging.getLogger(__name__)


@api.route('/lights/getlights', methods=['GET'])
@jwt_required
def getlights():
    lights = hue_utils.get_lights()

    return jsonify({
        'status': 'success',
        'payload': lights
    })


@api.route('/lights/setbrightness', methods=['POST'])
@jwt_required
def set_brightness():
    try:
        args = request.get_json()

        hue_utils.set_brightness(args['lightId'], args['brightness'])

        return jsonify({
            'status': 'success',
        })
    except Exception as e:
        logger.error(e)
        return jsonify({
            'status': 'error',
        }), 500


@api.route('/lights/changecolour', methods=['POST'])
@jwt_required
def change_colour():
    try:
        args = request.get_json()

        hue_utils.set_colour(args['lightId'], args['rgbColour'].replace('#', ''))

        return jsonify({
            'status': 'success',
        })
    except Exception as e:
        logger.error(e)
        return jsonify({
            'status': 'error',
        }), 500
