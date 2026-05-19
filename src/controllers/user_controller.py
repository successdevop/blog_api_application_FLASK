from flask import Blueprint
from src.repo.database import Database
from src.auth.auth import Auth

user_bp = Blueprint("user_c", __name__)

db = Database().db
auth = Auth(database=db)

@user_bp.route("/register", methods=["POST"])
def register_user():
    return auth.register()

@user_bp.route("/login", methods=["POST"])
def login():
    return auth.login()