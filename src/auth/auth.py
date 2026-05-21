import re

from flask import request
from src.model.user import User
from src.utils.utils import server_error, status_msg, set_password, generate_user_token


class Auth:
    def __init__(self, database=None):
        self._database = database

    def _validate_email(self, email: str):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    def _validate_password(self, password: str):
        if len(password) < 8:
            return False, "Password must be at least 8 characters"
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one upper case letter"
        if not re.search(r'[0-9]', password):
            return False, "Password must contain at least one number"

        return True, "OK"

    def register(self):
        data = request.get_json()
        if not data:
            return status_msg("Invalid or missing data", 400)

        user_name = data.get("user_name", "").strip()
        email = data.get("email", "").strip().lower()
        password = data.get("password", "").strip()

        if not user_name or len(user_name) < 3:
            return status_msg("user_name must be at least 3 characters", 400)

        is_valid_email = self._validate_email(email)
        if not is_valid_email:
            return status_msg(f"Email format is invalid", 400)

        if User.query.filter_by(email=email).first():
            return status_msg("Email already exists", status_code=409)

        if User.query.filter_by(user_name=user_name).first():
            return status_msg("user_name already exists", 409)

        is_valid_password, msg = self._validate_password(password=password)
        if not is_valid_password:
            return status_msg(msg, 400)

        new_user = User(user_name=user_name, email=email)
        set_password(new_user, password)

        try:
            self._database.session.add(new_user)
            self._database.session.commit()
            return status_msg({
                "message":"Registration successful",
                "user_id":new_user.user_id,
                "user_name":new_user.user_name
            }, status_code=201)

        except Exception as e:
            self._database.session.rollback()
            return server_error(error=e)

    def login(self):
        data = request.get_json()
        if not data:
            return status_msg("Invalid or missing data")

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return status_msg("Email and password required", 400)

        try:
            token, _ = generate_user_token(User, email=email, password=password)
            if not token:
                return status_msg("Invalid email or password")

            message = {'message':'Login success', 'access_token':f'{token}', 'token_type':'Bearer'}
            return status_msg(message, 200)
        except Exception as e:
            return status_msg({"Login failed":str(e)})

    def forgot_password(self):
        data = request.get_json()
        if not data:
            return status_msg("Invalid or missing data")

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return status_msg("Email and password required", 400)

        user = User.query.filter_by(email=email).first()
        if not user:
            return status_msg("user not found", 404)

        try:
            set_password(user, password=password)
            self._database.session.commit()
            return status_msg("Password reset successful", 200)
        except Exception as e:
            self._database.session.rollback()
            return server_error(error=e)