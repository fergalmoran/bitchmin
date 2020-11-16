from dataclasses import dataclass
from datetime import datetime

from flask_serialize import FlaskSerializeMixin
from sqlalchemy import event
from sqlalchemy.orm import relationship, validates, MapperExtension
from sqlalchemy_utils import IPAddressType

from app import db
from app.models._basemodel import _BaseModelMixin


@dataclass
class DnsNameServer(db.Model, _BaseModelMixin, FlaskSerializeMixin):
    __tablename__ = 'dns_nameservers'

    host = db.Column(db.String(255), unique=True, nullable=False)
    ip = db.Column(IPAddressType(255), nullable=False)
    zone_id = db.Column(db.Integer, db.ForeignKey('dns_zones.id'))
    zone = relationship("DnsZone", back_populates="nameservers")

    def __init__(self, zone, host, ip):
        self.zone = zone
        self.host = host
        self.ip = ip

    def to_dict(self):
        return {
            'host': self.host,
            'ip': self.ip
        }


@dataclass
class DnsZone(db.Model, _BaseModelMixin, FlaskSerializeMixin):
    __tablename__ = 'dns_zones'
    relationship_fields = ['nameservers', 'hosts']

    def __init__(self, zone_name):
        self.zone_name = zone_name
        self.serial = self._create_serial()

    def get_serial_increment(self):
        return int(str(self.serial)[8:])

    def _create_serial(self):
        return datetime.today().strftime('%Y%m%d{:02d}'.format(0))

    def increment_serial(self):
        current = str(self.serial)
        if current and len(current) == 10:
            inc = self.get_serial_increment()
            return datetime.today().strftime('%Y%m%d{:02d}'.format(inc + 1))

        return self._create_serial()

    def to_dict(self):
        ret_data = {
            'id': self.id,
            'name': self.zone_name,
            'serial': self.serial,
            'admin': self.admin,
            'nameservers': [ns.to_dict() for ns in self.nameservers],
            'hosts': [host.to_dict() for host in self.hosts]
        }
        return ret_data

    # TODO: FUCK!!
    admin = 'Ferg@lMoran.me'

    id = db.Column(db.Integer, primary_key=True)
    zone_name = db.Column(db.String(253), unique=True, nullable=False)
    serial = db.Column(db.Integer, default=_create_serial)

    hosts = relationship("DnsHost", back_populates="zone")
    nameservers = relationship("DnsNameServer", back_populates="zone")


@dataclass
class DnsHost(db.Model, _BaseModelMixin, FlaskSerializeMixin):
    __tablename__ = 'dns_hosts'

    id = db.Column(db.Integer, primary_key=True)
    zone_id = db.Column(db.Integer, db.ForeignKey('dns_zones.id'))
    zone = relationship("DnsZone", back_populates="hosts")

    host = db.Column(db.String(255), unique=True, nullable=False)
    ip = db.Column(IPAddressType(255), nullable=False)
    type = db.Column(db.String(10), nullable=False)
    ttl = db.Column(db.Integer(), nullable=False)

    def __init__(self, zone, host, ip, ttl=30, record_type='A'):
        self.zone = zone
        self.host = host
        self.ip = ip
        self.ttl = ttl
        self.type = record_type
        pass

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.host,
            'type': self.type,
            'ttl': self.ttl,
            'ip': self.ip,
            'created_on': self.created_on,
        }


# @event.listens_for(DnsZone.hosts, 'append')
# @event.listens_for(DnsZone.hosts, 'remove')
# def increment_zone_serial_handler(target, value, initiator):
#     target.serial = target.increment_serial()


@event.listens_for(DnsHost.ip, 'set', active_history=True)
def increment_zone_serial_handler(target, value, old, initiator):
    if target.zone:
        target.zone.serial = target.zone.increment_serial()
