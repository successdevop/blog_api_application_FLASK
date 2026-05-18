from flask import request, jsonify
from src.model.user import User


class UserService:
    def __init__(self, database):
        self._db = database

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

            if not user_name or not email or not password:
                return jsonify({"message":"missing fields"}), 401

            new_user = User(user_name=user_name, email=email)
            new_user.set_password(password=password)

            self._db.session.add(new_user)
            self._db.session.commit()
            return jsonify({"message": f"Congratulation {user_name}, your registration is successful"}), 201

        except Exception as e:
            self._db.session.rollback()
            return jsonify({"error": str(e)}), 500


