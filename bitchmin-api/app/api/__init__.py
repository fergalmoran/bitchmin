from flask import Blueprint

api = Blueprint('api', __name__)

from app.api import auth
from app.api import dns
from app.api import lights
from app.api import ping
from app.api import user
from app.api import debug
