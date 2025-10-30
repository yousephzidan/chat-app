from controllers import chat_bp
from models import Messages, User, db
from flask import session, jsonify
from sqlalchemy import or_, and_

@chat_bp.post("/chat/<int:contact_id>")
def chat(contact_id: int):

    current_user = session["user_id"]

    messages = (
            db.session.query(Messages.content, Messages.created_at, User.id)
            .join(User, Messages.sender_id == User.id)
            .filter(
                or_(
                    and_(
                        Messages.sender_id == current_user,
                        Messages.reciever_id == contact_id
                        ),
                    and_(
                        Messages.sender_id == contact_id,
                        Messages.reciever_id == current_user 
                        )

                    )
                )
            .order_by(Messages.created_at.asc())
            .all()
        )

    return jsonify([
        {
            "id": m.id,
            "msg": m.content,
            "created_at": m.created_at
            }
        for m in messages
        ])




