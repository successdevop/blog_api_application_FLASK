from sqlalchemy.orm import relationship

from src.repo.database import Database
from sqlalchemy import Column, Integer, String
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token


class User(Database.db.Model):
    __tablename__ = "users"
    user_id = Column(Integer, unique=True, primary_key=True)
    user_name = Column(String(64), nullable=False, unique=True, index=True)
    email = Column(String(120), nullable=False, unique=True, index=True)
    password = Column(String(20), nullable=False)
    posts = relationship("Post", back_populates="user", lazy="dynamic")

    def set_password(self, password: str):
        self.password = generate_password_hash(password)

    def check_password(self, password: str):
        return check_password_hash(self.password, password)

    @classmethod
    def authenticate_user(cls, email: str, password: str):
        user = cls.query.filter_by(email=email).first()

        if user and user.check_password(password=password):
            access_token = create_access_token(identity=user.email)
            return access_token, user
        return None

    def __repr__(self):
        return f"User(user_id:{self.user_id} | user_name:{self.user_name}"