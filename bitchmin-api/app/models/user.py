from dataclasses import dataclass
from datetime import datetime

from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from app.models._basemodel import _BaseModelMixin


@dataclass
class User(db.Model, _BaseModelMixin):
    __tablename__ = 'users'
    id: str
    fullName: str

    email = db.Column(db.String(120), unique=True, nullable=False)
    fullName = db.Column(db.String(120), unique=False, nullable=True)
    password = db.Column(db.String(255), nullable=False)

    dns_updates = relationship("DnsUpdate")

    def __init__(self, email, fullName, password):
        self.email = email
        self.fullName = fullName
        self.password = generate_password_hash(password, method='sha256')

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @classmethod
    def authenticate(cls, **kwargs):
        email = kwargs.get('email')
        password = kwargs.get('password')

        if not email or not password:
            return None

        user = cls.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return None

        return user

    @classmethod
    def by_id(cls, user_id):
        return cls.query.get(user_id)

    def to_dict(self):
        return dict(id=self.id, email=self.email)
