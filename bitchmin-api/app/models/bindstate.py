from sqlalchemy_utils import IPAddressType

from app import db
from app.models._basemodel import _BaseModelMixin

"""
This is the state (as best we can determine)
of the BIND server. Most important is to store the IP for ns1.bitchmints.com
and check if this has changed on every run
"""


class BindState(db.Model, _BaseModelMixin):
    __tablename__ = 'bind_state'

    nameserver_1_ip = db.Column(IPAddressType(255), nullable=False)
    nameserver_1_host = db.Column(db.String(255), unique=True, nullable=False)

