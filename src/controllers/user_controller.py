from flask import Blueprint
from src.repo.database import db
from src.auth.auth import Auth

user_bp = Blueprint("user_c", __name__)

auth = Auth(database=db)

@user_bp.route("/register", methods=["POST"])
def register_user():
    return auth.register()

@user_bp.route("/login", methods=["POST"])
def login():
    return auth.login()

@user_bp.route("/posts", methods=["POST"])
def forgot_password():
    return auth.forgot_password()