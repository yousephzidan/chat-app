from models import db
from datetime import datetime
from datetime import timezone

class Friends(db.Model):
    __tablename__ = "friends"

    id = db.Column(db.Integer, primary_key=True)

    status = db.Column(db.String(20), default="pending", nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reciever_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
