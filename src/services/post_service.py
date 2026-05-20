from flask import request
from src.utils.utils import status_msg, server_error

from src.model.comments import Comments
from src.model.post import Post
from flask_jwt_extended import get_jwt_identity

from src.schema.comment import comments_schema
from src.schema.post import posts_schema, post_schema


class PostService:

    def __init__(self, database = None):
        self._db = database

    def create_post(self):
        data = request.get_json()

        if not data:
            status_msg("Invalid or missing data")

        user_id = get_jwt_identity()

        title = data.get("title")
        body = data.get("body")

        if not title or not body:
            status_msg("Missing fields required")

        new_post = Post(title=title, body=body, author_id=user_id)

        try:
            self._db.session.add(new_post)
            self._db.session.commit()

            status_msg("post created successfully", 201)
        except Exception as e:
            self._db.session.rollback()
            server_error(error=e)
        finally:
            self._db.session.close()

    @staticmethod
    def retrieve_posts():
        posts = Post.query.all()
        if not posts:
            status_msg("No post made", 404)
        status_msg(f"{posts_schema.dump(posts)}", 200)

    @staticmethod
    def get_post(post_id: int):
        post = Post.query.get(post_id)
        if not post:
            status_msg(f"Post with id {post_id} not found", 404)
        status_msg(f"{post_schema.dump(post)}", 200)

    def edit_post(self, post_id: int):
        post = Post.query.filter_by(post_id=post_id).first()
        if not post:
            status_msg("post not found", 404)

        data = request.get_json()

        if "title" in data:
            post.title = data["title"]
        if "body" in data:
            post.body = data["body"]

        try:
            self._db.session.commit()
            status_msg("post updated or edited", 200)
        except Exception as e:
            self._db.session.rollback()
            server_error(error=e)
        finally:
            self._db.session.close()

    def delete_post(self, post_id: int):
        post = Post.query.filter_by(post_id=post_id).first()
        if not post:
            status_msg("post not found", 404)

        try:
            self._db.session.delete(post)
            self._db.session.commit()
            status_msg("post deleted successfully", 200)
        except Exception as e:
            self._db.session.rollback()
            server_error(error=e)
        finally:
            self._db.session.close()

    def add_comment(self, post_id: int):
        user_id = get_jwt_identity()
        post = Post.query.filter_by(post_id=post_id).first()
        if not post:
            status_msg("post not found", 404)

        data = request.get_json()
        if not data:
            status_msg("Invalid or missing data")

        body = data.get("body")
        new_comment = Comments(body=body, author_id=user_id, post_id=post_id)

        try:
            self._db.session.add(new_comment)
            self._db.session.commit()
            status_msg("comment added successfully", 200)
        except Exception as e:
            self._db.session.rollback()
            server_error(error=e)
        finally:
            self._db.session.close()

    def get_comments(self, post_id: int):
        post = Post.query.filter_by(post_id=post_id).first()
        if not post:
            status_msg("post not found", 404)

        comments = post.comments.all()
        if not comments:
            status_msg("no comments on this post", 404)

        status_msg(f"{comments_schema.dump(comments)}", 200)

    def edit_comment(self, post_id: str, comment_id: str):
        current_user_id = get_jwt_identity()
        comment = Comments.query.filter_by(post_id=post_id, comment_id=comment_id).first()
        if not comment:
            status_msg("comment not found", 404)

        data = request.get_json()
        if not data:
            status_msg("Invalid or missing data")

        if "body" in data:
            comment.body = data["body"]

        try:
            self._db.session.commit()
            status_msg("comment updated successfully", 200)
        except Exception as e:
            self._db.session.rollback()
            server_error(error=e)
        finally:
            self._db.session.close()

    def delete_comment(self, post_id: str, comment_id: str):
        comment = Comments.query.filter_by(post_id=post_id, comment_id=comment_id).first()
        if not comment:
            status_msg("comment not found", 404)

        try:
            self._db.session.delete(comment)
            status_msg("comment deleted successfuly", 200)
        except Exception as e:
            self._db.session.rollback()
            server_error(error=e)
        finally:
            self._db.session.close()
