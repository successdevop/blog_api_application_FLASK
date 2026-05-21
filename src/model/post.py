import secrets
from sqlalchemy.orm import relationship

from src.repo.database import db
from sqlalchemy import Column, String, ForeignKey, Text, DateTime
from datetime import datetime


class Post(db.Model):
    __tablename__ = "posts"
    post_id = Column(String(20), primary_key=True, default=lambda : secrets.token_hex(10))
    title = Column(String(200), nullable=False)
    body = Column(Text, nullable=False)
    created_at = Column(DateTime, index=True, default=datetime.now)
    author_id = Column(String(20), ForeignKey("users.user_id"), nullable=False)
    user = relationship("User", back_populates="posts")
    comments = relationship("Comments", back_populates="post", lazy="dynamic", cascade="all, delete-orphan")