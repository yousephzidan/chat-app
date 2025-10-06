from flask import render_template
from models import User
from flask import request
from werkzeug.security import check_password_hash
from flask import flash
from flask import url_for, redirect
from  controllers import auth_bp
from flask import session


@auth_bp.post("/login")
def login_post():
    username = request.form.get("username")
    password = request.form.get("password")


    user = User.query.filter_by(username=username).first()

    if not user:
        flash("Account doesn't exist. Please register first.", "flash_error") 
        return redirect(url_for("auth.login.login_get"))

    if not check_password_hash(user.password, password):
        flash("Inccorent credentials. Try again.", "flash_error") 
        return redirect(url_for("auth.login.login_get"))

    session["user_id"] = user.id
    session["logged"] = True

    flash("Account created successfully! Login", "flash_success")
    #return redirect(url_for("home.home.home_get"))

@auth_bp.get("/login")
def login_get():
    return render_template("auth/login.html")