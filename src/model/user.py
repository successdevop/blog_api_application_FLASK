from src.repo.database import db
from sqlalchemy import Column, Integer, String


class User(db.Model):
    __tablename__ = "users"
    user_id = Column(Integer, unique=True, primary_key=True)
    user_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)