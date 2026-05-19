from sqlalchemy.orm import relationship

from src.repo.database import Database
from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from datetime import datetime


class Post(Database.db.Model):
    __tablename__ = "posts"
    post_id = Column(Integer, primary_key=True)
    title = Column(String(140))
    body = Column(Text)
    created_at = Column(DateTime, index=True, default=datetime.utcnow())
    author_id = Column(Integer, ForeignKey("users.email"))
    user = relationship("User", back_populates="posts")