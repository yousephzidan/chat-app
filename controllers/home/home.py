from flask.blueprints import Blueprint
from flask import render_template
from models import User, db
from flask import flash
from flask import url_for, redirect
from  controllers import home_bp




@home_bp.get("/home")
def home_get():
    return render_template("home/home.html")