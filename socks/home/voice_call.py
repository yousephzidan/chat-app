from socks import socketio
from flask import session
from flask_socketio import emit, join_room, leave_room


@socketio.on("send_call_offer")
def call_offer(data):
    current_user_id = session["user_id"]
    receiver_id = data["to"]
    
    room = f"dm_room_{min(current_user_id, receiver_id)}/{max(current_user_id, receiver_id)}"
    emit("receive_call_offer",{"offer": data["offer"], "from": current_user_id}, room=room,include_self=False )
    print(f"[Backend] Forwarded offer to: {room}")


@socketio.on("send_call_answer")
def call_answer(data):
    current_user_id = session["user_id"]
    receiver_id = data["to"]
    
    room = f"dm_room_{min(current_user_id, receiver_id)}/{max(current_user_id, receiver_id)}"
    emit("receive_call_answer", {"answer": data["answer"], "from": current_user_id}, room=room,include_self=False )

    print(f"[Backend] Forwarded answer to: {room}")

@socketio.on("send_ice_candidate")
def call_candidate(data):
    current_user_id = session["user_id"]
    receiver_id = data["to"]
    
    room = f"dm_room_{min(current_user_id, receiver_id)}/{max(current_user_id, receiver_id)}"

    emit("receive_ice_candidate", {"candidate": data["candidate"]}, room=room, include_self=False)
    print(f"[Backend] Forwarded ICE candidate to: {room}")

