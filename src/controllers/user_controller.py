from flask import Blueprint
from src.repo.database import Database
from src.services.user_service import UserService


app_bp = Blueprint("main", __name__)
db = Database().db
service = UserService(database=db)

@app_bp.route("/", methods=["GET"])
def homepage():
    return "Welcome to Nkata Blog Application"

@app_bp.route("/register", methods=["POST"])
def register_user():
    service.register()