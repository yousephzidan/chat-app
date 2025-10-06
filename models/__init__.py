from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .friends import Friends
from .messages import Messages