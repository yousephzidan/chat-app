from flask.blueprints import Blueprint
from flask import render_template
from models import User, db, Friends
from flask import flash
from flask import url_for, redirect
from  controllers import home_bp
from flask import session
from sqlalchemy import or_, and_



@home_bp.get("/home")
def home_get():
    print(session) 
    user_info = User.query.filter_by(id=session["user_id"]).first()
    print(user_info.username)

    total_received_friends_reqs = (
        db.session.query(User.username, User.id)
        .join(Friends, User.id == Friends.sender_id)
        .filter(Friends.receiver_id == session["user_id"], Friends.status == "pending")
        .all()
    )

    user_id = session["user_id"]

    friends = (
        db.session.query(User.username, User.id)
        .join(Friends, or_(
            Friends.sender_id == User.id,
            Friends.receiver_id == User.id
            ))
        .filter(
            Friends.status == "accepted",
            or_(
                Friends.sender_id == user_id,
                Friends.receiver_id == user_id
                ),
            User.id != user_id  
            )
        .distinct()
        .all()
        )
    
    print(friends)
    return render_template("home/home.html", user_info=user_info, total_received_friends_reqs=total_received_friends_reqs, friends=friends)
