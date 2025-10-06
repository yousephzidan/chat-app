import os
from flask import Flask
from flask_socketio import SocketIO
from dotenv import load_dotenv
from config import DevelopmentConfig, TestingConfig, ProductionConfig
from models import db
from controllers import auth_bp

load_dotenv()

def env_type():
    env: str = os.getenv("FLASK_ENV", "development").lower()

    if env == "production":
        return ProductionConfig
    elif env == "development":
        return DevelopmentConfig 
    else:
        return TestingConfig

def create_app():
    app = Flask(__name__, template_folder="views")
    app.config.from_object(env_type())

    db.init_app(app)

    app.register_blueprint(auth_bp)

    socketio = SocketIO(app)
    
    with app.app_context():
        db.create_all()

    return app, socketio

if __name__ == "__main__":
    app, socketio = create_app()
    socketio.run(app, debug=app.config["DEBUG"])