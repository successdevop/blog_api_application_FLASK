from flask import jsonify, request
from src.model.user import User


class Auth:
    def __init__(self, database=None):
        self._database = database

    def register(self):
        try:
            data = request.get_json()
            if not data:
                return jsonify({"message":"Invalid or missing data"}), 401

            user_name = data.get("user_name")
            email = data.get("email")
            password = data.get("password")

            if User.query.filter_by(email=email).first():
                return jsonify({"message":"Email already exists"})

            if not user_name or not email or not password:
                return jsonify({"message":"Incomplete or missing credentials"})

            new_user = User(user_name=user_name, email=email)
            new_user.set_password(password=password)

            self._database.session.add(new_user)
            self._database.session.commit()

            return jsonify({"message":f"Congratulations {user_name}, your registration is successful"}), 201

        except Exception as e:
            self._database.session.rollback()
            return jsonify({"error":str(e)}), 500

    def login(self):
        try:
            data = request.get_json()
            if not data:
                return jsonify({"message":"Invalid or missing data"}), 401

            email = data.get("email")
            password = data.get("password")

            token, _ = User.authenticate_user(email=email, password=password)
            if not token:
                return jsonify({"message":"Invalid email or password"}), 401

            return jsonify({"message":"Login successful", "access_token":token, "token_type":"Bearer"}), 200
        except Exception as e:
            return jsonify({"error":str(e)}), 500