from flask import request
from flask_jwt_extended import get_jwt_identity
from sqlalchemy.exc import IntegrityError

from src.utils.utils import status_msg, server_error, pagination
from src.model.comments import Comments
from src.model.post import Post

from src.schema.comment import comments_schema
from src.schema.post import posts_schema, post_schema


class PostService:

    def __init__(self, database = None):
        self._db = database

    def create_post(self):
        data = request.get_json()

        if not data or not isinstance(data, dict):
            return status_msg("Invalid or missing data", 400)

        user_id = get_jwt_identity()
        if not user_id or not isinstance(user_id, str):
            return status_msg("Authentication required")

        title = data.get("title", "").strip()
        body = data.get("body", "").strip()

        if not title or len(title) > 200:
            return status_msg("Title is required and must be less than or equal 200 characters")
        if not body or len(body) < 10:
            return status_msg("Body text is required and must be at least 10 characters")

        new_post = Post(title=title, body=body, author_id=user_id)

        try:
            self._db.session.add(new_post)
            self._db.session.commit()

            return status_msg({
                "message":"Post created successfully",
                "post_id":new_post.post_id},
                201)
        except IntegrityError as e:
            self._db.session.rollback()
            return status_msg(f"Database integrity error | {e}", 400)
        except Exception as e:
            self._db.session.rollback()
            return server_error(error=e)

    @staticmethod
    def retrieve_posts():
        paginated, page, per_page = pagination(Post)
        if not paginated.items:
            return status_msg("No post found", 404)

        return status_msg({
            "posts": posts_schema.dump(paginated.items),
            "total": paginated.total,
            "page": page,
            "per_page": per_page,
            "pages": paginated.pages
        }, 200)

    @staticmethod
    def get_post(post_id: str):
        post = Post.query.get(post_id)
        if not post:
            return status_msg(f"Post with ID {post_id} not found", 404)

        return status_msg(post_schema.dump(post), 200)

    def edit_post(self, post_id: str):
        post = Post.query.filter_by(post_id=post_id).first()
        if not post:
            return status_msg("Post not found", 404)

        current_user_id = get_jwt_identity()
        if not isinstance(current_user_id, str):
            return status_msg("Authentication required")

        if current_user_id != post.author_id:
            return status_msg("Permission denied", 403)

        data = request.get_json()
        if not data or not isinstance(data, dict):
            return status_msg("Invalid or missing data", 400)

        if "title" in data:
            post.title = data["title"]
        if "body" in data:
            post.body = data["body"]

        try:
            self._db.session.commit()
            return status_msg("Post updated successfully", 200)
        except Exception as e:
            self._db.session.rollback()
            return server_error(error=e)

    def delete_post(self, post_id: str):
        post = Post.query.filter_by(post_id=post_id).first()
        if not post:
            return status_msg("Post not found", 404)

        current_user_id = get_jwt_identity()
        if not isinstance(current_user_id, str):
            return status_msg("Authentication required")

        if current_user_id != post.author_id:
            return status_msg("Permission denied", 403)

        try:
            self._db.session.delete(post)
            self._db.session.commit()
            return status_msg("Post deleted successfully", 200)
        except Exception as e:
            self._db.session.rollback()
            return server_error(error=e)

    def add_comment(self, post_id: str):
        post = Post.query.filter_by(post_id=post_id).first()
        if not post:
            return status_msg("Post not found", 404)

        current_user_id = get_jwt_identity()
        if not isinstance(current_user_id, str):
            return status_msg("Authentication required")

        data = request.get_json()
        if not data or not isinstance(data, dict):
            return status_msg("Invalid or missing data", 400)

        body = data.get("body", "").strip()
        if not body:
            return status_msg("Body text is required and must be at least 3 characters")

        new_comment = Comments(body=body, author_id=current_user_id, post_id=post_id)

        try:
            self._db.session.add(new_comment)
            self._db.session.commit()
            return status_msg("comment added successfully", 200)
        except Exception as e:
            self._db.session.rollback()
            return server_error(error=e)

    def get_comments(self, post_id: str):
        post = Post.query.filter_by(post_id=post_id).first()
        if not post:
            return status_msg("Post not found", 404)

        paginated, page, per_page = pagination(post.comments)
        if not paginated.items:
            return status_msg("No comments found", 404)

        return status_msg({
            "comments":comments_schema.dump(paginated.items),
            "total": paginated.total,
            "page": page,
            "per_page": per_page,
            "pages": paginated.pages
        },200)


    def edit_comment(self, post_id: str, comment_id: str):
        comment = Comments.query.filter_by(post_id=post_id, comment_id=comment_id).first()
        if not comment:
            return status_msg("comment not found", 404)

        current_user_id = get_jwt_identity()
        if not isinstance(current_user_id, str):
            return status_msg("Authentication required")

        if current_user_id != comment.author_id:
            return status_msg("Permission denied", 403)

        data = request.get_json()
        if not data or not isinstance(data, dict):
            return status_msg("Invalid or missing data", 400)

        if "body" in data:
            comment.body = data["body"]

        try:
            self._db.session.commit()
            return status_msg("comment updated successfully", 200)
        except Exception as e:
            self._db.session.rollback()
            return server_error(error=e)

    def delete_comment(self, post_id: str, comment_id: str):
        comment = Comments.query.filter_by(post_id=post_id, comment_id=comment_id).first()
        if not comment:
            return status_msg("comment not found", 404)

        current_user_id = get_jwt_identity()
        if not isinstance(current_user_id, str):
            return status_msg("Authentication required")

        if current_user_id != comment.author_id:
            return status_msg("Permission denied", 403)

        try:
            self._db.session.delete(comment)
            self._db.session.commit()
            return status_msg("comment deleted successfuly", 200)
        except Exception as e:
            self._db.session.rollback()
            return server_error(error=e)
