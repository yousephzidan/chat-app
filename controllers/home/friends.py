from flask import session, Blueprint, jsonify, abort, request, jsonify
from controllers import friends_bp
from models import User, Friends, db
from sqlalchemy import or_, and_

@friends_bp.post("/respond/<int:sender_id>")
def friend_request_action(sender_id: int):
    current_user = session.get('user_id')

    action = request.get_json()
    action = action.get("action")
    if not current_user:
        abort(404)

    friend_request = Friends.query.filter(Friends.sender_id==sender_id, Friends.receiver_id==current_user, Friends.status=="pending").first()
   
    if not friend_request:
        return jsonify({"error": "Friend request not found"})

    if action == "reject":
        db.session.delete(friend_request)
        db.session.commit()
        return jsonify({"reject": "friend request rejected"}), 201

    elif action == "accept":
        friend_request.status = "accepted"
        db.session.commit()
        return jsonify({"accept": "friend request accepted"}), 201

    return jsonify({"error": "Invalid action"}), 400


    ...
@friends_bp.post("/add/<string:friend_username>")
def add_friend(friend_username: str):
    current_user = session.get('user_id')

    if not current_user:
        abort(404)

    print("friend user name: ", friend_username) 
    friend = User.query.filter_by(username=friend_username).first()

    if not friend:
        return jsonify({"error": "User Not Found"}), 404
    
    friend_id = friend.id

    if friend_id == current_user:
        return jsonify({"error": "Can't friend your self"}), 409
    
    existing_friend_request =  Friends.query.filter(
        ((Friends.sender_id == current_user) & (Friends.receiver_id == friend_id))
        | ((Friends.sender_id == friend_id) & (Friends.receiver_id == current_user))
    ).first()

    if existing_friend_request:
        return jsonify({"error": "Friend request already exists"}), 409

    already_friends = Friends.query.filter(
    or_(
        and_(
            Friends.sender_id == current_user,
            Friends.receiver_id == friend_id,
            Friends.status == "accepted"
        ),
        and_(
            Friends.sender_id == friend_id,
            Friends.receiver_id == current_user,
            Friends.status == "accepted"
        )
    )
    ).first()

    if already_friends:
        return jsonify({"error": "You are already friends with the user"}), 409

    new_friend = Friends(
        sender_id=current_user,
        receiver_id=friend_id,
        status="pending",
    
    )

    db.session.add(new_friend)    
    db.session.commit()    

    return jsonify({"message": f"Friend request sent to {friend.username}"}), 201
