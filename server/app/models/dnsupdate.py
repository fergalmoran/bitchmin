import datetime
from dataclasses import dataclass

from sqlalchemy.orm import relationship
from sqlalchemy_utils import IPAddressType

from app import db
from app.models._basemodel import _BaseModelMixin


@dataclass
class DnsUpdate(db.Model, _BaseModelMixin):
    id: int
    host: str
    ip: str
    created_on: datetime.datetime

    __tablename__ = 'dns_updates'

    id = db.Column(db.Integer, primary_key=True)

    host = db.Column(db.String(255), unique=True, nullable=False)
    ip = db.Column(IPAddressType(255), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = relationship("User", uselist=False)

    def __init__(self, host, ip, user):
        self.host = host
        self.ip = ip
        self.user = user
        pass

    def to_dict(self):
        return dict(id=self.id, host=self.host, ip=self.ip)
