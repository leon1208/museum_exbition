from flask import Blueprint

gen = Blueprint('gen', __name__, url_prefix='/tool/gen')


from . import gen
from . import column