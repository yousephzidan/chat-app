from flask.blueprints import Blueprint

auth_bp: Blueprint = Blueprint("auth", __name__, template_folder="views")

from .auth.register import * 
