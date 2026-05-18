from flask import request, jsonify
from src.model.user import User
from werkzeug.security import generate_password_hash


class UserService:
    def __init__(self, database):
        self.db = database

    def register(self):
        data = request.get_json()
        if not data:
            return jsonify({"message":"Invalid or missing json"}), 401

        user_name = data.get("user_name")
        email = data.get("email")
        password = data.get("password")

        try:

            user = User.query.filter_by(email=email).first()
            if user:
                return jsonify({"message":"Email already exists"}), 404

            hash_pwd = generate_password_hash(password)

            new_user = User(user_name=user_name, email=email, password=hash_pwd)

            self.db.session.add(new_user)
            self.db.session.commit()
            return jsonify({"message": f"Congratulation {user_name}, your registration is successful"}), 201

        except Exception as e:
            self.db.session.rollback()
            return jsonify({"error": str(e)}), 500


