from flask import request, jsonify
from src.model.post import Post
from flask_jwt_extended import get_jwt_identity


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
            author_id = data.get("author_id")

            if not title or not body or not author_id:
                return jsonify({"message":"Missing fields required"}), 401

            new_post = Post(title=title, body=body, author_id=user_id)
            self._db.session.add(new_post)
            self._db.session.commit()

            return jsonify({"message":"post created successfully"}), 201
        except Exception as e:
            self._db.session.rollback()
            return jsonify({"error":str(e)})


