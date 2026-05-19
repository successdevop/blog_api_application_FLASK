from flask import Blueprint
from src.services.post_service import PostService
from src.repo.database import Database
from flask_jwt_extended import jwt_required


db = Database().db
post_service = PostService(database=db)

post_bp = Blueprint("post_c", __name__)

@post_bp.route("/post", methods=["POST"])
@jwt_required()
def create_post():
    return post_service.create_post()

