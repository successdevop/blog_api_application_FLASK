from flask import request
from src.model.user import User
from src.utils.utils import server_error, status_msg, set_password, generate_user_token


class Auth:
    def __init__(self, database=None):
        self._database = database

    def register(self):
        data = request.get_json()
        if not data:
            return status_msg("Invalid or missing data")

        user_name = data.get("user_name")
        email = data.get("email")
        password = data.get("password")

        if not user_name or not email or not password:
            return status_msg("Incomplete or missing credentials")

        if User.query.filter_by(email=email).first():
            return status_msg("Email already exists", status_code=409)

        new_user = User(user_name=user_name, email=email)
        set_password(new_user, password)

        try:
            self._database.session.add(new_user)
            self._database.session.commit()
            return status_msg(f"Congratulations {user_name}, your registration is successful", status_code=201)

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