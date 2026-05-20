from flask import jsonify, request
from src.model.user import User
from src.utils.utils import server_error, status_msg


class Auth:
    def __init__(self, database=None):
        self._database = database

    def register(self):
        try:
            data = request.get_json()
            if not data:
                status_msg("Invalid or missing data")

            user_name = data.get("user_name")
            email = data.get("email")
            password = data.get("password")

            if User.query.filter_by(email=email).first():
                status_msg("Email already exists", status_code=409)

            if not user_name or not email or not password:
                status_msg("Incomplete or missing credentials")

            new_user = User(user_name=user_name, email=email)
            new_user.set_password(password=password)

            self._database.session.add(new_user)
            self._database.session.commit()

            status_msg(f"Congratulations {user_name}, your registration is successful", status_code=201)

        except Exception as e:
            self._database.session.rollback()
            server_error(error=e)


    def login(self):
        try:
            data = request.get_json()
            if not data:
                status_msg("Invalid or missing data")

            email = data.get("email")
            password = data.get("password")

            token, _ = User.authenticate_user(email=email, password=password)
            if not token:
                status_msg("Invalid email or password")

            status_msg(f"Login successful, access_token:{token}, token_type:Bearer", 200)

        except Exception as e:
            server_error(error=e)