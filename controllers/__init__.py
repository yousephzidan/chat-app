from flask.blueprints import Blueprint

auth_bp: Blueprint = Blueprint("auth", __name__, template_folder="views")
home_bp: Blueprint = Blueprint("home", __name__, template_folder="views")
friends_bp = Blueprint("friends", __name__, url_prefix="/friends")
chat_bp = Blueprint("chat", __name__)

from .auth.register import * 
from .auth.login import * 
from .home.home import *
from .home.friends import *
