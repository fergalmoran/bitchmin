import json
from types import SimpleNamespace


class Zone(object):
    def __init__(self, serial, name, admin, hosts, nameservers, mailexchangers):
        self._serial = serial
        self._name = name
        self._admin = admin
        self._hosts = hosts
        self._nameservers = nameservers
        self._mailexchangers = mailexchangers

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
                ) for h in x.hosts},
                {ns.name: Nameserver(
                    ns.ip,
                    ns.name,
                    ns.ttl
                ) for ns in x.nameservers},
                {mx.name: MailExchanger(
                    mx.name,
                    mx.preference,
                    mx.ttl
                ) for mx in x.mailexchangers}
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

    @property
    def nameservers(self):
        return self._nameservers

    @property
    def mailexchangers(self):
        return self._mailexchangers


class Nameserver(object):

    def __init__(self, ip, name, ttl):
        self._ip = ip
        self._name = name
        self._ttl = ttl

    @property
    def ip(self):
        return self._ip

    @property
    def name(self):
        return self._name

    @property
    def ttl(self):
        return self._ttl


class MailExchanger(object):

    def __init__(self, name, preference, ttl):
        self._name = name
        self._preference = preference
        self._ttl = ttl

    @property
    def name(self):
        return self._name

    @property
    def preference(self):
        return self._preference

    @property
    def ttl(self):
        return self._ttl


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
