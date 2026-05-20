from flask import request, jsonify

from src.model.comments import Comments
from src.model.post import Post
from flask_jwt_extended import get_jwt_identity
from src.schema.post import posts_schema, post_schema


class PostService:

    def __init__(self, database):
        self._db = database

    def create_post(self):
        data = request.get_json()

        if not data:
            return jsonify({"message":"Invalid or missing data"}), 401

        try:
            user_id = get_jwt_identity()

            title = data.get("title")
            body = data.get("body")

            if not title or not body:
                return jsonify({"message":"Missing fields required"}), 401

            new_post = Post(title=title, body=body, author_id=int(user_id))
            self._db.session.add(new_post)
            self._db.session.commit()

            return jsonify({"message":"post created successfully"}), 201
        except Exception as e:
            self._db.session.rollback()
            return jsonify({"error":str(e)}), 500

    @staticmethod
    def retrieve_posts():
        posts = Post.query.all()

        if not posts:
            return jsonify({"message":"No post made"}), 404

        return jsonify(posts_schema.dump(posts)), 200

    @staticmethod
    def get_post(post_id: int):
        post = Post.query.get(post_id)
        if not post:
            return jsonify({"message":f"Post with id {post_id} not found"}), 404

        return jsonify(post_schema.dump(post)), 200

    def edit_post(self, post_id: int):
        post = Post.query.filter_by(post_id=post_id).first()
        if not post:
            return jsonify({"message":"post not found"}), 404

        data = request.get_json()

        if "title" in data:
            post.title = data["title"]
        if "body" in data:
            post.body = data["body"]

        self._db.session.commit()

        return jsonify({"message":"post updated or edited"}), 200

    def delete_post(self, post_id: int):
        post = Post.query.filter_by(post_id=post_id).first()
        if not post:
            return jsonify({"message":"post not found"}), 404

        self._db.session.delete(post)
        self._db.session.commit()
        return jsonify({"message":"post deleted successfully"}), 200

    def add_comment(self, post_id: int):
        user_id = get_jwt_identity()
        post = Post.query.filter_by(post_id=post_id).first()
        if not post:
            return jsonify({"message":"post not found"}), 404

        data = request.get_json()
        if not data:
            return jsonify({"message":"Invalid or missing data"}), 401

        body = data.get("body")
        new_comment = Comments(body=body, author_id=user_id, post_id=post_id)
        self._db.session.add(new_comment)
        self._db.session.commit()

        return jsonify({"message":"comment added successfully"}), 200








