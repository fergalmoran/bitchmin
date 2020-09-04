from ipaddress import IPv4Address

from flask import json


class IPAddressFieldEncoder(json.JSONEncoder):
    " Add support for serializing IPAddress fields"

    def default(self, value):
        if isinstance(value, IPv4Address):
            return value.exploded
        return json.JSONEncoder.default(self, value)
