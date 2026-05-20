from flask import jsonify
from typing import Type
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash


def server_error(error):
    return jsonify({"error": str(error)}), 500


def status_msg(message: str, status_code: int = 401):
    return jsonify({"message":message}), status_code


def set_password(obj: Type, password: str):
    obj.password = generate_password_hash(password=password)


def check_password(obj: Type, password: str):
    return check_password_hash(obj.password, password=password)


def generate_user_token(obj: Type, email: str, password: str):
    user = obj.query.filter_by(email=email).first()

    if user and check_password(obj, password=password):
        access_token = create_access_token(identity=obj.user_id)
        return access_token, user
    return None