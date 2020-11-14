import json
from types import SimpleNamespace


class Zone(object):
    def __init__(self, serial, name, admin, hosts):
        self._serial = serial
        self._name = name
        self._admin = admin
        self._hosts = hosts

    @staticmethod
    def from_json(data):
        try:
            zones = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
            return [Zone(
                x.serial,
                x.name,
                x.admin,
                {h.name: Host(
                    h.ip,
                    h.name,
                    h.ttl,
                    h.type
                ) for h in x.hosts}
            ) for x in zones]
        except Exception as e:
            print(e)

    @property
    def name(self):
        return self._name

    @property
    def admin(self):
        return self._admin

    @property
    def serial(self):
        return self._serial

    @property
    def hosts(self):
        return self._hosts


class Host(object):

    def __init__(self, ip, name, ttl, record_type):
        self._ip = ip
        self._name = name
        self._ttl = ttl
        self._record_type = record_type

    @property
    def ip(self):
        return self._ip

    @property
    def name(self):
        return self._name

    @property
    def ttl(self):
        return self._ttl

    @property
    def record_type(self):
        return self._record_type
