from flask.blueprints import Blueprint
from flask import render_template
from models import User, db
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash
from flask import flash
from flask import url_for, redirect
from  controllers import auth_bp



@auth_bp.post("/register")
def register_post():
    username = request.form.get("username")
    password = request.form.get("password")

    if not username:
        flash("Please enter a username", "username_error") 
        return redirect(url_for("auth.register_get"))

    if not password:
        flash("Please provide a password", "password_error") 
        return redirect(url_for("auth.register_get"))
 
    _hash_password = generate_password_hash(password, method="pbkdf2:sha256", salt_length=16)


    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        flash("Username already taken. Please choose another one.", "existingUser_error") 
        return redirect(url_for("auth.register_get"))

    user = User(username=username, password=_hash_password) 
    db.session.add(user)
    db.session.commit()

    flash("Account created successfully! Login", "general_flash_success")
    return redirect(url_for("auth.login_get"))

@auth_bp.get("/register")
def register_get():
    return render_template("auth/register.html")