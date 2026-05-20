import secrets
from sqlalchemy.orm import relationship
from src.repo.database import db
from sqlalchemy import Column, String


class User(db.Model):
    __tablename__ = "users"
    user_id = Column(String(20), primary_key=True, default=lambda : secrets.token_hex(10))
    user_name = Column(String(64), nullable=False, unique=True, index=True)
    email = Column(String(120), nullable=False, unique=True, index=True)
    password = Column(String(225), nullable=False)
    posts = relationship("Post", back_populates="user", lazy="dynamic")
    comments = relationship("Comments", back_populates="user", lazy="dynamic")


    def __repr__(self):
        return f"User(user_id:{self.user_id} | user_name:{self.user_name}"