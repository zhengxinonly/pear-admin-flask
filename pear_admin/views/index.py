from flask import Blueprint, render_template, send_from_directory
from flask_jwt_extended import jwt_required

index_bp = Blueprint("index", __name__)


@index_bp.route("/")
@jwt_required()
def index():
    return render_template("index.html")


@index_bp.route("/login.html")
@index_bp.route("/login")
def login():
    return render_template("login.html")


@index_bp.route("/register.html")
def register():
    return render_template("register.html")


@index_bp.route("/view/console/index.html")
def console1():
    return render_template("view/console/index.html")


@index_bp.route("/view/analysis/index.html")
def analysis():
    return render_template("view/analysis/index.html")


@index_bp.route("/view/system/person.html")
def person():
    return render_template("view/system/person.html")


@index_bp.route("/favicon.ico")
def fav_icon():
    return send_from_directory(directory="static", path="favicon.ico")
