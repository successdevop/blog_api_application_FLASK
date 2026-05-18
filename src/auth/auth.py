from flask import jsonify, Blueprint
from src.model.user import User
from flask_jwt_extended import create_access_token


class Auth:
    auth_bp = Blueprint("main", __name__)

    @auth_bp.route("/login", methods=['POST'])
    def login(self, user_name: str, password: str):
        try:
            user = User.query.filter_by(user_name).first()

            if not user or not user.check_password(password=password):
                return jsonify({"message":"Invalid user_name or password"}), 401

            access_token = create_access_token(identity=user_name)

            return jsonify({"message":"Login successful", "access_token":access_token, "token_type":"Bearer"}), 200
        except Exception as e:
            return jsonify({"error":str(e)}), 500


