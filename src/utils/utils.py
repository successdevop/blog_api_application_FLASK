from flask import jsonify, request
from src.model.user import User
from typing import Type
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash


def server_error(error):
    return jsonify({"error": str(error)}), 500


def status_msg(message, status_code: int = 401):
    return jsonify(message), status_code


def set_password(obj: User, password: str):
    obj.password = generate_password_hash(password=password)


def check_password(obj: User, password: str):
    return check_password_hash(obj.password, password=password)


def generate_user_token(obj: Type[User], email: str, password: str):
    user = obj.query.filter_by(email=email).first()

    if user and check_password(user, password=password):
        access_token = create_access_token(identity=user.user_id)
        return access_token, user
    return None


def pagination(obj: Type):
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)

    per_page = min(per_page, 100)

    paginated = obj.query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    return paginated, page, per_page
