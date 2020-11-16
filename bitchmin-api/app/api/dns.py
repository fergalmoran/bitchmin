import json
import logging
import os

import requests
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_current_user
from IPy import IP

from app import db
from app.api import api
from app.models import User, DnsHost, DnsZone
from app.utils import dnsupdate
from app.utils.dnsupdate import delete_record
from app.utils.dnsutils import get_dns_records
from app.utils.iputils import is_valid_ip, is_valid_hostname

logger = logging.getLogger(__name__)


@api.route('/dns/zones')
def get_zones():
    return jsonify([zone.to_dict() for zone in db.session.query(DnsZone).all()]), 200


@api.route('/dns/refresh', methods=['POST'])
@jwt_required
def refresh_dns():
    user = get_current_user()
    args = request.get_json()

    if not user:
        return jsonify({
            'status': 'error',
            'payload': 'Unable to find user'
        }), 401

    ip = args['ip']
    if not is_valid_ip(ip):
        return jsonify({
            'status': 'error',
            'payload': '{} is not a valid IP address'.format(ip)
        }), 400

    update_result = dnsupdate.update_dns(
        os.getenv('DNS_SERVER'),
        os.getenv('DNS_ZONE'),
        os.getenv('DNS_KEY'),
        args['host'],
        args['ip'])

    if update_result:
        return jsonify({
            'status': 'success',
            'payload': 'Host {} refreshed successfully'
        }), 200

    return jsonify({
        'status': 'failure',
        'payload': 'Unable to update host'
    }), 400


@api.route('/dns/check/', methods=['POST'])
@jwt_required
def check_host_record():
    args = request.get_json()
    ip = args['ip']
    host = args['host']

    actual_ip_records = get_dns_records(host, ip, os.getenv('DNS_SERVER'))
    if len(actual_ip_records) == 0:
        return jsonify({
            'status': 'error',
            'payload': 'Host {} is in not found in {}'.format(host, os.getenv('DNS_SERVER'), ip)
        }), 200

    if ip in actual_ip_records:
        return jsonify({
            'status': 'success',
            'payload': '{} is in {} as {}'.format(host, os.getenv('DNS_SERVER'), ip)
        }), 200

    return jsonify({
        'status': 'error',
        'payload': 'Host {} is stored as {} but resolves to {}'.format
        (host, ip, actual_ip_records[0])
    }), 200


@api.route('/dns/host/', methods=['DELETE'])
@jwt_required
def delete_dns_record():
    host = request.args['host']

    result = delete_record(
        os.getenv('DNS_SERVER'),
        os.getenv('DNS_ZONE'),
        os.getenv('DNS_KEY'),
        host)

    records = db.session.query(DnsHost).filter_by(host=host).all()
    for record in records:
        db.session.delete(record)
    db.session.commit()

    if result:
        return jsonify({
            'status': 'success',
        }), 200

    return jsonify({
        'status': 'error'
    }), 500


@api.route('/dns/host/', methods=['POST'])
@jwt_required
def update_dns():
    user = get_current_user()
    args = request.get_json()

    if not user:
        return jsonify({
            'status': 'error',
            'payload': 'Unable to find user'
        }), 401

    ip = args['ip']
    if not is_valid_ip(ip):
        return jsonify({
            'status': 'error',
            'payload': '{} is not a valid IP address'.format(ip)
        }), 400

    hostname = args['name']
    if not is_valid_hostname(hostname):
        return jsonify({
            'status': 'error',
            'payload': '{} is not a valid IP address'.format(hostname)
        }), 400

    zone = db.session.query(DnsZone).get(args['zone_id'])
    if not zone:
        return jsonify({
            'status': 'error',
            'payload': 'Zone {} does not exist'.format(args['zone_id'])
        }), 400

    count = db.session.query(DnsHost).filter_by(host=hostname).count()
    # count = db.session(DnsHost).query.filter_by(host=hostname).count()
    if count != 0:
        logger.warning('HOST {} is already in the system'.format(hostname))
        return jsonify({
            'status': 'duplicate',
            'payload': 'HOST {} is already in the system'.format(hostname)
        }), 409

    update_result = True or dnsupdate.update_dns(
        os.getenv('DNS_SERVER'),
        os.getenv('DNS_ZONE'),
        os.getenv('DNS_KEY'),
        args['zone_id'],
        args['name'],
        args['ip'])

    if update_result:
        host = DnsHost(
            zone,
            args['name'],
            args['ip']
        )
        db.session.add(host)
        db.session.commit()

        return jsonify({
            'status': 'success',
            'payload': host.to_dict()
        })

    return jsonify({
        'status': 'error'
    }), 500


@api.route('/dns/list')
@jwt_required
def get_dns_list():
    user = get_current_user()
    updates = db.session(DnsHost) \
        .query \
        .filter(User.id == user.id) \
        .all()
    return jsonify(updates)


@api.route("/dns/headers", methods=["GET"])
def get_request_headers():
    headers = {}
    for header in request.headers:
        headers[header[0]] = header[1]

    return jsonify({
        'status': 'failure',
        'payload': headers
    }), 200


@api.route("/dns/myip", methods=["GET"])
def get_my_ip():
    ip = requests.get('https://checkip.amazonaws.com').text.strip()

    if IP(ip).iptype() == 'PUBLIC':
        return jsonify({
            'status': 'success',
            'payload': ip
        }), 200

    # We're off a proxy
    ip = request.headers.get('X-Real-IP')
    if ip and IP(ip).iptype() == 'PUBLIC':
        return jsonify({
            'status': 'success',
            'payload': ip
        }), 200

    ip = request.headers.get('Forwarded')
    if ip and IP(ip).iptype() == 'PUBLIC':
        return jsonify({
            'status': 'success',
            'payload': ip
        }), 200

    return jsonify({
        'status': 'failure',
        'payload': ''
    }), 200
