from flask_socketio import SocketIO

socketio = SocketIO(cors_allowed_origins="*")

from .home import chat
from .home import voice_call


