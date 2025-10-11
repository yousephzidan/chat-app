import os
from flask import Flask
from flask_socketio import SocketIO
from dotenv import load_dotenv
from config import DevelopmentConfig, TestingConfig, ProductionConfig
from models import db
from controllers import auth_bp, home_bp, friends_bp, User, Friends
from werkzeug.security import generate_password_hash

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
    app.register_blueprint(home_bp)
    app.register_blueprint(friends_bp)

    socketio = SocketIO(app)
    
    with app.app_context():
        db.drop_all()
        db.create_all()

        for user in ["max1", "joe1", "tim1", "jack1"]:
            user = User(username=user, password=generate_password_hash("123", method="pbkdf2:sha256", salt_length=16)) 
            db.session.add(user)
            db.session.commit()

        friend = Friends(sender_id=1, receiver_id=3, status="pending")
        db.session.add(friend)
        db.session.commit()


        friend = Friends(sender_id=2, receiver_id=3, status="pending")
        db.session.add(friend)
        db.session.commit()

        friend = Friends(sender_id=1, receiver_id=2, status="pending")
        db.session.add(friend)
        db.session.commit()

    return app, socketio

if __name__ == "__main__":
    app, socketio = create_app()
    socketio.run(app, debug=app.config["DEBUG"])