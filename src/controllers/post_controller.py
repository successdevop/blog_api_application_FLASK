from flask import Blueprint
from src.services.post_service import PostService
from src.repo.database import db
from flask_jwt_extended import jwt_required


post_service = PostService(database=db)

post_bp = Blueprint("post_c", __name__)

@post_bp.route("/posts", methods=["POST"])
@jwt_required()
def create_post():
    return post_service.create_post()


@post_bp.route("/posts", methods=["GET"])
def retrieve_all_post():
    return post_service.retrieve_posts()


@post_bp.route("/posts/<string:post_id>", methods=["GET"])
def get_post(post_id: str):
    return post_service.get_post(post_id)


@post_bp.route("/posts/<string:post_id>", methods=["PATCH"])
@jwt_required()
def edit_post(post_id: str):
    return post_service.edit_post(post_id)


@post_bp.route("/posts/<string:post_id>", methods=["DELETE"])
@jwt_required()
def delete_post(post_id: str):
    return post_service.delete_post(post_id)


@post_bp.route("/posts/<string:post_id>/comments", methods=["POST"])
@jwt_required()
def add_comment_to_a_post(post_id: str):
    return post_service.add_comment(post_id=post_id)


@post_bp.route("/posts/<string:post_id>/comments", methods=["GET"])
def get_all_comments_on_a_post(post_id: str):
    return post_service.get_comments(post_id=post_id)


@post_bp.route("/posts/<string:post_id>/comments/<string:comment_id>", methods=["PATCH"])
@jwt_required()
def edit_comment_on_a_post(post_id: str, comment_id: str):
    return post_service.edit_comment(post_id, comment_id)


@post_bp.route("/posts/<string:post_id>/comments/<string:comment_id>", methods=["DELETE"])
@jwt_required()
def delete_comment_on_a_post(post_id: str, comment_id: str):
    return post_service.delete_comment(post_id, comment_id)