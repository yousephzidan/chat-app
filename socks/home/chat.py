from socks import socketio
from flask_socketio import emit, join_room
from flask import session
from models import db, Messages
from datetime import datetime, timezone

@socketio.on("join_dm")
def handle_dm_room(data):
    current_user_id = session["user_id"]
    receiver_id = data["dm_contact_id"]
    
    room = f"dm_room_{min(current_user_id, receiver_id)}/{max(current_user_id, receiver_id)}"
    join_room(room)
    

@socketio.on("send_dm")
def handle_dm_room(data):
    current_user_id = session["user_id"]
    receiver_id = data["dm_contact_id"]
    msg = data["msg"]
    

    room = f"dm_room_{min(current_user_id, receiver_id)}/{max(current_user_id, receiver_id)}"


    msg = Messages(
            sender_id=current_user_id,
            reciever_id=receiver_id,
            content=msg,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
    db.session.add(msg)
    db.session.commit()

    emit("receive_msg",
        {
         "sender_id": current_user_id,
         "receiver_id": receiver_id,
         "msg": msg.content,
         "created_at": msg.created_at.isoformat()
        },
        room=room
    )
    

    




