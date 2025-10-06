from models import db


class User(db.Model):
    __tablename__: str = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)

    messages = db.relationship("Message", backref="sender", lazy=True)

